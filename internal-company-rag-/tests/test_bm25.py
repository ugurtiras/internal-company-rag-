"""Tests for the BM25 retriever and the access filter placement."""

import pytest

from src.retrieval.access import UnknownRoleError, allowed_labels
from src.retrieval.bm25 import Bm25Retriever, build_index
from src.chunking.chunker import Chunk

CFG = {
    "roles": {
        "destek": ["tum_calisanlar", "destek"],
        "hukuk": ["hukuk"],
    }
}


def make_chunk(doc_id: str, label: str, text: str) -> Chunk:
    return Chunk(
        chunk_id=f"{doc_id}#0", doc_id=doc_id, title="t", access_label=label, section="s", text=text
    )


def test_turkish_case_folding_matches() -> None:
    chunks = [make_chunk("TST-001", "tum_calisanlar", "IŞIK İzin ışık")]
    index = build_index(chunks, k1=1.5, b=0.75, stem_prefix=0)
    results = Bm25Retriever(index).search("ışık", 5, None)
    assert len(results) == 1
    assert results[0][0].doc_id == "TST-001"


def test_prefix_stemming_connects_variants() -> None:
    chunks = [
        make_chunk("TST-010", "tum_calisanlar", "kredi hesaplanır"),
        make_chunk("TST-011", "tum_calisanlar", "taleb ortalama"),
    ]
    index = build_index(chunks, k1=1.5, b=0.75, stem_prefix=5)
    results = Bm25Retriever(index).search("krediler", 5, None)
    doc_ids = [chunk.doc_id for chunk, _ in results]
    assert doc_ids == ["TST-010"]


def test_filter_applies_before_ranking() -> None:
    allowed = make_chunk("DST-001", "destek", "SLA kredi talep süreci")
    forbidden = make_chunk("HUK-003", "hukuk", "SLA kredi tazminat oranları")
    index = build_index([forbidden, allowed], k1=1.5, b=0.75, stem_prefix=0)
    retriever = Bm25Retriever(index)

    unfiltered = retriever.search("SLA kredi tazminat", 5, None)
    assert unfiltered[0][0].doc_id == "HUK-003"

    filtered = retriever.search("SLA kredi tazminat", 1, frozenset({"destek"}))
    doc_ids = [chunk.doc_id for chunk, _ in filtered]
    assert doc_ids == ["DST-001"]
    assert all(chunk.access_label in {"destek"} for chunk, _ in filtered)


def test_empty_allowed_labels_return_no_results() -> None:
    chunks = [make_chunk("TST-001", "destek", "içerik")]
    index = build_index(chunks, k1=1.5, b=0.75, stem_prefix=0)
    assert Bm25Retriever(index).search("içerik", 5, frozenset()) == []


def test_zero_score_chunks_are_dropped() -> None:
    chunks = [make_chunk("TST-001", "destek", "içerikunity")]
    index = build_index(chunks, k1=1.5, b=0.75, stem_prefix=0)
    assert Bm25Retriever(index).search("farklı terimler", 5, None) == []


def test_control_mode_disables_filter() -> None:
    chunks = [make_chunk("HUK-003", "hukuk", "tazminat")]
    index = build_index(chunks, k1=1.5, b=0.75, stem_prefix=0)
    results = Bm25Retriever(index).search("tazminat", 5, None)
    assert [chunk.doc_id for chunk, _ in results] == ["HUK-003"]


def test_unknown_role_raises() -> None:
    with pytest.raises(UnknownRoleError):
        allowed_labels("misafir", CFG["roles"])


def test_invalid_label_in_role_config_raises() -> None:
    cfg = {"destek": ["tum_calisanlar", "herkes"]}
    with pytest.raises(ValueError, match="herkes"):
        allowed_labels("destek", cfg)
