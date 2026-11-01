"""Dense retrieval with cosine similarity and in-loop access filtering."""

import math

from src.chunking.chunker import Chunk


def _normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0.0:
        return [0.0] * len(vector)
    return [value / norm for value in vector]


class DenseRetriever:
    """Cosine-similarity retriever over encoder vectors.

    The encoder is injected (see src/embeddings/encoder.py). Access filtering
    happens inside the ranking loop: chunks outside the allowed labels are
    skipped and never consume a top-k slot. Corpus vectors are computed lazily
    on the first search and cached.
    """

    def __init__(self, chunks: list[Chunk], encoder) -> None:
        self.chunks = list(chunks)
        self.encoder = encoder
        self._vectors: list[list[float]] | None = None

    def search(
        self,
        query: str,
        k: int,
        allowed_labels: frozenset[str] | None,
    ) -> list[tuple[Chunk, float]]:
        """Return the top-k (chunk, score) pairs, best first, for the role.

        Passing None for ``allowed_labels`` disables the role filter entirely;
        this is available for evaluation controls only.
        """
        if k <= 0 or not self.chunks:
            return []
        if self._vectors is None:
            self._vectors = self.encoder.encode_passages([chunk.text for chunk in self.chunks])
        query_vec = _normalize(self.encoder.encode_query(query))
        scored: list[tuple[float, str, Chunk]] = []
        for chunk, vector in zip(self.chunks, self._vectors, strict=True):
            if allowed_labels is not None and chunk.access_label not in allowed_labels:
                continue
            normed = _normalize(vector)
            score = sum(q * v for q, v in zip(query_vec, normed, strict=True))
            scored.append((score, chunk.chunk_id, chunk))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return [(chunk, score) for score, _, chunk in scored[:k]]
