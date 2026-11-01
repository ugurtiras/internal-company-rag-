"""Split documents into chunks according to the configured strategy."""

import re
from dataclasses import dataclass

from src.ingestion.document import Document


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    access_label: str
    section: str
    text: str


def chunk_document(doc: Document, cfg: dict) -> list[Chunk]:
    """Chunk a single document; chunks inherit the document's access label."""
    strategy = cfg["chunking"]["strategy"]
    if strategy == "section":
        return _chunk_by_section(doc, cfg)
    if strategy == "fixed":
        return _chunk_fixed(doc, cfg)
    raise ValueError(f"unknown chunking strategy: {strategy!r}")


def chunk_documents(docs: list[Document], cfg: dict) -> list[Chunk]:
    """Chunk every document and return the flat chunk list."""
    chunks: list[Chunk] = []
    for doc in docs:
        chunks.extend(chunk_document(doc, cfg))
    return chunks


def _chunk_by_section(doc: Document, cfg: dict) -> list[Chunk]:
    """One chunk per '## ' section; pre-section text becomes the 'Giriş' section.

    The '# ' title line is dropped. Sections longer than max_chars are split at
    blank-line or list-item boundaries (hard line split as a last resort).
    """
    max_chars = cfg["chunking"]["max_chars"]
    chunks: list[Chunk] = []
    index = 0
    for section, body in _iter_sections(doc.text):
        for piece in _split_overlong(body, max_chars):
            header = f"{doc.title} - {section}\n"
            chunk_id = f"{doc.doc_id}#{index}"
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    doc_id=doc.doc_id,
                    title=doc.title,
                    access_label=doc.access_label,
                    section=section,
                    text=header + piece,
                )
            )
            index += 1
    return chunks


def _chunk_fixed(doc: Document, cfg: dict) -> list[Chunk]:
    """Character-window chunks with overlap; no section header is added."""
    size = cfg["chunking"]["fixed_size"]
    overlap = cfg["chunking"]["fixed_overlap"]
    if size <= 0:
        raise ValueError(f"fixed_size must be positive, got {size}")
    if overlap >= size:
        raise ValueError(f"fixed_overlap must be smaller than fixed_size: {overlap} >= {size}")
    step = size - overlap
    chunks: list[Chunk] = []
    index = 0
    for start in range(0, len(doc.text), step):
        piece = doc.text[start : start + size]
        if not piece.strip():
            continue
        chunk_id = f"{doc.doc_id}#{index}"
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                doc_id=doc.doc_id,
                title=doc.title,
                access_label=doc.access_label,
                section="",
                text=piece,
            )
        )
        index += 1
        if start + size >= len(doc.text):
            break
    return chunks


def _iter_sections(text: str) -> list[tuple[str, str]]:
    """Split body text into (section name, section body) pairs."""
    sections: list[tuple[str, str]] = []
    current_name = "Giriş"
    current: list[str] = []

    def flush() -> None:
        content = "\n".join(current).strip()
        if content:
            sections.append((current_name, content))
        current.clear()

    for line in text.splitlines():
        if line.startswith("## "):
            flush()
            current_name = line[3:].strip() or "Giriş"
        elif line.startswith("# "):
            continue
        else:
            current.append(line)
    flush()
    return sections


def _split_overlong(text: str, limit: int) -> list[str]:
    """Return pieces of ``text`` that each fit within ``limit`` characters."""
    if len(text) <= limit:
        return [text]
    return _pack(_blocks(text), limit)


def _blocks(text: str) -> list[str]:
    """Break text into paragraphs; list paragraphs become one block per item."""
    blocks: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        lines = [line.strip() for line in paragraph.splitlines() if line.strip()]
        if any(_is_list_item(line) for line in lines):
            blocks.extend(line for line in lines if _is_list_item(line))
        else:
            blocks.append(paragraph)
    return blocks


def _is_list_item(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith("- ") or stripped.startswith("* ")


def _pack(blocks: list[str], limit: int) -> list[str]:
    """Greedily pack blocks into parts no longer than ``limit`` characters."""
    parts: list[str] = []
    current: list[str] = []
    size = 0
    for block in blocks:
        if len(block) > limit:
            if current:
                parts.append("\n\n".join(current))
                current = []
                size = 0
            parts.extend(_hard_split(block, limit))
            continue
        add = len(block) + (2 if current else 0)
        if current and size + add > limit:
            parts.append("\n\n".join(current))
            current = [block]
            size = len(block)
        else:
            current.append(block)
            size += add
    if current:
        parts.append("\n\n".join(current))
    return parts


def _hard_split(block: str, limit: int) -> list[str]:
    """Last-resort split: line by line, then character windows within a line."""
    parts: list[str] = []
    current: list[str] = []
    size = 0
    for line in block.splitlines():
        if len(line) > limit:
            if current:
                parts.append("\n".join(current))
                current = []
                size = 0
            for start in range(0, len(line), limit):
                piece = line[start : start + limit].strip()
                if piece:
                    parts.append(piece)
            continue
        add = len(line) + (1 if current else 0)
        if current and size + add > limit:
            parts.append("\n".join(current))
            current = [line]
            size = len(line)
        else:
            current.append(line)
            size += add
    if current:
        parts.append("\n".join(current))
    return [part for part in parts if part]
