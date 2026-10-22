# Requirements-refinement agentic network (Task 1)

LangGraph network that turns a directory of heterogeneous documents (emails, meeting minutes,
interviews, surveys, draft specs) into one structured requirements specification.

## Setup

```powershell
python -m pip install -r requirements.txt
```

Create `.env` in this folder (it is git-ignored):

```
OPENAI_API_KEY=sk-...
```

## Run

```powershell
python main.py --input data/corpus --output output/requirements.md [--max-iterations 3]
```

The input directory is searched recursively for `.txt`, `.md` and `.eml` files.
Models can be overridden with the `EXTRACT_MODEL`, `CONSOLIDATE_MODEL` and `REVIEW_MODEL` environment variables.

## Files

| File | Purpose |
|---|---|
| `main.py` | CLI entry point, writes the output files |
| `graph.py` | LangGraph wiring (nodes, edges, feedback loop) |
| `nodes.py` | Node implementations and graph state |
| `prompts.py` | LLM system prompts and the priority scale |
| `schemas.py` | Pydantic models for structured LLM output |
| `config.py` | Model assignment and tuning constants |
| `REPORT.md` | Design report |
| `output/requirements.md` | Generated requirements document |
| `output/*.json`, `output/graph.mmd` | Intermediate artifacts and graph diagram |
