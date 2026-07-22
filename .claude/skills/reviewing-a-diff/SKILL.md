---
name: reviewing-a-diff
description: Reviewer discipline — verify the diff against the spec and guardrails, not taste. Use in code-reviewer and poc-gate: every acceptance criterion checked, every guardrail violation flagged, verdict explicit.
---
# Reviewing a diff (BMAD: Senior Dev/QA · Superpowers: review)
1. Review against the SPEC: every acceptance criterion verified, drift flagged.
2. A specced-but-absent guardrail/HITL control is a BLOCKER, never a nit.
3. Findings ranked: blockers / should-fix / nits, each with file:line + failure scenario.
4. Explicit verdict: MERGE or CHANGES REQUESTED. Never rewrite — send back.
