"""Tests for the web UI request handlers (pure logic, no socket or Flask)."""

import pytest
from pathlib import Path

from src.retrieval.access import UnknownRoleError
from src.retrieval.bm25 import Bm25Retriever, build_index
from src.utils.config import load_config
from src.web.app import handle_ask, handle_roles

REPO_ROOT = Path(__file__).resolve().parents[1]


def chunk(doc_id: str, label: str, text: str):
    from src.chunking.chunker import Chunk

    return Chunk(
        chunk_id=f"{doc_id}#0", doc_id=doc_id, title="t", access_label=label, section="s", text=text
    )


def const_cfg() -> dict:
    return {
        "web": {"host": "127.0.0.1", "port": 8000, "max_k": 10, "max_question_chars": 500},
        "retrieval": {"top_k": 5},
        "roles": {
            "destek": ["tum_calisanlar", "destek"],
            "hukuk": ["tum_calisanlar", "hukuk"],
        },
    }


def toy_retriever():
    chunks = [
        chunk("HUK-003", "hukuk", "SLA kredi tazminat oranları"),
        chunk("DST-001", "destek", "SLA kredi talep süreci"),
    ]
    return Bm25Retriever(build_index(chunks, k1=1.5, b=0.75, stem_prefix=0))


def test_roles_payload_lists_every_role() -> None:
    cfg = load_config(str(REPO_ROOT / "config.yaml"))
    payload = handle_roles(cfg)
    roles = [entry["role"] for entry in payload["roles"]]
    assert roles == sorted(cfg["roles"])
    yonetim = next(entry for entry in payload["roles"] if entry["role"] == "yonetim")
    assert len(yonetim["labels"]) == 9


def test_ask_unknown_role_is_rejected() -> None:
    retriever = toy_retriever()
    body = {"role": "misafir", "question": "tazminat oranı"}
    with pytest.raises(UnknownRoleError):
        handle_ask(const_cfg(), retriever, body)


def test_ask_empty_question_is_rejected() -> None:
    with pytest.raises(ValueError):
        handle_ask(const_cfg(), toy_retriever(), {"role": "destek", "question": "   "})


def test_ask_k_is_clamped() -> None:
    retriever = toy_retriever()
    body = {"role": "destek", "question": "SLA kredi", "k": 99}
    payload = handle_ask(const_cfg(), retriever, body)
    assert payload["k"] == 10
    body = {"role": "destek", "question": "SLA kredi", "k": 0}
    payload = handle_ask(const_cfg(), retriever, body)
    assert payload["k"] == 1


def test_ask_results_stay_inside_role_labels() -> None:
    payload = handle_ask(const_cfg(), toy_retriever(), {"role": "destek", "question": "SLA kredi"})
    labels = set(payload["allowed_labels"])
    assert all(item["access_label"] in labels for item in payload["results"])
    assert all(item["doc_id"] != "HUK-003" for item in payload["results"])


def test_ask_respects_role_separation_like_cli_acceptance() -> None:
    retriever = toy_retriever()
    body = {"role": "destek", "question": "SLA tazminat kredi"}
    destek = handle_ask(const_cfg(), retriever, body)
    assert all(item["doc_id"] != "HUK-003" for item in destek["results"])
    assert destek["results"], "destek should still see its own documents"
    body = {"role": "hukuk", "question": "SLA tazminat kredi"}
    hukuk = handle_ask(const_cfg(), retriever, body)
    assert hukuk["results"][0]["doc_id"] == "HUK-003"
