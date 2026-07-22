---
name: wiring-integrations
description: Integration discipline — contract-first, catalog-only, least-privilege, recommendation-vs-invocation kept separate. Use in connector-advisor and custom API work.
---
# Wiring integrations (BMAD: Integration/DevOps · contract-first)
1. Only recommend connectors from the catalog (connectors/catalog.json); one-line rationale each.
2. Advisors recommend; they never invoke. Execution happens in the dev pipeline, scoped.
3. Least privilege: read-only default, named schemas/tables only, secrets in a manager.
4. Validate against the declared contract/schema; regulated data masked AT the source.
