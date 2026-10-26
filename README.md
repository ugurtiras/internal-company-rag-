# Internal Company RAG

Internal document assistant (RAG) with role-based access control.
Demo corpus: synthetic documents of the fictional company "Penguin Cloud".

## Quickstart
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
pytest
ruff check . && ruff format --check .
```

## Layout
| Path | Purpose |
|---|---|
| `src/ingestion/` | Load documents |
| `src/chunking/` | Split text into chunks |
| `src/embeddings/` | Text to vectors |
| `src/vectordb/` | Vector DB operations |
| `src/retrieval/` | Similarity search with access filtering |
| `src/prompts/` | Prompt templates |
| `src/llm/` | LLM client |
| `src/api/` | API endpoints |
| `src/utils/` | Shared helpers |
| `tests/` | Unit and integration tests |
| `data/raw/` | Synthetic documents (versioned) |
| `eval/` | Golden set and evaluation scripts |
| `docs/` | Experiments log and ADRs |
| `config.yaml` | All tunable settings |
| `docs/adr/` | Architecture decision records |
| `docs/experiments.md` | Experiment log |

## Demo

Web UI (standard library only, no extra dependencies):

```bash
python -m src.web
# open http://127.0.0.1:8000
```

Same question, three roles — support can not see the legal compensation policy,
legal can:

```bash
python -m src.cli ask --role destek "SLA ihlalinde tazminat oranı nasıl belirlenir?"
python -m src.cli ask --role hukuk "SLA ihlalinde tazminat oranı nasıl belirlenir?"
python -m src.cli ask --role yonetim "SLA ihlalinde tazminat oranı nasıl belirlenir?"
python -m src.cli roles
```

Evaluation (role filter on for access checks; the quality section is a labeled
CONTROL run with the filter disabled to isolate the retriever):

```bash
python -m eval.run_retrieval                      # baseline (section + BM25, stem 5)
python -m eval.run_retrieval --set retrieval.bm25.stem_prefix=0   # E-002
python -m eval.run_retrieval --set chunking.strategy=fixed        # E-005
python -m eval.run_retrieval --out results.json
```

Optional dense retrieval (needs a model download on first run):

```bash
pip install -r requirements-dense.txt
python -m eval.run_retrieval --set retrieval.type=dense
```

