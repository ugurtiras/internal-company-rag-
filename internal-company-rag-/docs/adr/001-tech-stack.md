# ADR-001: Technology stack

## Context
Internal document assistant (RAG) over Turkish documents with role-based access control.
Constraints: no mandated technology, 16 GB RAM, no GPU, privacy matters (internal documents),
experiments must be reproducible and comparable.

## Decision
| Layer | Choice | Alternatives considered |
|---|---|---|
| Language | Python 3.11+ | - |
| Orchestration | Plain Python, no framework | LangChain, LlamaIndex |
| Vector DB | Qdrant (local mode first, Docker server in M5) | ChromaDB, FAISS |
| Embedding | Local multilingual model, configurable (start: intfloat/multilingual-e5-base) | API embeddings |
| LLM | Local via Ollama (OpenAI-compatible API), configurable | Hosted APIs |
| API | CLI first, then FastAPI | - |
| Evaluation | Own scripts (hit rate, MRR, faithfulness) | RAGAS (only if justified by measurement) |
| Config | config.yaml + .env | - |

## Rationale
- Qdrant: metadata filtering at search time (required for access control), Docker-ready, in-memory mode for fast tests.
- Local LLM and embeddings: documents never leave the machine; model versions are pinned, so experiments are reproducible.
- Plain Python: each pipeline stage is explicit and defensible in the thesis.
- Components that will be compared (chunking, embedding model, top-k, LLM) are config-driven; the rest stays fixed to avoid needless abstraction.

## Consequences
- CPU-only inference is slow; LLM size is limited to small quantized models.
- Changing embedding model or chunking requires re-indexing; collection names include model and chunk settings.
- LLM and embedding providers sit behind small interfaces so a hosted API can be added later.