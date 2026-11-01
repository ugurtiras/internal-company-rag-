"""Turn a markdown file into a validated Document."""

import re
from dataclasses import dataclass
from pathlib import Path

from src.ingestion.access import is_valid_access_label
from src.ingestion.frontmatter import split_front_matter

DOC_ID_PATTERN = re.compile(r"^([A-Z]+)-(\d{3})$")


class InvalidDocumentError(ValueError):
    """Raised when a document must not be indexed."""


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    department: str
    access_label: str
    text: str


def parse_document(content: str) -> Document:
    try:
        meta, text = split_front_matter(content)
    except ValueError as exc:
        raise InvalidDocumentError(str(exc)) from exc

    doc_id = str(meta.get("doc_id", "")).strip()
    if not DOC_ID_PATTERN.match(doc_id):
        raise InvalidDocumentError(f"invalid doc_id: {doc_id!r}")

    label = meta.get("erisim")
    if not is_valid_access_label(label):
        raise InvalidDocumentError(f"invalid access label: {label!r}")

    title = str(meta.get("baslik", "")).strip()
    if not title:
        raise InvalidDocumentError("missing title")

    return Document(
        doc_id=doc_id,
        title=title,
        department=str(meta.get("departman", "")).strip(),
        access_label=label,
        text=text,
    )


def load_document(path: Path) -> Document:
    return parse_document(path.read_text(encoding="utf-8"))
