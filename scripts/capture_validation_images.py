"""Capture labeled validation images from a USB camera in a small local GUI."""

from __future__ import annotations

import argparse
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import ttk

import cv2
from PIL import Image, ImageTk

from brick_detection.capture import (
    CaptureRecord,
    append_manifest_record,
    capture_path,
    new_holdout_root,
    validate_part_id,
)


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

        root.title(f"BrickVision – Validierungsaufnahmen ({self.validation_root.name})")
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.minsize(760, 620)
        controls = ttk.Frame(root, padding=12)
        controls.pack(fill="x")
        ttk.Label(controls, text="Bekannte LDraw-Teil-ID:").grid(row=0, column=0, sticky="w")
        self.part_id = tk.StringVar()
        part_input = ttk.Entry(controls, textvariable=self.part_id, width=28)
        part_input.grid(row=0, column=1, padx=(8, 16), sticky="ew")
        part_input.focus_set()
        ttk.Button(controls, text="Foto aufnehmen", command=self.capture).grid(row=0, column=2)
        controls.columnconfigure(1, weight=1)
        self.status = tk.StringVar(value=f"Kamera {camera_index} wird gestartet …")
        ttk.Label(controls, textvariable=self.status).grid(
            row=1, column=0, columnspan=3, pady=(8, 0), sticky="w"
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
                    f"Live: {width}×{height}. Ziel: {self.validation_root.name}. Teil-ID eingeben."
                )
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_frame)
            image.thumbnail((960, 700))
            rendered = ImageTk.PhotoImage(image=image)
            self.preview.configure(image=rendered)
            self.preview.image = rendered
        else:
            self.status.set("Kein Kamerabild verfügbar. Verbindung und Kameraindex prüfen.")
        self.root.after(30, self.update_preview)

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
    arguments = parser.parse_args()
    output = arguments.output or new_holdout_root(Path("data/validation"), datetime.now())
    root = tk.Tk()
    CaptureApplication(
        root,
        arguments.camera,
        output,
        arguments.width,
        arguments.height,
        arguments.fps,
    )
    root.mainloop()


if __name__ == "__main__":
    main()
