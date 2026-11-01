"""Load every supported document from a directory."""

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from src.ingestion.document import Document, InvalidDocumentError, load_document

# One reader per file extension. To support a new format, add a reader here.
READERS: dict[str, Callable[[Path], Document]] = {
    ".md": load_document,
}


@dataclass
class LoadReport:
    documents: list[Document] = field(default_factory=list)
    rejected: dict[str, str] = field(default_factory=dict)
    unsupported: list[str] = field(default_factory=list)


def load_directory(directory: Path) -> LoadReport:
    """Load all supported files. Invalid files are skipped and reported, never indexed."""
    report = LoadReport()
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        reader = READERS.get(path.suffix.lower())
        if reader is None:
            report.unsupported.append(path.name)
            continue
        try:
            report.documents.append(reader(path))
        except (InvalidDocumentError, UnicodeDecodeError) as exc:
            report.rejected[path.name] = str(exc)
    return report
