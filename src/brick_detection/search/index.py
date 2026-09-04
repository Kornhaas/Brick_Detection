"""Small, deterministic cosine-similarity index for the retrieval PoC."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class PartCandidate:
    """A part-level result aggregated from its best matching render views."""

    part_id: str
    score: float
    matching_views: int


@dataclass(frozen=True)
class EmbeddingIndex:
    """An immutable, in-memory normalized vector index."""

    vectors: np.ndarray
    part_ids: tuple[str, ...]
    image_paths: tuple[str, ...]
    model_version: str

    def __post_init__(self) -> None:
        if self.vectors.ndim != 2 or self.vectors.shape[0] != len(self.part_ids):
            raise ValueError("Vectors and part IDs must have matching row counts.")
        if len(self.part_ids) != len(self.image_paths):
            raise ValueError("Part IDs and image paths must have matching lengths.")

    def query(
        self,
        vector: np.ndarray,
        top_render_k: int = 50,
        top_part_k: int = 5,
        evidence_view_k: int = 3,
        exclude_image_path: str | None = None,
    ) -> list[PartCandidate]:
        """Find top renders, then aggregate their scores at part level."""
        if vector.shape != (self.vectors.shape[1],):
            raise ValueError("Query vector dimension does not match index dimension.")
        normalized = vector / np.linalg.norm(vector)
        scores = self.vectors @ normalized
        if exclude_image_path is not None:
            scores = scores.copy()
            for index, image_path in enumerate(self.image_paths):
                if image_path == exclude_image_path:
                    scores[index] = -np.inf
        indices = np.argsort(scores)[::-1][:top_render_k]
        grouped: dict[str, list[float]] = {}
        for index in indices:
            if np.isfinite(scores[index]):
                grouped.setdefault(self.part_ids[int(index)], []).append(float(scores[index]))
        if evidence_view_k < 1:
            raise ValueError("Evidence view count must be positive.")
        candidates = []
        for part_id, values in grouped.items():
            strongest_evidence = sorted(values, reverse=True)[:evidence_view_k]
            candidates.append(
                PartCandidate(part_id, sum(strongest_evidence) / len(strongest_evidence), len(values))
            )
        return sorted(candidates, key=lambda candidate: candidate.score, reverse=True)[:top_part_k]

    def with_reference(self, vector: np.ndarray, part_id: str, image_path: str) -> EmbeddingIndex:
        """Return a new index with one human-confirmed reference embedding added."""
        if vector.shape != (self.vectors.shape[1],):
            raise ValueError("Reference vector dimension does not match index dimension.")
        normalized = vector / np.linalg.norm(vector)
        return EmbeddingIndex(
            np.vstack((self.vectors, normalized.astype(np.float32))),
            self.part_ids + (part_id,),
            self.image_paths + (image_path,),
            self.model_version,
        )

    def save(self, path: Path) -> None:
        """Persist vectors and metadata in one NumPy archive."""
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            path,
            vectors=self.vectors,
            part_ids=np.array(self.part_ids),
            image_paths=np.array(self.image_paths),
            model_version=np.array(self.model_version),
        )

    @classmethod
    def load(cls, path: Path) -> EmbeddingIndex:
        """Load a previously generated index."""
        with np.load(path, allow_pickle=False) as archive:
            return cls(
                vectors=archive["vectors"],
                part_ids=tuple(archive["part_ids"].tolist()),
                image_paths=tuple(archive["image_paths"].tolist()),
                model_version=str(archive["model_version"].item()),
            )
