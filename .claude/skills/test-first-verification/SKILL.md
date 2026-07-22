---
name: test-first-verification
description: Superpowers test-first discipline applied to AI — set the bar BEFORE measuring, build golden/adversarial/regression sets, wire a CI gate that blocks on regression. Use in eval and poc-gate.
---
# Test-first verification (Superpowers: TDD · BMAD: QA)
1. Set the metric bar from the business need FIRST; then measure against it.
2. Three sets: golden (common path), adversarial (designed to break it), regression (never again).
3. Safety metrics are pass/fail gates, never averaged away.
4. An adversarial set that finds nothing is too weak — strengthen it.
5. Clear PASS/FAIL verdict; no vibes ("the demo looked great" is not evidence).
