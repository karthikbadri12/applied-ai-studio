# Contributing to Applied AI Enterprise

The unusual thing about this repo: **most of the "code" is Markdown.** Agents are
versioned specifications, not library code, which means a PR that changes agent
behaviour is reviewable by a product manager, a risk officer, or a delivery lead,
not just an engineer. Please keep it that way.

## Repo layout

```
CONSTITUTION.md      the rules every agent obeys (changes here are high-impact)
HARNESS.md           runtime enforcement: guardrails, gates, audit ledger
QUALITY_BAR.md       per-artifact definition of done + the build contract
GOVERNANCE.md        EU AI Act / NIST RMF / MRM crosswalk
EVALS.md             evaluation doctrine
DISASTER_COMMAND.md  incident command
.claude/agents/      the 25 agent specs (canonical source)
.claude/skills/      the 14 composable skills + the /appliedai entry point
registry/            agents · stages · phases · skills · frameworks (JSON)
artifacts/templates/ what each stage produces
exemplar/claims-idp/ the gold-standard worked example + working codebase
src/aidlc_studio/    the `aidlc` CLI (stdlib-only Python)
```

## Adding an agent

1. Write `.claude/agents/<id>.md`. YAML frontmatter (`name`, `description`, and
   `model` only if it genuinely needs a specific tier), then: role intro, what you
   do, outputs, guardrails, and the **Skills & methodology** footer.
2. Register it in **all three**:
   - `registry/agents.json`: id, type, layer, file, artifact/advises
   - `registry/skills.json`: BMAD persona, Spec Kit phase, required skills
   - `registry/phases.json`: which phase it acts or is consulted in
3. If it produces an artifact, add the template to `artifacts/templates/` and a
   stage-specific floor row to `QUALITY_BAR.md`.
4. Run `python3 -m src.aidlc_studio.cli list` (or `aidlc list`), your agent should
   appear with its persona and phase.

**Agent-writing conventions:** one job per agent. Say what it is *not* responsible
for. Guardrails are specific and testable ("MUST cite the artifact it read"), never
aspirational ("should be helpful"). Advisors recommend and never act.

## Adding a skill, domain, or connector

- **Skill** → `.claude/skills/<name>/SKILL.md` with `name` + `description`
  frontmatter; reference it from the agents that require it and add it to
  `registry/skills.json`.
- **Domain** → a pack under `domains/` plus an entry in `domains/index.json`:
  regulations, data classes, typical sources, mandatory HITL points.
- **Connector** → `connectors/catalog.json` + a config block in
  `connectors/mcp.example.json`. **Env-var names only; never a credential value,
  not even a fake-looking one.**

## Before you open a PR

```bash
# 1. registries must be valid JSON
for f in registry/*.json aidlc.config.example.json; do python3 -c "import json,sys;json.load(open('$f'))"; done

# 2. the exemplar must stay green
cd exemplar/claims-idp/build
python3 -m unittest discover -s tests     # 34 tests
python3 evals/run_evals.py                # 7 bars, all PASS, exit 0
```

Both must pass. The exemplar is the repo's proof, a red exemplar means the pitch
doesn't work.

## Standards

- **The quality bar applies to documentation too.** Quantified claims, labelled
  numbers, no marketing adjectives. If you can't source it, don't assert it.
- **Cloud/platform facts must be current and verified.** Product names in this
  space change often (Vertex AI → Gemini Enterprise Agent Platform, Azure AI
  Foundry → Microsoft Foundry). Check before you write, and cite where practical.
- **Conventional commits**: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.
- **Versioning**: bump `pyproject.toml` when the CLI or the packaged pack changes;
  PyPI never accepts the same version twice.
- **No secrets, ever**: not in code, artifacts, examples, tests, or fixtures.

## What gets rejected

- Agents that overlap an existing agent's charter (split or extend instead).
- Guardrails that can't be checked.
- Artifact templates that don't state their input contract and output artifact.
- Anything that lets the pipeline advance past a human gate automatically.
- Fabricated benchmark numbers or unverifiable vendor claims.
