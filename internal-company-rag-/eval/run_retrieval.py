"""Run the retrieval evaluation.

Usage:
    python -m eval.run_retrieval [--set KEY=VALUE ...] [--out FILE.json]

Section 1 (quality): intentional, labeled CONTROL run on answerable golden
questions with the role filter disabled (allowed_labels=None) so the raw
retriever is isolated. Doc-level hit@1/3/5, recall@5 and MRR are computed over
the top-k CHUNK list, per type and overall.

Section 2 (access): for every role times every answerable question:
- leaks_with_filter: queries whose filtered top-k contains a forbidden chunk
  (must stay 0). Any nonzero value exits with code 1.
- queries_leaking_without_filter: CONTROL for comparison only.
- authorized_questions: queries whose every gold doc is readable by the role;
  filtered hit rates are reported on this subset.

--set overrides config values by dotted path (e.g. chunking.strategy=fixed).
Every reported number comes from this run; nothing is estimated.
"""

import argparse
import json
from collections import defaultdict

from src.cli import DEFAULT_CONFIG_PATH
from src.retrieval.access import allowed_labels
from src.retrieval.factory import build_retriever, load_chunks
from src.utils.config import load_config

HIT_LIMIT = 5


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eval.run_retrieval", description=__doc__.splitlines()[0])
    parser.add_argument("--set", dest="overrides", action="append", default=[],
                        metavar="KEY=VALUE", help="override a config value by dotted path")
    parser.add_argument("--out", default=None, help="write the JSON summary to this file")
    args = parser.parse_args(argv)

    cfg = _apply_overrides(load_config(DEFAULT_CONFIG_PATH), args.overrides)
    chunks = load_chunks(cfg)
    retriever = build_retriever(cfg, chunks)
    top_k = cfg["retrieval"]["top_k"]
    doc_labels = {chunk.doc_id: chunk.access_label for chunk in chunks}
    items = _load_answerable(cfg["data"]["golden_path"])
    print(f"chunks loaded: {len(chunks)} | golden questions (answerable): {len(items)}")
    print("overrides applied:", args.overrides or "none")
    print()

    summary = {"config": {"overrides": args.overrides, "top_k": top_k},
               "chunks_loaded": len(chunks), "quality": {}, "access": {}}

    quality = _evaluate_quality(retriever, items, top_k)
    summary["quality"] = quality
    print("## Section 1: quality (CONTROL: role filter disabled)")
    print(_quality_table(quality, top_k))

    access, leak_counts = _evaluate_access(retriever, items, cfg["roles"], doc_labels, top_k)
    summary["access"] = access
    print()
    print("## Section 2: access")
    print(_access_table(access, top_k))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as file:
            json.dump(summary, file, indent=2, sort_keys=True)
        print(f"\nwrote summary to {args.out}")

    if any(count > 0 for count in leak_counts.values()):
        print("FAIL: leaks_with_filter is nonzero for at least one role")
        return 1
    print("OK: leaks_with_filter is 0 for every role")
    return 0


def _apply_overrides(cfg: dict, overrides: list[str]) -> dict:
    for override in overrides:
        path, sep, raw_value = override.partition("=")
        if not sep:
            raise ValueError(f"invalid --set value, expected KEY=VALUE: {override!r}")
        keys = path.split(".")
        node = cfg
        for key in keys[:-1]:
            node = node[key]
        try:
            node[keys[-1]] = json.loads(raw_value)
        except json.JSONDecodeError:
            node[keys[-1]] = raw_value
    return cfg


def _load_answerable(path: str) -> list[dict]:
    items = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            item = json.loads(line)
            if item.get("source_docs"):
                items.append(item)
    return items


def _evaluate_quality(retriever, items: list[dict], top_k: int) -> dict:
    per_type: dict[str, dict[str, float]] = defaultdict(lambda: {
        "n": 0, "hit1": 0, "hit3": 0, "hit5": 0, "recall_sum": 0.0, "mrr_sum": 0.0})
    for item in items:
        gold = set(item["source_docs"])
        results = retriever.search(item["question"], top_k, None)
        doc_ids = [chunk.doc_id for chunk, _ in results]
        gold_found = {doc_id for doc_id in doc_ids if doc_id in gold}
        mrr = 0.0
        for rank, doc_id in enumerate(doc_ids, start=1):
            if doc_id in gold:
                mrr = 1.0 / rank
                break
        recall = len(gold_found) / len(gold) if gold else 0.0
        for qtype in (item["type"], "ALL"):
            bucket = per_type[qtype]
            bucket["n"] += 1
            _bump_hits(bucket, gold, doc_ids, top_k)
            bucket["recall_sum"] += recall
            bucket["mrr_sum"] += mrr
    rows = {}
    for qtype, bucket in per_type.items():
        n = bucket["n"]
        rows[qtype] = {
            "n": n,
            "hit@1": bucket["hit1"] / n if n else 0.0,
            "hit@3": bucket["hit3"] / n if n else 0.0,
            "hit@5": bucket["hit5"] / n if n else 0.0,
            "recall@5": bucket["recall_sum"] / n if n else 0.0,
            "mrr": bucket["mrr_sum"] / n if n else 0.0,
        }
    return rows


def _bump_hits(bucket: dict, gold: set, doc_ids: list[str], top_k: int) -> None:
    for k in (1, 3, HIT_LIMIT):
        if doc_ids[: min(k, top_k)]:
            if set(doc_ids[: min(k, top_k)]) & gold:
                bucket[f"hit{k}"] += 1


def _evaluate_access(retriever, items: list[dict], roles_cfg: dict, doc_labels: dict, top_k: int):
    rows: dict[str, dict] = {}
    leak_counts: dict[str, int] = {}
    for role in sorted(roles_cfg):
        labels = allowed_labels(role, roles_cfg)
        readable_docs = {doc_id for doc_id, label in doc_labels.items() if label in labels}
        leaks_with = 0
        leaks_without = 0
        authorized = 0
        auth_hits = {1: 0, 3: 0, HIT_LIMIT: 0}
        for item in items:
            gold = set(item["source_docs"])
            filtered = retriever.search(item["question"], top_k, labels)
            if any(chunk.access_label not in labels for chunk, _ in filtered):
                leaks_with += 1
            unfiltered = retriever.search(item["question"], top_k, None)
            if any(chunk.access_label not in labels for chunk, _ in unfiltered):
                leaks_without += 1
            if gold <= readable_docs:
                authorized += 1
                doc_ids = [chunk.doc_id for chunk, _ in filtered]
                for k in (1, 3, HIT_LIMIT):
                    if set(doc_ids[: min(k, top_k)]) & gold:
                        auth_hits[k] += 1
        leak_counts[role] = leaks_with
        denominator = authorized if authorized else 1
        rows[role] = {
            "leaks_with_filter": leaks_with,
            "control_leaks_without_filter": leaks_without,
            "authorized_questions": authorized,
            "authorized_hit@1": auth_hits[1] / denominator if authorized else 0.0,
            "authorized_hit@3": auth_hits[3] / denominator if authorized else 0.0,
            "authorized_hit@5": auth_hits[HIT_LIMIT] / denominator if authorized else 0.0,
        }
    return rows, leak_counts


def _quality_table(quality: dict, top_k: int) -> str:
    header = "| type | n | hit@1 | hit@3 | hit@5 | recall@5 | MRR |"
    lines = [header, "|---|---|---|---|---|---|---|"]
    for qtype in sorted(quality):
        row = quality[qtype]
        lines.append(
            f"| {qtype} | {row['n']} | {_pct(row['hit@1'])} | {_pct(row['hit@3'])} | "
            f"{_pct(row['hit@5'])} | {_pct(row['recall@5'])} | {_pct(row['mrr'])} |"
        )
    return "\n".join(lines)


def _access_table(access: dict, top_k: int) -> str:
    header = ("| role | leaks_with_filter | control leaks_without_filter "
              "| authorized_questions | hit@1 | hit@3 | hit@5 |")
    lines = [header, "|---|---|---|---|---|---|---|"]
    for role in sorted(access):
        row = access[role]
        lines.append(
            f"| {role} | {row['leaks_with_filter']} | {row['control_leaks_without_filter']} | "
            f"{row['authorized_questions']} | {_pct(row['authorized_hit@1'])} | "
            f"{_pct(row['authorized_hit@3'])} | {_pct(row['authorized_hit@5'])} |"
        )
    return "\n".join(lines)


def _pct(value: float) -> str:
    return f"{value:.3f}"


if __name__ == "__main__":
    raise SystemExit(main())
