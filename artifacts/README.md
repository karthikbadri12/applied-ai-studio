# artifacts/

The stage agents write their outputs here, using the matching template in
`templates/`. The artifact of stage N is the input contract of stage N+1.

```
01-prd.md            ← intake        (signed PRD)
02-process-map.md    ← process-map
03-assessment.md     ← assess        (solution verdict + model shortlist)
04-business-case.md  ← value-prop
05-architecture.md   ← architecture
06-ai-spec.md        ← dev-spec      (the dev-pipeline contract)
07-data-science.md   ← data-science
08-evals.md          ← eval
09-poc-gate.md       ← poc-gate      (GO / CONDITIONAL / NO-GO)
10-production.md     ← production
11-observability.md  ← observability
12-delivery-brief.md ← brief         (capstone)
dev/backlog.md       ← discovery     (dev pipeline)
```

One run = one set of numbered files here. For multiple concurrent initiatives, put
each in a subfolder (`artifacts/<initiative-slug>/`).
