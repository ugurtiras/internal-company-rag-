# Experiments Log

Important: this project is currently developed in an offline sandbox without
PyYAML/pytest and without PyPI access. The numbers below come from an offline
reproduction that ran the SAME chunker/BM25 code over the real corpus and the
real golden set, parsing front matter with a tiny handmade parser
(`run_real_corpus_smoke.py` / `run_experiments_offline.py`, outputs captured).
They are NOT yet confirmed by `python -m eval.run_retrieval` in a proper
environment; run that command before defending these numbers. No number here is
estimated; all are command output.

## Quality experiments

Baseline: section chunking + BM25 (k1 1.5, b 0.75), top_k 5, doc-level metrics
over top-k chunks; filterless (labeled CONTROL) on the 176 answerable golden
questions.

| Date | ID | Change | Config | hit@1 | hit@5 | recall@5 | MRR | Decision |
|---|---|---|---|---|---|---|---|---|
| 2026-10-21 | E-001 | baseline | section, stem_prefix 5 | 0.920 | 1.000 | 0.973 | 0.955 | keep as baseline (defaults) |
| 2026-10-21 | E-002 | disable stemming | section, stem_prefix 0 | 0.898 | 0.977 | 0.938 | 0.932 | worse on every metric; keep stem 5 |
| 2026-10-21 | E-003 | shorter stem | section, stem_prefix 4 | 0.915 | 0.989 | 0.958 | 0.945 | worse than stem 5 |
| 2026-10-21 | E-004 | longer stem | section, stem_prefix 6 | 0.932 | 0.994 | 0.955 | 0.957 | hit@1 +0.012 but hit@5 drops; differences are a few questions — not meaningful; keep stem 5 |
| 2026-10-21 | E-005 | fixed chunking | fixed 500/100, stem_prefix 5 | 0.926 | 1.000 | 0.969 | 0.957 | close to baseline; section keeps structure (section names in chunks) → keep section |
| 2026-10-21 | E-006 | fixed + no stem | fixed 500/100, stem_prefix 0 | 0.881 | 0.983 | 0.962 | 0.926 | clearly worse; confirms stem 5 |
| 2026-10-21 | E-007 | dense (E5) | retrieval.type=dense | not measured | not measured | not measured | not measured | model download blocked in sandbox; not measured, not estimated |

## Access experiments

Same retriever, role filter applied before ranking for every role x every
answerable question (176). `leaks_with_filter` counts queries whose filtered
top-k contains a forbidden chunk and MUST stay 0 (eval exits 1 otherwise).
`control leaks without filter` shows what the same retriever would leak when the
filter is disabled (the labeled CONTROL in the eval script).

| Role | leaks_with_filter | control leaks without filter | authorized questions | authorized hit@5 |
|---|---|---|---|---|
| calisan | 0 | 162 | 57 | 57/57 (1.000) |
| destek | 0 | 151 | 73 | 73/73 (1.000) |
| finans | 0 | 162 | 57 | 57/57 (1.000) |
| hukuk | 0 | 161 | 64 | 64/64 (1.000) |
| ik | 0 | 157 | 63 | 63/63 (1.000) |
| muhendis | 0 | 124 | 107 | 107/107 (1.000) |
| satis | 0 | 155 | 70 | 70/70 (1.000) |
| yonetim | 0 | 0 | 176 | 176/176 (1.000) |

Cross-ACL check (the acceptance scenario): "SLA ihlalinde tazminat oranı nasıl
belirlenir?" asked as `destek` returns DST-007 chunks and never HUK-003; asked
as `hukuk` it returns HUK-003 chunks.

## Caveats

- Small corpus (30 docs, 176 answerable questions) whose questions reuse the
  documents' own wording; hit@5 is likely saturated (1.000 for several configs).
  Differences of a few questions between stem variants are not meaningful.
- The stem_prefix comparison used the same golden set as the baseline: there is
  no hold-out, so these numbers describe the golden set, not true generalization.
- Dense and hybrid retrieval were not measured (model download unavailable in
  the sandbox); no number was invented for them.
- The role-to-label mapping is an assumption pending confirmation (see
  ADR 002 and config.yaml).
- All quality rows were produced by the offline reproduction described above;
  confirm each row with `python -m eval.run_retrieval --set ... --out ...` in a
  proper environment before citing numbers to others.
