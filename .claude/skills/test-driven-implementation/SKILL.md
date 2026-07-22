---
name: test-driven-implementation
description: Coder discipline — a story is done only when its eval case passes in CI. Use in coder and data-science: red → green against the spec's acceptance criteria, guardrails wired, no secrets.
---
# Test-driven implementation (Superpowers: TDD · BMAD: Developer)
1. Read the story's acceptance criteria + eval case before writing anything.
2. Build the smallest thing that satisfies them; match the repo's conventions.
3. Done = eval case passes + CI eval gate green + tests written + zero secrets in the diff.
4. Log experiments (data-science): what changed, score, cost/latency, keep/kill.
