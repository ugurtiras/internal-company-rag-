"""Tests for the dense retriever using a fake encoder (no network, no model)."""

from src.chunking.chunker import Chunk
from src.retrieval.dense import DenseRetriever


class FakeEncoder:
    """Deterministic encoder: 'x' maps to axis one, 'z' to axis two, other
    texts mix both axes, so rankings stay unambiguous."""

    def encode_passages(self, passages: list[str]) -> list[list[float]]:
        return [
            [1.0, 0.0] if "x" in text else [0.0, 1.0] if "z" in text else [0.5, 0.5]
            for text in passages
        ]

    def encode_query(self, query: str) -> list[float]:
        if "x" in query:
            return [1.0, 0.0]
        if "z" in query:
            return [0.0, 1.0]
        return [0.5, 0.5]


def make_chunk(doc_id: str, label: str, text: str) -> Chunk:
    return Chunk(
        chunk_id=f"{doc_id}#0", doc_id=doc_id, title="t", access_label=label, section="s", text=text
    )


def test_ranking_and_filter_with_fake_encoder() -> None:
    chunks = [
        make_chunk("DST-001", "destek", "ayni içerik"),
        make_chunk("DST-002", "destek", "x içerik"),
        make_chunk("HUK-003", "hukuk", "x içerik"),
    ]
    retriever = DenseRetriever(chunks, FakeEncoder())

    unfiltered = [chunk.doc_id for chunk, _ in retriever.search("x", 5, None)]
    assert unfiltered == ["DST-002", "HUK-003", "DST-001"]

    filtered = retriever.search("x", 1, frozenset({"destek"}))
    assert [chunk.doc_id for chunk, _ in filtered] == ["DST-002"]
    assert all(chunk.access_label == "destek" for chunk, _ in filtered)


def test_query_to_other_axis_ranks_other_chunks() -> None:
    chunks = [
        make_chunk("DST-001", "destek", "z içerik"),
        make_chunk("SAT-001", "satis", "ayni başka içerik"),
    ]
    retriever = DenseRetriever(chunks, FakeEncoder())
    results = retriever.search("z", 5, None)
    assert [chunk.doc_id for chunk, _ in results] == ["DST-001", "SAT-001"]


def test_empty_allowed_labels_return_no_results() -> None:
    chunks = [make_chunk("TST-001", "destek", "x içerik")]
    retriever = DenseRetriever(chunks, FakeEncoder())
    assert retriever.search("x", 5, frozenset()) == []
