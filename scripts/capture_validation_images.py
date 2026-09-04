"""Capture labeled validation images from a USB camera in a small local GUI."""

from __future__ import annotations

import argparse
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import ttk

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
        self.suggestion_images: list[ImageTk.PhotoImage] = []

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
        self.preview.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        root.bind("<Return>", lambda _event: self.capture())
        self.update_preview()

    def update_preview(self) -> None:
        """Read and display the next preview frame."""
        success, frame = self.camera.read()
        if success:
            self.latest_frame = frame
            if self.status.get().endswith("wird gestartet …"):
                height, width = frame.shape[:2]
                self.status.set(
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
            self.status.set("Kein Kamerabild verfügbar. Verbindung und Kameraindex prüfen.")
        self.root.after(30, self.update_preview)

    def suggest(self) -> None:
        """Show render-index candidates; saving still requires explicit human confirmation."""
        if self.latest_frame is None or self.index is None or self.encoder is None:
            self.status.set("Noch kein Kamerabild für Vorschläge verfügbar.")
            return
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
            self.status.set("Kein Vorschlag über dem Similarity-Filter. Teil-ID manuell eingeben.")
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
        self.status.set("Vorschlag wählen, nur wenn das echte Teil sicher bestätigt ist.")

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
            self.status.set(f"Nicht gespeichert: {error}")
            return
        if self.latest_frame is None:
            self.status.set("Noch kein Kamerabild verfügbar.")
            return
        output_path = capture_path(self.validation_root, part_id, datetime.now())
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(output_path), self.latest_frame):
            self.status.set("Foto konnte nicht gespeichert werden.")
            return
        relative_path = output_path.relative_to(self.validation_root).as_posix()
        append_manifest_record(self.validation_root, CaptureRecord(relative_path, part_id))
        self.status.set(f"Gespeichert: {relative_path}")

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
