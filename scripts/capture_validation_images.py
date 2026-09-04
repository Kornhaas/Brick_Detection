"""Capture labeled validation images from a USB camera in a small local GUI."""

from __future__ import annotations

import argparse
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import scrolledtext, ttk

import cv2
from PIL import Image, ImageTk

from brick_detection.assisted_capture import (
    new_reference_root,
    suggestion_preview_paths,
    visible_suggestions,
)
from brick_detection.capture import (
    CaptureRecord,
    append_manifest_record,
    capture_path,
    manifest_records,
    new_holdout_root,
    validate_part_id,
)
from brick_detection.search import EmbeddingIndex
from brick_detection.vision import DINOv2Encoder
from brick_detection.vision.preprocess import foreground_square_crop


class CaptureApplication:
    """Preview one camera and persist deliberate, labeled captures."""

    def __init__(
        self,
        root: tk.Tk,
        camera_index: int,
        validation_root: Path,
        width: int,
        height: int,
        fps: int,
        index_path: Path | None,
        minimum_similarity: float,
        maximum_suggestions: int,
    ) -> None:
        self.root = root
        self.validation_root = validation_root.resolve()
        self.camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if not self.camera.isOpened():
            self.camera.release()
            raise RuntimeError(f"USB camera {camera_index} could not be opened.")
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.camera.set(cv2.CAP_PROP_FPS, fps)
        self.latest_frame: object | None = None
        self.index = EmbeddingIndex.load(index_path) if index_path is not None else None
        self.encoder = DINOv2Encoder() if self.index is not None else None
        if self.index is not None and self.index.model_version != self.encoder.version:
            raise RuntimeError(
                f"Index expects {self.index.model_version}, encoder is {self.encoder.version}."
            )
        self.minimum_similarity = minimum_similarity
        self.maximum_suggestions = maximum_suggestions
        self.has_started_initial_recognition = False
        self.has_received_first_frame = False
        self.suggestion_images: list[ImageTk.PhotoImage] = []
        self.camera_error_reported = False

        root.title(f"BrickVision – Validierungsaufnahmen ({self.validation_root.name})")
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.minsize(760, 620)
        controls = ttk.Frame(root, padding=12)
        controls.pack(fill="x")
        if self.index is not None:
            ttk.Button(controls, text="Teil erkennen", command=self.suggest).grid(
                row=0, column=0, padx=(0, 12), sticky="w"
            )
            self.suggestion_buttons = ttk.Frame(controls)
            self.suggestion_buttons.grid(row=0, column=1, sticky="ew")
        ttk.Label(controls, text="Manuelle ID (Fallback):").grid(row=1, column=0, sticky="w")
        self.part_id = tk.StringVar()
        part_input = ttk.Entry(controls, textvariable=self.part_id, width=28)
        part_input.grid(row=1, column=1, padx=(8, 16), sticky="ew")
        ttk.Button(controls, text="Manuell speichern", command=self.capture).grid(row=1, column=2)
        controls.columnconfigure(1, weight=1)
        self.status = tk.StringVar(value=f"Kamera {camera_index} wird gestartet …")
        ttk.Label(controls, textvariable=self.status).grid(
            row=2, column=0, columnspan=3, pady=(8, 0), sticky="w"
        )
        self.preview = ttk.Label(root, anchor="center")
        self.preview.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        activity = ttk.LabelFrame(root, text="Aktivitaetslog", padding=6)
        activity.pack(fill="x", padx=12, pady=(0, 12))
        self.activity_log = scrolledtext.ScrolledText(activity, height=5, state="disabled")
        self.activity_log.pack(fill="x")
        self.report(f"Starte Kamera {camera_index}; Ziel: {self.validation_root.name}")
        if self.index is not None:
            self.report(f"Renderindex geladen: {len(self.index.part_ids)} Ansichten")
        self.add_existing_session_references()
        root.bind("<Return>", lambda _event: self.capture())
        self.update_preview()

    def report(self, message: str) -> None:
        """Show the current meaningful operation in the status line and activity log."""
        self.status.set(message)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activity_log.configure(state="normal")
        self.activity_log.insert("end", f"[{timestamp}] {message}\n")
        self.activity_log.see("end")
        self.activity_log.configure(state="disabled")

    def update_preview(self) -> None:
        """Read and display the next preview frame."""
        success, frame = self.camera.read()
        if success:
            self.latest_frame = frame
            if not self.has_received_first_frame:
                self.has_received_first_frame = True
                height, width = frame.shape[:2]
                self.report(
                    f"Live: {width}×{height}. Ziel: {self.validation_root.name}. "
                    "Erkennung startet …"
                )
                if self.index is not None and not self.has_started_initial_recognition:
                    self.has_started_initial_recognition = True
                    self.root.after(100, self.suggest)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_frame)
            image.thumbnail((960, 700))
            rendered = ImageTk.PhotoImage(image=image)
            self.preview.configure(image=rendered)
            self.preview.image = rendered
        else:
            if not self.camera_error_reported:
                self.camera_error_reported = True
                self.report("Kein Kamerabild verfügbar. Verbindung und Kameraindex prüfen.")
        self.root.after(30, self.update_preview)

    def suggest(self) -> None:
        """Show render-index candidates; saving still requires explicit human confirmation."""
        if self.latest_frame is None or self.index is None or self.encoder is None:
            self.report("Erkennung wartet noch auf ein Kamerabild.")
            return
        self.report(
            "Erkennung läuft: Vordergrund wird zugeschnitten und mit Referenzen verglichen."
        )
        image = Image.fromarray(cv2.cvtColor(self.latest_frame, cv2.COLOR_BGR2RGB))
        vector = self.encoder.embed_images([image], crop_foreground=True)[0]
        candidates = visible_suggestions(
            self.index.query(vector, top_part_k=self.maximum_suggestions),
            self.minimum_similarity,
            self.maximum_suggestions,
        )
        for button in self.suggestion_buttons.winfo_children():
            button.destroy()
        self.suggestion_images = []
        if not candidates:
            self.report("Kein Vorschlag über dem Similarity-Filter. Teil-ID manuell eingeben.")
            return
        preview_paths = suggestion_preview_paths(
            candidates, self.index.image_paths, self.index.part_ids
        )
        for column, candidate in enumerate(candidates):
            label = f"{candidate.part_id} ({candidate.score:.1%} ähnlich)"
            preview = self.load_suggestion_preview(preview_paths.get(candidate.part_id))
            button = ttk.Button(
                self.suggestion_buttons,
                text=label,
                command=lambda part_id=candidate.part_id: self.confirm_suggestion(part_id),
                compound="top",
            )
            if preview is not None:
                button.configure(image=preview)
                self.suggestion_images.append(preview)
            button.grid(row=0, column=column, padx=4, sticky="n")
        top_candidate = candidates[0]
        self.report(
            f"{len(candidates)} Vorschläge bereit; Top: {top_candidate.part_id} "
            f"mit {top_candidate.score:.1%} Ähnlichkeit. Bitte visuell bestätigen."
        )

    @staticmethod
    def load_suggestion_preview(path: Path | None) -> ImageTk.PhotoImage | None:
        """Load a compact render preview without preventing candidate selection on failure."""
        if path is None or not path.is_file():
            return None
        with Image.open(path) as image:
            preview = image.copy()
        preview = foreground_square_crop(preview, padding_ratio=0.12)
        preview.thumbnail((180, 180))
        return ImageTk.PhotoImage(image=preview)

    def confirm_suggestion(self, part_id: str) -> None:
        """Copy a deliberately selected suggestion into the known-ID field and save it."""
        self.part_id.set(part_id)
        self.capture()

    def capture(self) -> None:
        """Save the current frame only when a known part ID is supplied."""
        try:
            part_id = validate_part_id(self.part_id.get())
        except ValueError as error:
            self.report(f"Nicht gespeichert: {error}")
            return
        if self.latest_frame is None:
            self.report("Nicht gespeichert: Noch kein Kamerabild verfügbar.")
            return
        output_path = capture_path(self.validation_root, part_id, datetime.now())
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(output_path), self.latest_frame):
            self.report("Foto konnte nicht gespeichert werden.")
            return
        relative_path = output_path.relative_to(self.validation_root).as_posix()
        append_manifest_record(self.validation_root, CaptureRecord(relative_path, part_id))
        self.add_reference_image(output_path, part_id)
        self.report(f"Gespeichert und als echte Referenz aktiviert: {relative_path}")

    def add_existing_session_references(self) -> None:
        """Make already confirmed images from this session available after an app restart."""
        if self.index is None or self.encoder is None:
            return
        activated_count = 0
        for record in manifest_records(self.validation_root):
            image_path = (self.validation_root / record.image_path).resolve()
            if image_path.is_file():
                self.add_reference_image(image_path, record.part_id)
                activated_count += 1
        if activated_count:
            self.report(
                f"{activated_count} bestätigte Echtbild-Referenzen aus dieser Sitzung aktiviert."
            )

    def add_reference_image(self, image_path: Path, part_id: str) -> None:
        """Add one human-confirmed camera image to the in-memory session index."""
        if self.index is None or self.encoder is None:
            return
        with Image.open(image_path) as image:
            vector = self.encoder.embed_images([image.convert("RGB")], crop_foreground=True)[0]
        self.index = self.index.with_reference(vector, part_id, str(image_path.resolve()))

    def close(self) -> None:
        """Release the camera before closing the local window."""
        self.camera.release()
        self.root.destroy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera", type=int, default=0, help="USB camera index (default: 0)")
    parser.add_argument(
        "--width", type=int, default=4656, help="Requested capture width (default: 4656)"
    )
    parser.add_argument(
        "--height", type=int, default=3496, help="Requested capture height (default: 3496)"
    )
    parser.add_argument("--fps", type=int, default=15, help="Requested capture rate (default: 15)")
    parser.add_argument("--output", type=Path, help="Existing local validation directory to resume")
    parser.add_argument(
        "--index", type=Path, help="Synthetic index for human-confirmed suggestions"
    )
    parser.add_argument("--min-similarity", type=float, default=0.5)
    parser.add_argument("--max-suggestions", type=int, default=5)
    arguments = parser.parse_args()
    output = arguments.output
    if output is None:
        output = (
            new_reference_root(Path("data/references/real"), datetime.now())
            if arguments.index is not None
            else new_holdout_root(Path("data/validation"), datetime.now())
        )
    root = tk.Tk()
    CaptureApplication(
        root,
        arguments.camera,
        output,
        arguments.width,
        arguments.height,
        arguments.fps,
        arguments.index.resolve() if arguments.index is not None else None,
        arguments.min_similarity,
        arguments.max_suggestions,
    )
    root.mainloop()


if __name__ == "__main__":
    main()
