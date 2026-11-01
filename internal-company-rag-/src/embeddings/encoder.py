"""Encoder interface used by the dense retriever."""

from typing import Protocol


class Encoder(Protocol):
    """Encodes passages and queries into embedding vectors."""

    def encode_passages(self, passages: list[str]) -> list[list[float]]:
        """Encode a batch of passage texts into normalized vectors."""
        ...

    def encode_query(self, query: str) -> list[float]:
        """Encode one query text into a normalized vector."""
        ...


class SentenceTransformerEncoder:
    """E5-style encoder backed by sentence-transformers, imported lazily so the
    default BM25 install never needs this package. Query and passage prefixes
    come from config; vectors are normalized (normalize_embeddings=True)."""

    def __init__(self, model_name: str, query_prefix: str, passage_prefix: str) -> None:
        self._model_name = model_name
        self._query_prefix = query_prefix
        self._passage_prefix = passage_prefix
        self._model = None

    def _get_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self._model_name)
        return self._model

    def encode_passages(self, passages: list[str]) -> list[list[float]]:
        model = self._get_model()
        texts = [f"{self._passage_prefix}{text}" for text in passages]
        embeddings = model.encode(texts, normalize_embeddings=True)
        return [[float(value) for value in row] for row in embeddings]

    def encode_query(self, query: str) -> list[float]:
        model = self._get_model()
        embedding = model.encode([f"{self._query_prefix}{query}"], normalize_embeddings=True)[0]
        return [float(value) for value in embedding]
