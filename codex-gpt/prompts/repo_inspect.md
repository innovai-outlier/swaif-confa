# TD‑001 (Revised) — Inspect & Adapt Baseline Before Changes

**Goal**  
Before touching code, Codex will inventory the existing repository structure, conventions, and quality gates, run initial checks, and produce a short **Refactor/Enhancement Plan**. Any scaffolding or config is **added only if missing**, never destructively overwriting current choices.

---

## Operating Principles

1. **Non‑destructive first**: detect what exists; only add what’s missing.
2. **Match the repo’s style**: mirror file layout, naming, typing style, and test layout already in use.
3. **Evidence‑based plan**: propose changes based on findings (tests, lint, types, dead code), not assumptions.
4. **Small, reversible steps**: split subsequent work into atomic PRs with green checks.

---

## Scope (Codex executes)

### A) Recon & Inventory
- Generate a concise tree of source files (depth 2–3) and test dirs.
- Extract current tooling:
  - Python version(s)
  - Test runner(s)
  - Linters/formatters
  - Type checker(s)
  - CI workflows
- Parse `pyproject.toml` / `setup.cfg` / `requirements*.txt` / `Makefile` / `noxfile.py` if present.
- Detect MVC alignment: where Models, Controllers, and Views live.

**Deliverable:** `reports/inventory.md` containing:
- Repo tree (trimmed)
- Tools & versions found
- Scripts/entry points
- Current CLI/UI entry paths
- Quick dependency highlights

### B) Health Checks
Run what exists; if a tool is missing, **skip** and note it (do not add yet).
- Tests: run the repo’s existing test command(s) or `pytest -q` if available.
- Lint: run existing linter(s).
- Types: run existing type checker(s).
- Optional metrics (if quick): test duration, test count, coverage flag presence.

**Deliverable:** `reports/health.md` with:
- Commands executed and exit codes
- Summaries of failures (first 20 lines per failure)
- Lint/type highlights (top categories)

### C) Gap Analysis
- Identify missing safeguards (e.g., no tests, no lint, no typing, no CI).
- Identify mismatches (e.g., CLI logic mixed into controllers, view bleed into models).
- Locate dead code (simple heuristics) and highest‑risk areas (flaky tests, large files, no tests).

**Deliverable:** `reports/gaps.md` with a table:
- Gap | Evidence | Suggested remedy | Effort (S/M/L) | Risk (L/M/H)

### D) Minimal Additions (only if missing)
Add these **only when absent**, placing them to match repo conventions:
- `reports/` directory (for the artifacts above).
- `.github/workflows/ci.yml` that runs the repo’s existing test/lint/type steps **if they already exist**; otherwise it comments “step skipped; tool not detected”.
- If no test exists at all, add a **single** smoke test that imports the main entry point to catch import errors (no behavior changes).

### E) Refactor/Enhancement Plan
Produce `reports/refactor-plan.md` that proposes a **short, sequenced plan** (3–7 steps), each as a tiny PR with:
- Goal & rationale
- File(s) touched
- Tests to add/adjust
- Rollback notes

---

## Acceptance Criteria

- No destructive edits; existing configs and code style are respected.
- The following files are created/updated:
  - `reports/inventory.md` (clear current state)
  - `reports/health.md` (commands, outcomes, summaries)
  - `reports/gaps.md` (table with remedies)
  - `reports/refactor-plan.md` (3–7 atomic steps)
  - `.github/workflows/ci.yml` **only if** missing, and it conditionally runs tools that exist
  - A single smoke test **only if** no tests exist
- If CI already exists, it remains unmodified in this PR.
- README remains untouched.
- PR is small and fully reversible.

---

## Commands (suggested; adapt to repo)

> Codex should discover and prefer the repo’s own commands. If unknown, try these safely and record results.

```bash
# tests
pytest -q || echo "pytest not available or failing"

# lint
ruff check . || echo "ruff not available or failing"

# types
mypy swaif_confa || echo "mypy not available or failing"

# tree (trimmed)
python - <<'PY'
import os
def walk(root='.'):
    for d,_,fs in os.walk(root):
        depth=d.count(os.sep)
        if depth>3 or any(p in d for p in ('.venv','__pycache__','build','dist','.git')):
            continue
        print(d)
        for f in fs:
            if f.endswith(('.py','.toml','.yml','.yaml','.ini','.cfg','Makefile','noxfile.py')):
                print('  -', f)
walk('.')
PY
```

---

## Commit & PR

- **Commit message:** `chore: add repo inventory & health reports; minimal CI/test only if missing`
- **PR Title:** `[swaif-confa] TD‑001 — Inspect repo & generate plan (no destructive changes)`

---

## Follow‑ups (will become TD‑002+ after review)

- Apply one linter or formatter consistently (only if repo lacks one).
- Strengthen typing in high‑value modules (mypy gates).
- Untangle MVC boundaries if leakage is found.
- Replace ad‑hoc logging with a structured logger.
- Add Streamlit view or polish CLI—**without** altering controllers/models.
