# Changelog

## [Unreleased]
- Repo skeleton (M0)
- config: full config.yaml with data/chunking/retrieval/roles sections and a `load_config` util
- chunking: section and fixed strategies (frozen `Chunk`, per-doc ids, access label inheritance)
- retrieval: access decisions in `allowed_labels`, BM25 retriever with pre-ranking filtering
- retrieval: optional dense retriever with encoder protocol (sentence-transformers, lazy import)
- cli: `python -m src.cli ask|roles` with role-scoped output
- web: standard-library-only web UI (`python -m src.web`) reusing the same
  pre-ranking access filter; unknown role or empty question -> HTTP 400
- eval: quality (labeled CONTROL, filterless) and access sections; exit 1 on any leak
- tests: unit tests for chunker/bm25/dense/config/access plus real-data regression gate
- devops: pinned runtime/dev requirements, GitHub Actions CI, docs (ADR 002, experiments log)
