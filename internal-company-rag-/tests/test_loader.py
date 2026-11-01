from pathlib import Path

from src.ingestion.loader import load_directory

VALID = """---
doc_id: YON-001
baslik: Test Title
departman: Yönetim
erisim: tum_calisanlar
---

# Body
"""


def test_valid_files_are_loaded(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text(VALID, encoding="utf-8")
    report = load_directory(tmp_path)
    assert len(report.documents) == 1
    assert report.rejected == {}


def test_invalid_file_is_reported_not_loaded(tmp_path: Path) -> None:
    (tmp_path / "good.md").write_text(VALID, encoding="utf-8")
    (tmp_path / "bad.md").write_text(VALID.replace("tum_calisanlar", "herkes"), encoding="utf-8")
    report = load_directory(tmp_path)
    assert [d.doc_id for d in report.documents] == ["YON-001"]
    assert "bad.md" in report.rejected


def test_unknown_extension_is_reported(tmp_path: Path) -> None:
    (tmp_path / "notes.pdf").write_bytes(b"%PDF")
    (tmp_path / ".gitkeep").write_text("", encoding="utf-8")
    report = load_directory(tmp_path)
    assert report.documents == []
    assert report.unsupported == ["notes.pdf"]
