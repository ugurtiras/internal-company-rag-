"""Assemble chunks and retrievers from configuration."""

from pathlib import Path

from src.chunking.chunker import Chunk, chunk_documents
from src.embeddings.encoder import SentenceTransformerEncoder
from src.ingestion.loader import load_directory
from src.retrieval import bm25, dense


def load_chunks(cfg: dict) -> list[Chunk]:
    """Load documents from data.raw_dir, fail on any rejected file, then chunk."""
    raw_dir = Path(cfg["data"]["raw_dir"])
    report = load_directory(raw_dir)
    if report.rejected:
        raise ValueError(f"rejected documents in {raw_dir}: {report.rejected}")
    return chunk_documents(report.documents, cfg)


def build_retriever(cfg: dict, chunks: list[Chunk]):
    """Create the retriever configured as retrieval.type."""
    rtype = cfg["retrieval"]["type"]
    if rtype == "bm25":
        bm25_cfg = cfg["retrieval"]["bm25"]
        index = bm25.build_index(
            chunks, k1=bm25_cfg["k1"], b=bm25_cfg["b"], stem_prefix=bm25_cfg["stem_prefix"]
        )
        return bm25.Bm25Retriever(index)
    if rtype == "dense":
        dense_cfg = cfg["retrieval"]["dense"]
        encoder = SentenceTransformerEncoder(
            model_name=dense_cfg["model_name"],
            query_prefix=dense_cfg["query_prefix"],
            passage_prefix=dense_cfg["passage_prefix"],
        )
        return dense.DenseRetriever(chunks, encoder)
    raise ValueError(f"unknown retrieval type: {rtype!r}")
