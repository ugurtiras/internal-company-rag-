"""Command-line interface for role-scoped retrieval over the internal corpus."""

import argparse

from src.retrieval.access import allowed_labels
from src.retrieval.factory import build_retriever, load_chunks
from src.utils.config import load_config

PREVIEW_CHARS = 160
DEFAULT_CONFIG_PATH = "config.yaml"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="src.cli", description="Internal company RAG CLI")
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH, help="path to config.yaml")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("roles", help="list roles and the access labels they read")

    ask = subparsers.add_parser("ask", help="ask a question as a role")
    ask.add_argument("--role", required=True)
    ask.add_argument("question")
    ask.add_argument("-k", type=int, default=None, help="number of chunks to return")

    args = parser.parse_args(argv)
    cfg = load_config(args.config)

    if args.command == "roles":
        _run_roles(cfg)
        return 0
    if args.command == "ask":
        return _run_ask(args, cfg)
    parser.error(f"unknown command: {args.command}")  # pragma: no cover
    return 2


def _run_roles(cfg: dict) -> None:
    roles_cfg = cfg["roles"]
    for role in sorted(roles_cfg):
        labels = ", ".join(sorted(allowed_labels(role, roles_cfg)))
        print(f"{role}: {labels}")


def _run_ask(args: argparse.Namespace, cfg: dict) -> int:
    labels = allowed_labels(args.role, cfg["roles"])
    chunks = load_chunks(cfg)
    retriever = build_retriever(cfg, chunks)
    top_k = args.k if args.k is not None else cfg["retrieval"]["top_k"]
    results = retriever.search(args.question, top_k, labels)

    print(f"role: {args.role}")
    print(f"allowed labels: {', '.join(sorted(labels))}")
    if not results:
        print("No accessible source found.")
        return 0
    for rank, (chunk, score) in enumerate(results, start=1):
        preview = " ".join(chunk.text.split())[:PREVIEW_CHARS]
        print(
            f"{rank}. [{chunk.doc_id}] {chunk.section} | {chunk.access_label} | "
            f"{score:.4f} | {preview}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
