---
name: writing-a-spec
description: Spec Kit-style specification writing — the spec is the primary artifact, not the code. Use when producing the PRD or the AI Spec. Every field testable, acceptance criteria explicit, approved before implementation.
---
# Writing a spec (Spec Kit: /speckit.specify · BMAD: PM)
1. Specifications are the primary artifact; code serves the spec.
2. Every field must be testable — if you can't write an eval for it, it's underspecified.
3. Explicit acceptance criteria, always. "Ship when metric ≥ X AND p95 < Ys."
4. Never invent requirements the user never stated (hard guardrail).
5. Phase gate: the spec is APPROVED (human gate) before any downstream work starts.
