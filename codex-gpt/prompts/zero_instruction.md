# Codex Operational Instruction — `swaif-confa` (Python MVC)

## Mission
Codex handles **all operational tasks** for the `innovai-outlier/swaif-confa` repository.  
Our discussions here define *what* to build (strategy/tactics). Codex’s job is to execute those tactical steps inside the repo.

---

## Repo Context
- Language: Python 3.11+
- Architecture: MVC
  - Models: `swaif_confa/models/`
  - Controllers: `swaif_confa/controllers/`
  - Views: `swaif_confa/views/` (CLI now, Streamlit later)
- Testing: `pytest`
- Linting/formatting: `ruff`
- Type-checking: `mypy`
- CI: GitHub Actions
- README: in pt-BR — preserve content unless instructed otherwise.

---

## Codex Role
Codex **must**:
1. Implement code, config, and file changes as directed by tactics.
2. Keep MVC layers separated; models/controllers must be UI-agnostic.
3. Ensure all changes:
   - Pass `pytest`, `ruff check .`, and `mypy swaif_confa`.
   - Respect PR title format: `[swaif-confa] <Title>`.
   - Follow commit conventions: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
4. Write/update tests for all new features or fixes.
5. Update CI only when needed to support new code or tests.

Codex **must not**:
- Make architectural or roadmap changes without new tactical instruction.
- Translate/rewrite the README without request.
- Commit code that breaks CI.

---

## Operational Loop
1. **Receive** tactical instruction from strategy/tactics discussion.
2. **Plan** a minimal set of changes to fulfill it.
3. **Apply** changes in small, reversible commits.
4. **Verify**:
   - Run `pytest -q`
   - Run `ruff check .`
   - Run `mypy swaif_confa`
5. **Commit & PR**:
   - Atomic commit with message matching conventions.
   - PR title as `[swaif-confa] <Title>`.

---

## Quality Bar
- Clean, typed Python code.
- Test coverage for new/changed behavior.
- No failing tests, lint errors, or type errors.
- Minimal impact: avoid touching unrelated files.

---

**Note:** This file is an *operational manual* for Codex, not a strategy document.


---

# Contributor Guide

## Dev Environment Tips
- Use pnpm dlx turbo run where <project_name> to jump to a package instead of scanning with ls.
- Run pnpm install --filter <project_name> to add the package to your workspace so Vite, ESLint, and TypeScript can see it.
- Use pnpm create vite@latest <project_name> -- --template react-ts to spin up a new React + Vite package with TypeScript checks ready.
- Check the name field inside each package's package.json to confirm the right name—skip the top-level one.

## Testing Instructions
- Find the CI plan in the .github/workflows folder.
- Run pnpm turbo run test --filter <project_name> to run every check defined for that package.
- From the package root you can just call pnpm test. The commit should pass all tests before you merge.
- To focus on one step, add the Vitest pattern: pnpm vitest run -t "<test name>".
- Fix any test or type errors until the whole suite is green.
- After moving files or changing imports, run pnpm lint --filter <project_name> to be sure ESLint and TypeScript rules still pass.
- Add or update tests for the code you change, even if nobody asked.

## PR instructions
Title format: [<project_name>] <Title>













