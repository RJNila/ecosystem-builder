# Contributing

## Branching & commits
- Trunk-based: branch off `main`, short-lived branches `feat/*`, `fix/*`, `chore/*`.
- Conventional Commits: `feat(org): create endpoint`, `fix(db): null check`, etc.

## Local dev
- Python 3.11; Postgres running locally.
- venv:
  - macOS/Linux: `python -m venv .venv && source .venv/bin/activate`
  - Windows: `.venv\Scripts\Activate.ps1`
- Install deps: `pip install -r requirements.txt`
- Env: create `.env.local` (see README).
- Run: `uvicorn app.main:app --reload --port 8000` → http://localhost:8000/docs

## Tests & quality
- Unit tests: `pytest -q`
- Lint (optional): `ruff check .` / `black --check .`

## Pull requests
- Open PR to `main` with the template filled; small and focused.
- CI must be green; approvals per CODEOWNERS (lead-only).
- Squash merge; delete branch.

## Releases
- Tag `main` with `vX.Y.Z` when user-visible changes ship.
