"""Role-scoped retrieval web UI, built on the standard library only.

The server reuses the exact same retrieval path as the CLI: the role filter is
applied before scoring and no bypass exists here either. Request bodies are
JSON; unknown roles and invalid input fail with HTTP 400 (never default access).

Run with:
    python -m src.web [--host HOST] [--port PORT]

Then open http://127.0.0.1:8000 in a browser.
"""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from src.retrieval.access import allowed_labels
from src.retrieval.factory import build_retriever, load_chunks
from src.utils.config import load_config

STATIC_DIR = Path(__file__).resolve().parent / "static"


def handle_roles(cfg: dict) -> dict:
    """List roles with their reachable labels plus retrieval defaults."""
    roles_cfg = cfg["roles"]
    return {
        "roles": [
            {"role": role, "labels": sorted(allowed_labels(role, roles_cfg))}
            for role in sorted(roles_cfg)
        ],
        "default_top_k": cfg["retrieval"]["top_k"],
    }


def handle_ask(cfg: dict, retriever, body: dict) -> dict:
    """Answer one ask request with the role filter enforced (no bypass flag)."""
    question = str(body.get("question", "")).strip()
    if not question:
        raise ValueError("question is required")
    if len(question) > cfg["web"]["max_question_chars"]:
        raise ValueError(f"question exceeds {cfg['web']['max_question_chars']} characters")

    role = str(body.get("role", ""))
    labels = allowed_labels(role, cfg["roles"])  # raises UnknownRoleError

    top_k = body.get("k", cfg["retrieval"]["top_k"])
    if not isinstance(top_k, int):
        raise ValueError("k must be an integer")
    top_k = min(cfg["web"]["max_k"], max(1, top_k))

    results = retriever.search(question, top_k, labels)
    items = [
        {
            "rank": rank,
            "chunk_id": chunk.chunk_id,
            "doc_id": chunk.doc_id,
            "section": chunk.section,
            "access_label": chunk.access_label,
            "score": round(score, 4),
            "snippet": " ".join(chunk.text.split())[:160],
        }
        for rank, (chunk, score) in enumerate(results, start=1)
    ]
    return {
        "role": role,
        "question": question,
        "k": top_k,
        "allowed_labels": sorted(labels),
        "results": items,
    }


def build_server(cfg: dict, retriever) -> ThreadingHTTPServer:
    """Create the HTTP server with the prepared application state attached."""

    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: int, body: bytes, ctype: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_json(self, status: int, payload: dict) -> None:
            data = json.dumps(payload).encode("utf-8")
            self._send(status, data, "application/json; charset=utf-8")

        def _static_file(self, name: str) -> None:
            path = STATIC_DIR / name
            if not path.is_file():
                self._send_json(404, {"error": "not found"})
                return
            ctype = {
                ".html": "text/html; charset=utf-8",
                ".css": "text/css; charset=utf-8",
                ".js": "text/javascript; charset=utf-8",
            }[path.suffix]
            self._send(200, path.read_bytes(), ctype)

        def do_GET(self) -> None:  # noqa: N802 - framework convention
            route = self.path.split("?", 1)[0]
            if route in ("/", "/index.html"):
                self._static_file("index.html")
            elif route == "/style.css":
                self._static_file("style.css")
            elif route == "/app.js":
                self._static_file("app.js")
            elif route == "/api/roles":
                self._send_json(200, handle_roles(Handler._cfg))
            else:
                self._send_json(404, {"error": "not found"})

        def do_POST(self) -> None:  # noqa: N802 - framework convention
            if self.path.split("?", 1)[0] != "/api/ask":
                self._send_json(404, {"error": "not found"})
                return
            try:
                body = json.loads(
                    self.rfile.read(int(self.headers.get("Content-Length", 0)) or 0)
                )
                if not isinstance(body, dict):
                    raise ValueError("request body must be a JSON object")
                payload = handle_ask(Handler._cfg, Handler._retriever, body)
                self._send_json(200, payload)
            except (ValueError, KeyError) as exc:
                self._send_json(400, {"error": str(exc)})

        def log_message(self, format: str, *args) -> None:  # noqa: A002, ARG002
            pass  # keep stdout clean for the demo

    Handler._cfg = cfg
    Handler._retriever = retriever
    return ThreadingHTTPServer((cfg["web"]["host"], cfg["web"]["port"]), Handler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="src.web", description="Internal RAG web UI")
    parser.add_argument("--host", default=None, help="override web.host from config")
    parser.add_argument("--port", type=int, default=None, help="override web.port from config")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args(argv)

    cfg = load_config(args.config)
    if args.host:
        cfg["web"]["host"] = args.host
    if args.port:
        cfg["web"]["port"] = args.port

    chunks = load_chunks(cfg)
    retriever = build_retriever(cfg, chunks)
    server = build_server(cfg, retriever)
    url = f"http://{cfg['web']['host']}:{cfg['web']['port']}"
    print(f"serving web UI on {url} (role filter enforced before ranking; Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
