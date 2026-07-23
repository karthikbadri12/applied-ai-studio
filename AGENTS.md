# AGENTS.md — Applied AI Enterprise

This is the cross-tool entry point. **Claude Code** reads the native agent files in
`.claude/agents/`; **Cursor, VS Code agents, Antigravity, and Codex** read *this*
file (the `AGENTS.md` standard). Same system, one source of truth.

## What this repo is
A domain-agnostic **Applied-AI agent system** that takes an executive problem
statement and drives it through the full AI Development Life Cycle (ADLC) — from a
one-line VP ticket to a funded, governed, production-ready delivery plan — then hands
a spec to a downstream coding pipeline. See `ARCHITECTURE.md`.

## The rules that bind every agent
Read and obey **`CONSTITUTION.md`** first. It is non-negotiable: the administrator is
human-final, evidence over assertion, ask before you build, safety/privacy for
regulated data, one recommended path, artifacts are the interface, traceability.

## How to run it (any IDE)
1. **Start with the orchestrator.** Drop in a problem statement:
   > "Our claims team is drowning — 40k FNOL calls/month, 6-min handle time. Can AI help?"
   Ask the orchestrator to run the ADLC pipeline. In Claude Code: it delegates to the
   subagents automatically. In Cursor/Antigravity: follow the orchestrator role in
   `.claude/agents/orchestrator.md` and invoke the stage agents in order.
2. **The pipeline (in order):** intake → process-map → assess → value-prop →
   architecture → dev-spec → data-science → eval → poc-gate → production →
   observability → brief. Each writes a file into `artifacts/`.
3. **Advisors are consulted, not run in sequence:** `model-selector`, `cloud-gcp`,
   `cloud-aws`, `cloud-azure`, `cloud-onprem`, `connector-advisor`, `domain-advisor`.
4. **Human gates stop the pipeline.** When you see the `⛔ HUMAN GATE` block, a person
   must approve before it advances (PRD sign-off, funding, POC GO/NO-GO, launch).
5. **The dev pipeline is separate** (`pipelines/dev-pipeline.md`): once the AI Spec is
   approved + funded, run `discovery → coder → code-reviewer`.

## The agent roster
Defined in `registry/agents.json`; each agent's full brief is in `.claude/agents/*.md`.
- **Orchestrator (1):** `orchestrator`
- **Pipeline (12):** `intake`, `process-map`, `assess`, `value-prop`, `architecture`,
  `dev-spec`, `data-science`, `eval`, `poc-gate`, `production`, `observability`, `brief`
- **Advisors (7):** `model-selector`, `cloud-gcp`, `cloud-aws`, `cloud-azure`,
  `cloud-onprem`, `connector-advisor`, `domain-advisor`
- **Dev pipeline (3):** `discovery`, `coder`, `code-reviewer`

## Skills & methodology (Spec Kit · BMAD · Superpowers)
Every agent carries **required skills** combining Spec Kit's phase gates, BMAD's
personas, and Superpowers' composable skills — see `SKILLS.md` and
`registry/skills.json`. Before acting as any agent, load the skills listed in that
agent's *Skills & methodology* section (`.claude/skills/<name>/SKILL.md`).

## Install (per IDE)
Full instructions in `docs/INSTALL.md` — Claude Code (native custom agents), Cursor,
VS Code Copilot, Antigravity, Windsurf. Includes a 2-minute smoke test.

## Connectors
`connectors/` holds the catalog + an MCP config (`mcp.example.json`) that works across
Claude Code, Cursor, and Antigravity. Secrets never live in the repo.

## Coding conventions (for the dev pipeline)
- Read a file/framework before editing it — a target repo may diverge from your priors.
- Match the target repo's existing patterns; new code should read like it was always there.
- Never hardcode a secret. Never send regulated data to a model the architecture
  artifact didn't approve. Never mark a story done on a red eval gate.
