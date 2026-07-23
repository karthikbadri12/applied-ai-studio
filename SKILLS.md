# SKILLS.md: The Combined Methodology Layer

Every agent in this pack carries **required skills** drawn from three agentic-SDLC
frameworks, combined into one discipline. The mapping is machine-readable in
`registry/skills.json`; the skills themselves live in `.claude/skills/<name>/SKILL.md`;
each agent's file ends with its own **Skills & methodology** section.

## The three frameworks (and how they combine here)

| Framework | Methodology | What this pack takes from it |
|-----------|-------------|------------------------------|
| **Spec Kit** | Constitution → Specify → Clarify → Plan → Tasks → Implement | The **phase-gate spine**. Our CONSTITUTION.md is the Constitution phase; the PRD/AI Spec are Specify; assess is Clarify; architecture is Plan; backlogs are Tasks. Specs are the primary artifact — nothing implements against an unapproved spec. |
| **BMAD** | Analyst → PM → Architect → Scrum Master → Dev → QA | The **persona pipeline**. Every agent declares its BMAD persona and hands its artifact down the line, exactly as BMAD's 12-persona method prescribes. |
| **Superpowers** | Brainstorm → Spec → Approval → Plan → Test-driven execution | The **composable skills**. Socratic brainstorming before any artifact, written plans before any build, test-first everything — packaged as skills that agents load before acting. |

*(OpenSpec's fluid propose→design→tasks loop is the sanctioned lightweight mode for
single-stage runs, see `registry/skills.json → frameworks.openspec`.)*

## The 14 skills

| Skill | From | Used by |
|-------|------|---------|
| `socratic-brainstorm` | Superpowers brainstorm · BMAD Analyst | intake |
| `writing-a-spec` | Spec Kit /specify | intake, dev-spec, brief |
| `clarify-then-commit` | Spec Kit clarify | process-map, assess, domain-advisor |
| `breaking-down-work` | Spec Kit /tasks · BMAD SM | process-map, dev-spec, discovery |
| `planning-before-coding` | Spec Kit /plan · Superpowers write-plan | architecture, cloud-*, discovery |
| `evaluating-options` | Constitution Art. 5 | orchestrator, assess, architecture, model-selector, cloud-* |
| `business-case-math` | BMAD PM/Analyst | value-prop, model-selector |
| `test-first-verification` | Superpowers TDD · BMAD QA | eval, poc-gate, code-reviewer |
| `test-driven-implementation` | Superpowers TDD · BMAD Dev | data-science, coder |
| `reviewing-a-diff` | BMAD Senior Dev/QA | poc-gate, code-reviewer |
| `safe-rollout` | BMAD Release/DevOps | production |
| `observability-first` | BMAD SRE | observability |
| `wiring-integrations` | contract-first integration | connector-advisor, coder |
| `immutable-audit-trail` | BMAD Compliance/Risk | orchestrator, production, brief, domain-advisor |

## How skills activate

- **In Claude Code:** the skills in `.claude/skills/` are discoverable; the orchestrator
  injects each delegated agent's required skills (from `registry/skills.json`) into its
  delegation, Superpowers-style.
- **In Cursor / Antigravity / VS Code:** the assistant acting as an agent reads that
  agent's *Skills & methodology* section and loads each linked SKILL.md before acting.
- **Standalone:** running any single agent, read its skill files first, they carry the
  discipline (ask-first, spec-first, test-first, audit-always) that the Constitution
  enforces globally.

## The stage → Spec Kit phase map

```
Constitution   CONSTITUTION.md + orchestrator + domain-advisor
Specify        intake (PRD) · dev-spec (AI Spec)
Clarify        process-map · assess · value-prop
Plan           architecture · model-selector · cloud-gcp/aws/azure/onprem
Tasks          eval (sets & bars) · dev-spec handoff · discovery backlog
Implement      data-science · production · observability · coder → code-reviewer
Phase gates    sponsor PRD sign-off · finance case · POC GO/NO-GO · security launch · owner brief
```
