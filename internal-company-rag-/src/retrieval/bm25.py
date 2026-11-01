"""BM25 retrieval with pre-ranking access filtering. No external dependencies."""

import math
import re
from collections import Counter
from dataclasses import dataclass, field

from src.chunking.chunker import Chunk

TOKEN_PATTERN = re.compile(r"\w+", re.UNICODE)


def _lower_tr(text: str) -> str:
    """Turkish-aware lowercasing: dotted/capital 'İ' and dotless 'I' map correctly."""
    return text.replace("İ", "i").replace("I", "ı").lower()


def _tokens(text: str, stem_prefix: int) -> list[str]:
    tokens = TOKEN_PATTERN.findall(_lower_tr(text))
    if stem_prefix > 0:
        tokens = [token[:stem_prefix] for token in tokens]
    return tokens


def _idf(df: int, total_docs: int) -> float:
    """Standard BM25 idf: ln(1 + (N - df + 0.5) / (df + 0.5))."""
    return math.log(1.0 + (total_docs - df + 0.5) / (df + 0.5))


@dataclass(frozen=True)
class Bm25Index:
    """Precomputed index statistics over the full corpus."""

    chunks: list[Chunk]
    k1: float
    b: float
    stem_prefix: int
    term_freqs: list[Counter] = field(default_factory=list)
    doc_lengths: list[int] = field(default_factory=list)
    doc_freqs: dict[str, int] = field(default_factory=dict)
    avg_doc_len: float = 0.0


def build_index(chunks: list[Chunk], k1: float, b: float, stem_prefix: int) -> Bm25Index:
    """Tokenize every chunk and compute corpus statistics (df over all chunks)."""
    term_freqs: list[Counter] = []
    doc_lengths: list[int] = []
    doc_freqs: dict[str, int] = {}
    for chunk in chunks:
        tf = Counter(_tokens(chunk.text, stem_prefix))
        term_freqs.append(tf)
        doc_lengths.append(sum(tf.values()))
        for term in tf:
            doc_freqs[term] = doc_freqs.get(term, 0) + 1
    avg = sum(doc_lengths) / len(chunks) if chunks else 0.0
    return Bm25Index(
        chunks=chunks, k1=k1, b=b, stem_prefix=stem_prefix,
        term_freqs=term_freqs, doc_lengths=doc_lengths,
        doc_freqs=doc_freqs, avg_doc_len=avg,
    )


class Bm25Retriever:
    """BM25 scorer. Access filtering happens BEFORE scoring: chunks outside the
    allowed labels are never scored, so they cannot occupy a top-k slot.
    Corpus statistics (N, df) are computed over the whole index, so scores are
    stable regardless of the caller's role."""

    def __init__(self, index: Bm25Index) -> None:
        self._index = index

    @property
    def chunks(self) -> list[Chunk]:
        return self._index.chunks

    def search(
        self,
        query: str,
        k: int,
        allowed_labels: frozenset[str] | None,
    ) -> list[tuple[Chunk, float]]:
        """Return the top-k (chunk, score) pairs, best first, for the role.

        ``allowed_labels`` restricts which chunks may be scored. Passing None
        disables the role filter entirely; this is available for evaluation
        controls only.
        """
        if k <= 0 or not self._index.chunks:
            return []
        query_tokens = _tokens(query, self._index.stem_prefix)
        if not query_tokens:
            return []
        query_tf = Counter(query_tokens)
        index = self._index
        total_docs = len(index.chunks)
        scored: list[tuple[float, str, Chunk]] = []
        for pos, chunk in enumerate(index.chunks):
            if allowed_labels is not None and chunk.access_label not in allowed_labels:
                continue
            score = self._score_one(pos, query_tf, total_docs)
            if score > 0:
                scored.append((score, chunk.chunk_id, chunk))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return [(chunk, score) for score, _, chunk in scored[:k]]

    def _score_one(self, pos: int, query_tf: Counter, total_docs: int) -> float:
        index = self._index
        tf = index.term_freqs[pos]
        if not tf:
            return 0.0
        doc_len = index.doc_lengths[pos]
        score = 0.0
        for term, q_count in query_tf.items():
            df = index.doc_freqs.get(term, 0)
            if df == 0:
                continue
            term_tf = tf.get(term, 0)
            if term_tf == 0:
                continue
            normalization = index.k1 * (1.0 - index.b + index.b * doc_len / index.avg_doc_len)
            score += (
                _idf(df, total_docs)
                * term_tf
                * (index.k1 + 1.0)
                / (term_tf + normalization)
                * q_count
            )
        return score
