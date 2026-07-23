# PRODUCT.md — vision, roadmap, and how decisions get made

**Vision:** make disciplined AI delivery the path of least resistance — so that
doing it properly is faster than cutting corners.

This file is the product layer: who it's for, what we're optimising, what ships
next, and how that's decided. It follows the same rule as every other artifact —
claims carry numbers, and priorities carry their scoring.

---

## Personas

| Persona | Their problem today | What AIDLC gives them |
|---|---|---|
| **Forward-deployed engineer / delivery lead** | Every engagement restarts the same discovery, architecture, and governance work from scratch | A repeatable lifecycle with the artifacts pre-shaped; the estate review and 4-cloud comparison done in an afternoon, not a fortnight |
| **PM / BA** | Hands over a brief that engineering reinterprets; can't tell whether the AI actually works | The Socratic intake loop, a signed PRD with a real success metric, and eval results in language they can take to a sponsor |
| **Platform / ML engineer** | Ambiguous requirements; evals bolted on at the end | An unambiguous, testable AI Spec and a CI eval gate from day one |
| **Executive sponsor** | Funds initiatives that look great in demo and stall in security review | A business case with auditable arithmetic, five decision points they control, and a launch-blocker list with owners |
| **Risk / compliance** | Discovers the AI system at the end, with no evidence trail | A contemporaneous, append-only evidence pack mapped to EU AI Act tiers and NIST AI RMF |

## What we optimise for

1. **Time-to-first-artifact** — a useful PRD within one working session of a
   problem statement.
2. **Artifact defensibility** — an artifact survives hostile questions in a C-suite
   or governance review without a follow-up meeting.
3. **Proof over assertion** — the exemplar runs green, keyless, on any laptop.
4. **Zero lock-in** — Markdown specs and MCP; no framework dependency to install,
   version, or secure.

Explicitly **not** optimising for: agent count, model benchmark scores, or
low-code UI surface. Those are vanity.

## OKRs — next two quarters

**O1 · Practitioners can adopt it without a conversation**
- KR1.1 Install → first artifact in under 10 minutes, verified on all 5 IDEs
- KR1.2 `aidlc check` passes on a clean machine for every IDE flavour (currently: 5/5)
- KR1.3 INSTALL.md has a verify + troubleshoot step per IDE (done)

**O2 · Artifacts hold up in front of a governance function**
- KR2.1 Every stage has a documented quality floor in `QUALITY_BAR.md` (12/12)
- KR2.2 Governance crosswalk published for EU AI Act + NIST AI RMF + MRM (done)
- KR2.3 A second worked exemplar in a different domain and solution class (telecom, agentic) — *open*

**O3 · The proof stays true**
- KR3.1 Exemplar tests + evals green in CI on every PR (34 tests, 7 bars)
- KR3.2 Cloud/platform facts re-verified at least quarterly (last: 2026-07)
- KR3.3 Zero secrets in repo history — enforced by review

## Roadmap (RICE-scored)

*Reach 1–10 (share of users touched) · Impact 0.25–3 · Confidence 0–1 · Effort in person-days. Score = R×I×C/E.*

| # | Item | R | I | C | E | **Score** | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Telecom exemplar** (agentic solution class, second domain) | 8 | 3 | 0.9 | 5 | **4.3** | Next |
| 2 | **Trusted-publishing CI** (tag → PyPI, no tokens) | 6 | 2 | 0.95 | 2 | **5.7** | Next |
| 3 | **Connector test harness** (verify an MCP connector before the build depends on it) | 7 | 2.5 | 0.8 | 6 | **2.3** | Planned |
| 4 | **Per-domain golden-set starter packs** | 6 | 2 | 0.7 | 8 | **1.1** | Planned |
| 5 | **GOVERNANCE deep integrations** (export the evidence pack to GRC formats) | 4 | 2 | 0.6 | 10 | **0.5** | Backlog |
| 6 | **A2A interop demo** (AIDLC-designed agent talking to a partner agent) | 3 | 2 | 0.6 | 8 | **0.45** | Backlog |
| 7 | **Windsurf-native flavour** (beyond the AGENTS.md path) | 3 | 1 | 0.7 | 4 | **0.53** | Backlog |

Sequencing note: #2 ships before #1 because it removes a manual, credential-handling
step from every future release — small effort, compounding return.

## Release policy

- **Semantic versioning.** Patch = docs/fixes. Minor = new agents, skills, or
  registry fields (backward-compatible). Major = a change to the Constitution, the
  gate model, or the artifact contract.
- **PyPI** (`aidlc-studio`) on every minor+; a version is never republished.
- **Global installs update** with `aidlc init --global --force`.
- **Breaking changes** require a migration note in the PR and the release notes.

## Success metrics & feedback

| Signal | Source | Why |
|---|---|---|
| Installs | PyPI download stats | Reach; the only usage number we have |
| Issues by layer | GitHub labels (agent / CLI / docs / IDE) | Where the friction is |
| "It didn't ask questions" reports | Issues | The canary — means the Constitution didn't load in that IDE |
| Exemplar CI status | GitHub Actions | The proof, continuously |
| Community exemplars | PRs | The strongest adoption signal there is |

**Privacy-first:** the CLI collects **no telemetry** — no phone-home, no analytics,
no install beacon. It scaffolds files and exits. Feedback comes from GitHub, which
means we see less, and that's the correct trade for a tool that runs inside
enterprise repos.

## Principles for saying no

- If it lets the pipeline skip a human gate, no.
- If it requires credentials to demonstrate value, no.
- If it adds an agent whose charter overlaps an existing one, extend instead.
- If it can't be reviewed in a pull request by a non-engineer, reconsider the design.
