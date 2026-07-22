# The Dev Pipeline (decoupled)

The 12-stage ADLC spine is about **deciding what to build and whether to build it**.
The dev pipeline is about **building it**. They are deliberately separate pipelines
joined by a single artifact: the **AI Spec** (`artifacts/06-ai-spec.md`).

```
   ADLC SPINE (planning)                    │  DEV PIPELINE (building)
   intake → … → dev-spec → … → brief        │  discovery → coder → code-reviewer
                    │                        │      ▲
                    └──── AI Spec ───────────┼──────┘
                                             │  trigger: spec approved + funded
```

## Why decoupled

1. **You often plan without building.** Many initiatives should die at `poc-gate` or
   never get funded. Coupling planning to code wastes engineering on unfunded ideas.
2. **Different owners, different cadence.** Planning is FDE/PM/sponsor work; building
   is engineering work. The handoff is the AI Spec, not a shared branch.
3. **The spec is the contract.** `discovery`, `coder`, and `code-reviewer` all build
   and check against `06-ai-spec.md`. Scope not in the spec goes *back* to `dev-spec`
   — it never leaks into the code.

## The trigger

The dev pipeline does **not** auto-start. The orchestrator starts it only when:
- `artifacts/06-ai-spec.md` is approved, **and**
- the initiative is funded (`value-prop` case approved, `poc-gate` = GO/CONDITIONAL).

## The three stages

| Stage | Agent | Input | Output |
|-------|-------|-------|--------|
| 1 | `discovery` | AI Spec + brief + target repo | `artifacts/dev/backlog.md` (codebase map + ranked stories) |
| 2 | `coder` | one backlog story at a time | code + tests + wired eval gate |
| 3 | `code-reviewer` | the coder's diff | review report + MERGE / CHANGES REQUESTED |

Loop stages 2–3 per story until the backlog slice is done and the eval gate is green.

## What carries over from the spine

- **Model strategy** — from `architecture` / `model-selector` (routing + fallback).
- **Connectors** — from `connector-advisor` (MCP config, auth, scopes).
- **Guardrails & HITL points** — from `dev-spec` and `process-map`.
- **Eval gate** — from `eval`; `code-reviewer` blocks merge on a red gate.
- **Controls** — regulated-data controls from `architecture`; `code-reviewer`
  verifies no regulated data reaches an unapproved model.

The dev pipeline never re-decides the plan. If reality forces a change, it routes the
change back to the owning spine agent, keeps the artifacts the source of truth, and
resumes.
