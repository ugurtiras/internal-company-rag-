"""Tests for the chunker: sections, prefixes, splitting, fixed windows."""

import pytest

from src.chunking.chunker import chunk_document, chunk_documents
from src.ingestion.document import Document

CFG_SECTION = {
    "chunking": {"strategy": "section", "max_chars": 1200, "fixed_size": 500, "fixed_overlap": 100}
}


def make_doc(doc_id: str, access_label: str, text: str) -> Document:
    return Document(
        doc_id=doc_id,
        title="Örnek Başlık",
        department="Test",
        access_label=access_label,
        text=text,
    )


def simple_body() -> str:
    return (
        "# Örnek Başlık\n\n"
        "## 1. Amaç\n\nBu belge amaç içerir.\n\n"
        "## 2. Kapsam\n\nKapsam buradadır.\n"
    )


def test_each_section_becomes_chunk_with_title_prefix() -> None:
    doc = make_doc("TST-001", "destek", simple_body())
    chunks = chunk_document(doc, CFG_SECTION)
    sections = [chunk.section for chunk in chunks]
    assert sections == ["1. Amaç", "2. Kapsam"]
    assert chunks[0].text.startswith("Örnek Başlık - 1. Amaç\nBu belge amaç içerir.")
    assert chunks[1].text.startswith("Örnek Başlık - 2. Kapsam\nKapsam buradadır.")


def test_chunk_ids_are_doc_id_and_index() -> None:
    doc = make_doc("TST-001", "destek", simple_body())
    chunks = chunk_document(doc, CFG_SECTION)
    assert [chunk.chunk_id for chunk in chunks] == ["TST-001#0", "TST-001#1"]


def test_chunks_inherit_access_label() -> None:
    doc = make_doc("TST-002", "ik_gizli", simple_body())
    chunks = chunk_document(doc, CFG_SECTION)
    assert {chunk.access_label for chunk in chunks} == {"ik_gizli"}


def test_text_before_first_section_is_giris() -> None:
    body = "# Başlık\n\nBu giriş metnidir.\n\n## 1. Gövde\n\nİçerik.\n"
    doc = make_doc("TST-003", "satis", body)
    chunks = chunk_document(doc, CFG_SECTION)
    assert chunks[0].section == "Giriş"
    assert "Bu giriş metnidir." in chunks[0].text
    assert chunks[1].section == "1. Gövde"


def test_long_section_is_split_within_limit() -> None:
    long = ""
    for i in range(10):
        long += f"Paragraf {i} " + "kelime " * 150
        long += "\n\n"
    body = f"# Başlık\n\n## 1. Long\n\n{long}"
    doc = make_doc("TST-004", "finans", body)
    cfg = {"chunking": {**CFG_SECTION["chunking"], "max_chars": 300}}
    chunks = chunk_document(doc, cfg)
    assert len(chunks) > 1
    header_len = len("Örnek Başlık - 1. Long\n")
    for chunk in chunks:
        # body pieces respect max_chars; the added title/section header adds a small overhead
        assert len(chunk.text) <= 300 + header_len
        assert chunk.text.startswith("Örnek Başlık - 1. Long\n")
        assert chunk.chunk_id.startswith("TST-004#")
    joined = "\n".join(chunk.text.split("\n", 1)[1] for chunk in chunks)
    for i in range(10):
        assert f"Paragraf {i}" in joined


def test_fixed_window_with_overlap() -> None:
    doc = make_doc("TST-005", "destek", "abcdefghij")
    cfg = {
        "chunking": {"strategy": "fixed", "fixed_size": 4, "fixed_overlap": 1, "max_chars": 1200}
    }
    chunks = chunk_document(doc, cfg)
    texts = [chunk.text for chunk in chunks]
    assert texts == ["abcd", "defg", "ghij"]
    assert [chunk.chunk_id for chunk in chunks] == ["TST-005#0", "TST-005#1", "TST-005#2"]


def test_fixed_overlap_larger_than_size_raises() -> None:
    doc = make_doc("TST-006", "destek", "metin")
    cfg = {
        "chunking": {
            "strategy": "fixed",
            "fixed_size": 100,
            "fixed_overlap": 100,
            "max_chars": 1200,
        }
    }
    with pytest.raises(ValueError, match="fixed_overlap"):
        chunk_document(doc, cfg)


def test_unknown_strategy_raises() -> None:
    doc = make_doc("TST-007", "destek", "metin")
    with pytest.raises(ValueError, match="unknown chunking strategy"):
        chunk_document(doc, {"chunking": {"strategy": "semantic"}})


def test_chunk_documents_flattens() -> None:
    docs = [make_doc("TST-001", "satis", simple_body()), make_doc("TST-002", "ik", simple_body())]
    chunks = chunk_documents(docs, CFG_SECTION)
    assert [chunk.doc_id for chunk in chunks] == ["TST-001", "TST-001", "TST-002", "TST-002"]
