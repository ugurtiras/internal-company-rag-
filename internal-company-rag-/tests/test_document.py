import pytest

from src.ingestion.document import InvalidDocumentError, parse_document

VALID = """---
doc_id: YON-001
baslik: Test Title
departman: Yönetim
erisim: tum_calisanlar
---

# Body
"""


def test_valid_document_is_parsed() -> None:
    doc = parse_document(VALID)
    assert doc.doc_id == "YON-001"
    assert doc.access_label == "tum_calisanlar"
    assert doc.text.startswith("# Body")


def test_unknown_access_label_is_rejected() -> None:
    with pytest.raises(InvalidDocumentError):
        parse_document(VALID.replace("tum_calisanlar", "herkes"))


def test_missing_access_label_is_rejected() -> None:
    with pytest.raises(InvalidDocumentError):
        parse_document(VALID.replace("erisim: tum_calisanlar\n", ""))


def test_bad_doc_id_is_rejected() -> None:
    with pytest.raises(InvalidDocumentError):
        parse_document(VALID.replace("YON-001", "yon1"))


def test_no_front_matter_is_rejected() -> None:
    with pytest.raises(InvalidDocumentError):
        parse_document("# only a heading")
