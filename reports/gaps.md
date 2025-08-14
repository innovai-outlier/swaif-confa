# Gap Analysis

| Gap | Evidence | Suggested remedy | Effort | Risk |
| --- | --- | --- | --- | --- |
| No declared dependencies | No `requirements*` or `pyproject.toml` found | Add `requirements.txt` or `pyproject.toml` listing packages like `pandas` | M | M |
| Tests fail to import `pandas` | `pytest -q` raised `ModuleNotFoundError` for `pandas` | Ensure dependencies installed before running tests | S | H |
| Lint violations | `ruff check .` reported 31 errors (`F541`, `E402`, etc.) | Address lint findings or adopt formatter | M | M |
| Type check failures | `mypy src` reported 14 errors and missing `pandas` stubs | Add type annotations and install type stubs | M | M |
| No CI pipeline | No `.github/workflows` directory present | Introduce CI to run tests, lint, and types | S | M |
| Debug/legacy scripts in repo | Files like `debug_direto.py`, `debug_pipeline.py` present in root | Move to tooling directory or remove if obsolete | S | L |
| Large, multi-purpose modules | `src/models/data_loader.py` ~270+ lines | Break into focused modules with tests | L | M |
