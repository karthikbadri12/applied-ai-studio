## What & why

<!-- What changes, and what problem it solves. Link an issue if one exists. -->

## Which layer

- [ ] Agent spec (`.claude/agents/`)
- [ ] Skill (`.claude/skills/`)
- [ ] Registry (`registry/*.json`)
- [ ] Governance docs (Constitution / Harness / Quality bar / Governance / Evals / Disaster command)
- [ ] CLI (`src/aidlc_studio/`)
- [ ] Exemplar (`exemplar/claims-idp/`)
- [ ] Docs / site (`docs/`, `README.md`)

## Checklist

- [ ] All `registry/*.json` are valid JSON and consistent with each other
      (an added/renamed agent appears in `agents.json`, `skills.json`, `phases.json`)
- [ ] Exemplar tests green — `python3 -m unittest discover -s tests`
- [ ] Exemplar evals green — `python3 evals/run_evals.py` exits 0, all bars PASS
- [ ] `QUALITY_BAR.md` respected (quantified claims, labelled numbers, no unsourced assertions)
- [ ] No secrets, credentials, or real customer data anywhere — env-var **names** only
- [ ] Cloud/platform facts verified as current (product names change often here)
- [ ] `pyproject.toml` version bumped if the CLI or packaged pack changed
- [ ] Human gates still cannot be bypassed automatically

## Behaviour change to the pipeline?

<!-- Does this change what an agent does, what an artifact must contain, or when the
     pipeline stops? If yes, say exactly how — this is the part reviewers care about. -->

- [ ] No behaviour change (docs/refactor only)
- [ ] Behaviour changes, described above

## Breaking change?

- [ ] No
- [ ] Yes — describe migration for existing installs (`aidlc init --global --force`, etc.)
