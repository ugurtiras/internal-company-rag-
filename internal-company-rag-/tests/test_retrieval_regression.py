"""Regression gate over the real corpus and golden set.

Quality thresholds (ALL hit@5 >= 0.95, MRR >= 0.90) come from the assignment
brief; they must be re-checked (and lowered if needed) once the real baseline
is measured on this machine. ASSUMPTION: role-label mapping is the one in
config.yaml, pending confirmation.
"""

import json
from pathlib import Path

import pytest

from src.cli import DEFAULT_CONFIG_PATH
from src.retrieval.access import allowed_labels
from src.retrieval.factory import build_retriever, load_chunks
from src.utils.config import load_config

REPO_ROOT = Path(__file__).resolve().parents[1]
GOLDEN_PATH = REPO_ROOT / "eval" / "golden_qa.jsonl"

CROSS_ROLE = "destek"
CROSS_QUESTION = "SLA ihlalinde tazminat oranı nasıl belirlenir?"
CROSS_FORBIDDEN_DOC = "HUK-003"

HIT5_THRESHOLD = 0.95
MRR_THRESHOLD = 0.90


@pytest.fixture(scope="module")
def setup() -> tuple:
    cfg = load_config(str(REPO_ROOT / DEFAULT_CONFIG_PATH))
    chunks = load_chunks(cfg)
    retriever = build_retriever(cfg, chunks)
    doc_ids = {chunk.doc_id for chunk in chunks}
    doc_labels = {chunk.doc_id: chunk.access_label for chunk in chunks}
    gold = _load_answerable_golden(GOLDEN_PATH)
    return cfg, chunks, retriever, doc_ids, doc_labels, gold


def _load_answerable_golden(path: Path) -> list[dict]:
    items = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            item = json.loads(line)
            if item["source_docs"]:
                items.append(item)
    return items


def test_golden_source_docs_exist_in_corpus(setup) -> None:
    _, _, _, doc_ids, _, gold = setup
    missing = {doc for item in gold for doc in item["source_docs"]} - doc_ids
    assert missing == set()


def _quality_row(setup) -> tuple[float, float]:
    cfg, _, retriever, _, _, gold = setup
    top_k = cfg["retrieval"]["top_k"]
    hit5 = 0
    mrr_sum = 0.0
    for item in gold:
        gold_set = set(item["source_docs"])
        results = retriever.search(item["question"], top_k, None)
        doc_ids = [chunk.doc_id for chunk, _ in results]
        if set(doc_ids[: min(5, top_k)]) & gold_set:
            hit5 += 1
        for rank, doc_id in enumerate(doc_ids, start=1):
            if doc_id in gold_set:
                mrr_sum += 1.0 / rank
                break
    n = len(gold)
    return hit5 / n, mrr_sum / n


def test_all_hit5_and_mrr_meet_thresholds(setup) -> None:
    hit5, mrr = _quality_row(setup)
    # Thresholds per assignment brief; adjust only with a measured baseline.
    assert hit5 >= HIT5_THRESHOLD, f"hit@5 {hit5:.3f} < {HIT5_THRESHOLD}"
    assert mrr >= MRR_THRESHOLD, f"MRR {mrr:.3f} < {MRR_THRESHOLD}"


def test_no_role_leaks_forbidden_chunks(setup) -> None:
    cfg, _, retriever, _, _, gold = setup
    top_k = cfg["retrieval"]["top_k"]
    for role in sorted(cfg["roles"]):
        labels = allowed_labels(role, cfg["roles"])
        for item in gold:
            results = retriever.search(item["question"], top_k, labels)
            offending = [chunk for chunk, _ in results if chunk.access_label not in labels]
            assert offending == [], f"role {role} leaked {[c.doc_id for c in offending]}"


def test_cross_acl_support_cannot_read_huk003(setup) -> None:
    cfg, _, retriever, _, _, _ = setup
    top_k = cfg["retrieval"]["top_k"]
    labels = allowed_labels(CROSS_ROLE, cfg["roles"])
    results = retriever.search(CROSS_QUESTION, top_k, labels)
    doc_ids = [chunk.doc_id for chunk, _ in results]
    assert CROSS_FORBIDDEN_DOC not in doc_ids
    own = [doc_id for doc_id in doc_ids if doc_id.startswith("DST")]
    assert own, f"support found none of its own documents: {doc_ids}"
