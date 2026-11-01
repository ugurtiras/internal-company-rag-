# ADR 002: Retrieval baseline and access filtering

## Context

The assistant must answer questions over internal Penguin Cloud documents while
respecting role-based access: a user's role limits which documents the retriever
may ever surface. Trainees asked how the baseline should be implemented without
external frameworks and where access filtering has to happen.

## Options considered

1. Filter after ranking (retriever scores everything, drop unauthorized
   chunks/pieces afterwards). Simple, but unauthorized content influences the
   ranking and can push authorized results out of the top-k; any post-processing
   bug leaks content.
2. Filter before ranking (current choice). The scorer only ever sees chunks
   whose access label is allowed for the role; unauthorized chunks cannot occupy
   a top-k slot.
3. One index per role (or per label). Isolates indexes architecturally, but
   duplicates memory and lets roles with overlapping labels diverge when one
   index is rebuilt and the other is not.

## Decision

- Filter is applied BEFORE scoring (`src/retrieval/bm25.py:search`,
  `src/retrieval/dense.py:search`). Chunks outside `allowed_labels` are never
  scored.
- The only place an access decision is made is
  `src/retrieval/access.py:allowed_labels`; unknown roles raise
  `UnknownRoleError`, invalid labels in the config raise `ValueError`. There is
  no default-access fallback and no bypass flag in the CLI.
- A filterless mode exists only for the evaluation script, explicitly labeled
  CONTROL in `eval/run_retrieval.py`, to isolate retriever quality.
- Baseline: section chunking + BM25 (k1 1.5, b 0.75, stem_prefix 5) with no
  external dependencies; dense (E5) is an optional, config-driven path.

## Consequences

- Filtering correctness does not depend on reranking or scoring details.
- Corpus statistics (N, df) stay corpus-wide, so scores are stable across roles.
- The role-label mapping is an explicit assumption documented in `config.yaml`
  and must be confirmed by the project owner.
