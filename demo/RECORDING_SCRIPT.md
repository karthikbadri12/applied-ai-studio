# Demo Recording Script — 7 minutes

Audience: a hiring manager or enterprise buyer who has seen a hundred AI demos and
is bored of all of them. The differentiator is not that it generates something —
it's that it **refuses to skip the boring parts** and can prove its work.

**Core narrative:** *"Everyone can demo a model. This demos the delivery discipline —
and it stops for a human at every decision that matters."*

---

## Scene 0 · Pre-flight (do this before recording)

- [ ] `uvx --from aidlc-studio aidlc init --global` already run; VS Code reloaded
- [ ] A **fresh empty folder** open (`~/demo-fnol`) — no prior artifacts
- [ ] Terminal font ≥ 16pt; editor zoom up one step; hide bookmarks bar
- [ ] Browser tabs pre-opened: PyPI page · GitHub repo · `docs/index.html`
- [ ] The exemplar pre-verified in a second terminal tab:
      `cd ~/Downloads/applied-ai-studio/exemplar/claims-idp/build && make test && make eval`
- [ ] Notifications off (macOS Focus). Close Slack/Mail.
- [ ] **Fallback ready:** the exemplar artifacts already exist — if anything live
      stalls, cut to Scene 4 and narrate from the finished artifacts. Never wait
      on screen for a slow generation; talk over it or cut.

---

## Scene 1 · The hook (0:00 – 0:45)

**Screen:** `docs/index.html` hero, then the PyPI page.

> "Most AI initiatives die one of three deaths: nobody defined the problem, nobody
> could prove it worked, or nobody thought about production until it broke.
>
> I encoded the discipline that prevents all three. It's called AIDLC — twenty-five
> agents, four phases, five human gates. It's open source, it's on PyPI, and it
> installs into any IDE with one command."

**Type:**
```bash
uvx --from aidlc-studio aidlc init --global
```

> "That's it. Now every project I open has the whole delivery org chart in it."

---

## Scene 2 · It asks before it builds (0:45 – 2:15)

**Screen:** empty `~/demo-fnol` folder in VS Code, Claude Code panel open.

**Type:**
```
/appliedai Our consumer wireless care team handles 2 million contacts a quarter.
Average handle time is 11 minutes, first-contact resolution is 62%, and agents
toggle between six systems. Can AI help?
```

> "Watch what it does *not* do. It doesn't start writing code."

**When the batched questions appear — pause, and point at them:**

> "It's asking me eleven numbered questions before it will produce anything. What's
> the success metric. Where does ground truth live. What can the agent never do
> autonomously. Which cloud. Which connectors, and the credential environment
> variable names — never the secrets themselves.
>
> This is the single biggest reason AI projects fail, and it's the part every demo
> skips."

**Answer on camera** (say them as you type):
- Cloud: **GCP**
- Connectors: **Snowflake** (env vars pending)
- Mode: **plan**

---

## Scene 3 · The human gate (2:15 – 3:30)

**Screen:** `artifacts/01-prd.md` appears in the file tree — open it.

> "A PRD, written to disk. Success metric with a baseline and a target. A stakeholder
> map. A cost model with the arithmetic shown — because 'high labour cost' isn't a
> number a CFO can act on."

**Scroll to the gate message in chat.**

> "And then it stops. ⛔ Human gate — the sponsor signs the PRD. It will not advance
> on an unsigned PRD. There are five of these: PRD, funding, go/no-go, security
> launch, and the final brief.
>
> An AI system that won't stop for a human isn't a product. It's a liability."

**Type in chat:** `approved`

> "Now it continues — and every cloud advisor runs in parallel."

---

## Scene 4 · Decision-grade artifacts (3:30 – 5:00)

**Screen:** switch to `~/Downloads/applied-ai-studio/exemplar/claims-idp/artifacts/`

> "Rather than watch a full run, here's one already finished — a P&C insurer's
> claims intake, carried end to end. Twelve artifacts."

**Open `05-architecture.md`, scroll to the cloud table:**

> "Four cloud advisors were asked the *same* question, so this is like-for-like:
> GCP, AWS, Azure, on-prem. One winner — and the reasons the other three lost are
> on the record. Below it, the PII controls matrix: every data class, its control,
> and who verified it."

**Open `08-evals.md`:**

> "Seven metric bars, each derived from the business need *before* anything was
> measured. Hallucination rate is a pass/fail safety gate — it never gets averaged
> away against accuracy."

**Open `metrics.json` briefly:**

> "And it's all machine-readable — stage timings, gate approvers, eval scores. This
> is what a governance review actually asks for."

---

## Scene 5 · The money shot (5:00 – 6:30)

**Screen:** terminal in `exemplar/claims-idp/build`.

> "It doesn't just plan. Build mode produces a working repository."

**Type:**
```bash
make demo
```
> "Full pipeline — classify, extract, validate, confidence-gate, route, audit. Note
> the low-confidence case falling back to the stronger model, and the prompt
> injection getting quarantined instead of executed."

**Type:**
```bash
make eval
```
> "Seven bars. All green. Forty-eight cases — golden, adversarial, regression.
>
> And notice they're **not** a hundred percent. Ninety-seven point nine on
> classification, ninety-two on extraction F1. The fixtures have deliberate defects
> in them, because a demo that scores perfectly is a demo that's lying.
>
> Zero credentials. This just ran on your laptop with no API key — that's why it can
> run in CI on every pull request. Red bar, no merge."

---

## Scene 6 · Close (6:30 – 7:15)

**Screen:** `docs/index.html`, scroll the end-to-end section.

> "Twenty-five agents, four phases, five human gates, twelve artifacts and an
> append-only audit ledger.
>
> One design decision I'd call out: there's no agent framework underneath this. The
> agents are versioned Markdown specs, so the whole org chart is reviewable in a
> pull request by someone who doesn't write code, and it runs on whatever agentic
> runtime the IDE already has — Claude Code, Cursor, Copilot, Antigravity.
>
> The framework decision belongs to the *solution*, not the tooling. That's why the
> cloud advisor recommends ADK on Google, Strands on AWS, Agent Framework on Azure.
>
> It's on GitHub and PyPI. Install it and point it at your ugliest problem."

**End on the repo URL.**

---

## Delivery notes

- **Pace:** slow down on the gate (Scene 3) and the eval table (Scene 5). Those are
  the two moments a senior buyer leans in. Everything else can move.
- **Don't read the screen aloud.** Say what it *means*.
- **Own the imperfect numbers.** Volunteering that the scores aren't 100% and
  explaining why buys more credibility than any feature.
- **If something stalls:** keep talking, cut to the exemplar, come back. Never
  narrate dead air.
- **Record 1080p minimum**, mic close, one take per scene — assemble after. Scene 5
  is worth re-taking until the terminal output is clean.
- Have a 60-second cut ready: Scene 2 questions → Scene 3 gate → Scene 5 evals.
  That's the whole story if someone only watches a minute.
