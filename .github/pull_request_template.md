## What
- Short summary

## Why
- Problem / user story / ticket link

## How
- Key implementation notes (DB changes? env vars? feature flags? K8s?)

## Risk / Rollback
- Impact & rollback plan if needed

## Tests
- [ ] Unit tests added/updated (or N/A)
- [ ] Local run OK (`uvicorn app.main:app --reload`)
- [ ] FastAPI /docs verified

## Approvals needed (informational)
- Dev code → **backend-leads**
- CI/K8s/infra → **devops-leads**
- Prod config (if applicable) → **platform**

## Ops / Release
- [ ] No breaking API change
- [ ] DB migrations handled (if any)
- [ ] K8s/Helm values updated (if needed)
- [ ] CI (CodeBuild) green
