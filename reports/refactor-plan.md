# Refactor & Enhancement Plan

1. **Introduce dependency management**
   - *Rationale*: tests fail due to missing `pandas` and no requirements file.
   - *Files*: add `requirements.txt` or `pyproject.toml` with core libs.
   - *Tests*: rerun `pytest` to confirm imports.
   - *Rollback*: remove the file if incompatibilities arise.

2. **Consolidate tests and remove debug scripts**
   - *Rationale*: root-level test files and debug scripts clutter repository.
   - *Files*: move stray `test_*.py` into `tests/`, archive or delete `debug_*.py`.
   - *Tests*: execute full `pytest` suite to ensure paths updated.
   - *Rollback*: restore original files if necessary.

3. **Apply Ruff autofixes and configure linting**
   - *Rationale*: 31 lint errors indicate style inconsistencies.
   - *Files*: fix reported issues, optionally add `.ruff.toml` for configuration.
   - *Tests*: `ruff check .` should pass; run `pytest` for safety.
   - *Rollback*: revert individual files if behavior changes.

4. **Strengthen typing with mypy**
   - *Rationale*: 14 type errors and missing `pandas-stubs`.
   - *Files*: annotate variables like `bloco`, adjust defaults to use `Optional`.
   - *Tests*: `mypy src` and `pytest` to ensure compatibility.
   - *Rollback*: revert specific annotations if they introduce runtime issues.

5. **Modularize `data_loader` and improve coverage**
   - *Rationale*: large monolithic module is high risk.
   - *Files*: split `data_loader.py` into smaller modules (e.g., `wab_loader`, `c6_loader`).
   - *Tests*: add unit tests for each new module.
   - *Rollback*: keep original `data_loader.py` available until parity confirmed.
