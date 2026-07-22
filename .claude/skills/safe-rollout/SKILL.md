---
name: safe-rollout
description: Release discipline — canary, rollback trigger, launch-blocker checklist, nothing ships on a red gate or open blocker. Use in production and deployer contexts.
---
# Safe rollout (BMAD: Release/DevOps · Superpowers: verification-before-completion)
1. No ship unless the eval gate is green and the POC gate verdict allows it.
2. Rollout = canary/cohort/ramp + a named rollback trigger + a runbook.
3. Every launch blocker has an owner and a status; open blocker = no launch.
4. State the rollback plan before shipping, not after the incident.
