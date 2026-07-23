# Google Cloud — full-stack service map for AI delivery

The knowledge base behind the `cloud-gcp` advisor. Organized by **architecture
layer**, so an architecture artifact names a concrete service at *every* layer —
not just "use Gemini." Each entry: what it is · when to choose it · what to watch.

> **Currency rule.** Google renames and consolidates fast (Vertex AI → Gemini
> Enterprise Agent Platform, Cloud Next 2026). Verified July 2026. The advisor
> **must** re-check with a web search before presenting, and flag anything marked
> *Preview* as not-yet-GA. Sources at the bottom.

---

## 0. The platform umbrella

**Gemini Enterprise Agent Platform** — announced at Cloud Next 2026 as the evolution
of **Vertex AI**, consolidated with **Agentspace** into one product. Say
*"Gemini Enterprise Agent Platform (formerly Vertex AI)"* on first mention; "Vertex
AI" alone is the pre-2026 name and dates you instantly.

Bundles: ADK (code-first) · Agent Studio (low-code) · Agent Engine (managed runtime)
· Model Garden (200+ models) · persistent memory · enterprise governance — pay-as-you-go.

---

## 1. Ingestion & data movement

| Service | Use it for | Watch for |
|---|---|---|
| **Cloud Storage (GCS)** | Landing zone for documents, images, audio, model artifacts | Lifecycle rules + retention are a governance requirement, not an optimisation |
| **Pub/Sub** | Event-driven ingestion, decoupling producers from the AI pipeline | At-least-once delivery — the pipeline must be idempotent |
| **Dataflow** | Streaming/batch transformation at scale (Apache Beam) | Heavier than needed for simple ETL; consider BigQuery-native first |
| **Datastream** | CDC from operational databases into BigQuery | Schema-drift handling must be explicit |
| **Cloud Composer** | Managed Airflow — orchestration for teams already on Airflow | If the estate has Airflow, this is the low-friction path (`stack-review` will find it) |
| **Storage Transfer Service / BigQuery Data Transfer** | Bulk migration, scheduled SaaS ingests | Check source connector coverage before committing |

## 2. Data platform & storage

| Service | Use it for | Watch for |
|---|---|---|
| **BigQuery** | The analytical core — and increasingly the *AI* core (see §5) | Slot/on-demand cost model drives most FinOps surprises |
| **BigQuery ML** | Train/serve classical ML **in SQL**, no data movement | Often beats a bespoke pipeline for tabular problems — always evaluate it before proposing Vertex training |
| **AlloyDB / Cloud SQL (PostgreSQL)** | Operational store; `pgvector` for embeddings alongside transactional data | Good when retrieval must be transactionally consistent with app state |
| **Spanner** | Global, strongly-consistent operational data | Usually overkill unless already in the estate |
| **Firestore** | App/session state, agent memory backing store | Model access patterns first |
| **Bigtable** | High-throughput, low-latency feature serving | Specialised — justify it |

## 3. Document & multimodal processing

| Service | Use it for | Watch for |
|---|---|---|
| **Document AI** | OCR, layout parsing, form/entity extraction, splitting mixed packets; **native BigQuery integration** | The right *pre-processor* before an LLM — cheaper and more reliable than asking a model to OCR |
| **Document AI Custom Extractor** | Domain-specific document types with training data | Needs labelled data — check the ground-truth inventory |
| **Speech-to-Text / Text-to-Speech** | Call recordings, IVR, voice agents | Diarisation and domain vocabulary matter more than headline WER |
| **Cloud Vision / Video Intelligence** | Image and video understanding outside the LLM path | Compare against Gemini multimodal — sometimes one model replaces both |
| **Translation** | Multilingual pipelines | Evaluate whether Gemini handles it natively first |

## 4. Models & model access

| Capability | What to name | Notes |
|---|---|---|
| **Model Garden** | 200+ foundation models in one catalog | Includes **Gemini 3.1 Pro / Flash**, open **Gemma 4**, and third-party incl. **Anthropic Claude** (Opus/Sonnet/Haiku), media models (e.g. Lyria) |
| **Routing cascade** | Flash for volume → Pro for hard/low-confidence cases | This is the single biggest cost lever; state it explicitly with the trigger condition |
| **Grounding with Google Search** | Freshness-dependent answers | Check data-egress policy before enabling in a regulated flow |
| **Provisioned Throughput** | Latency-sensitive production workloads | Capacity reservation vs pay-as-you-go is a FinOps decision, make it deliberately |
| **Batch prediction** | Offline scoring at volume | Materially cheaper than online — use it wherever latency isn't required |
| **Model tuning (supervised / distillation)** | Consistent domain behaviour a prompt can't reach | Only after prompt+RAG have been evaluated and found insufficient |

## 5. Retrieval & grounding (RAG)

| Service | Use it for | Watch for |
|---|---|---|
| **Vertex AI Search** (in Agent Builder) | Managed end-to-end RAG: ingests documents, BigQuery, websites, SharePoint, Salesforce; handles chunking, embedding, indexing; grounded answers **with citations** | Fastest path to a defensible RAG baseline — start here before building custom |
| **Vector Search** (2.0) | Custom, high-scale retrieval; **hybrid** vector + full-text + semantic re-ranking in one parallel query | Choose when you need control over chunking/ranking that the managed path won't give |
| **BigQuery vector search** | Semantic search **directly in the warehouse** — native vector support, embedding generation, vector index management | Excellent when the corpus already lives in BigQuery: no separate vector DB, no copy, governance inherited |
| **AlloyDB / pgvector** | Retrieval co-located with operational data | Transactional consistency with app state |
| **Ranking / re-ranking APIs** | Precision on top-k | Retrieval quality usually beats model upgrades for grounded accuracy |

**The architecture point worth making:** three legitimate retrieval homes —
warehouse-native (BigQuery), purpose-built (Vector Search), or operational
(AlloyDB). Naming *why* you picked one is the senior move.

## 6. Agents & orchestration

| Component | What it is | When |
|---|---|---|
| **ADK (Agent Development Kit)** | Open-source, code-first agent framework — **Python, TypeScript, Go, Java**; native **multi-agent** composition and delegation; build/debug/deploy | The default for engineering-owned agents |
| **Agent Studio** | Low-code visual agent builder | Business-user-owned agents, rapid prototyping |
| **Workspace Studio** | No-code agents inside Google Workspace | Workflow automation for knowledge workers |
| **Agent Engine (Agent Runtime)** | Managed runtime: scaling, sub-second cold starts, long-running agents, persistent memory | The production deploy target — say this, not "run it on Cloud Run," unless there's a reason |
| **A2A (Agent2Agent) v1.0** | Cross-vendor/framework agent interop | Multi-vendor estates; partner agents |
| **Managed MCP servers + Apigee** | Tool/API exposure to agents; Apigee as the API-to-agent bridge | The clean answer to "how does the agent reach our internal APIs safely" |
| **Partner agents** | Box, Workday, Salesforce, ServiceNow | Buy-before-build check |
| **Cloud Run / GKE** | Self-managed hosting when Agent Engine doesn't fit | Justify why managed didn't work |
| **Workflows / Cloud Tasks** | Deterministic orchestration around the agent | Not everything needs to be agentic — say so |

## 7. Enterprise integration

**Apigee** (API management + the agent bridge) · **Application Integration**
(connectors to SAP, Salesforce, ServiceNow, Workday) · **Eventarc** (event routing) ·
**BigQuery Omni / BigLake** (query across clouds, incl. data left in S3/Azure) ·
**Cortex Framework** (accelerators for SAP and other enterprise sources).

> The LLM↔deterministic-systems bridge lives here. When a solution must write back
> to SAP or Salesforce, name Apigee/Application Integration **and** the human
> approval step — never an unattended agent write to a system of record.

## 8. Classical ML & training

**Vertex AI Training** (custom jobs, distributed) · **Pipelines** (KFP-based MLOps) ·
**Feature Store** · **Model Registry** (versioning + lineage — the model-inventory
evidence in `GOVERNANCE.md`) · **Experiments** · **AutoML** · **TPUs/GPUs**.

Reminder from `assess`: if the problem is tabular, **BigQuery ML is often the right
answer** and the whole GenAI stack is unnecessary. Recommending the simpler thing is
a credibility move, not a weakness.

## 9. Evaluation & quality

| Capability | Use |
|---|---|
| **Gen AI evaluation service** | Model/prompt comparison against your metrics — wire it to the bars in `bars.yaml` |
| **Vertex Experiments** | Track the experiment log required by `07-data-science.md` |
| **Model Registry + lineage** | Which version produced which result — MRM evidence |
| **BigQuery as eval store** | Keep eval runs queryable and joinable to production outcomes |

Per `EVALS.md`: managed eval tooling supports the harness — it does not replace
golden/adversarial/regression sets or the CI gate.

## 10. Security, privacy & governance

**This is the layer that wins enterprise deals — never leave it thin.**

| Service | What it does |
|---|---|
| **Model Armor** | Content safety + security controls on **LLM prompts and responses** — sensitive-data leakage, **prompt injection**, offensive content; integrated with Sensitive Data Protection; monitoring dashboard *(Preview)* |
| **Sensitive Data Protection (DLP)** | 150+ AI-driven classifiers; discovery, de-identification, masking, tokenisation; powers DSPM |
| **VPC Service Controls** | Trusted perimeter around managed services to stop exfiltration; **Agent Identity as a first-class principal** in ingress/egress rules *(Preview)*; violation analyser |
| **CMEK / Cloud KMS** | Customer-managed keys for datasets, models, GKE |
| **IAM + Workload Identity** | Least privilege; no long-lived keys |
| **Security Command Center** | Posture, threat detection, findings across the estate |
| **Assured Workloads** | Regulatory/sovereignty controls (regions, personnel) |
| **Access Transparency / Access Approval** | Visibility and control over provider access — often required by bank/insurer security review |
| **Data residency** | Region pinning + regional endpoints; state it explicitly per data class |

Map each to the controls matrix in `05-architecture.md` (data class × control ×
verified-by). **Model Armor + Sensitive Data Protection + VPC-SC** is the standard
trio for a regulated GenAI deployment — name all three.

## 11. Observability & operations

**Cloud Monitoring / Logging / Trace / Error Reporting** (the golden signals) ·
**Agent Engine built-in observability** · **BigQuery as the audit warehouse** (where
`audit.jsonl` lands for querying) · **Looker / Looker Studio** (the dashboards in
`11-observability.md`) · **Cloud Build / Deploy + Artifact Registry** (CI/CD carrying
the eval gate).

## 12. FinOps

**Billing export → BigQuery** (per-feature/team/tenant attribution) · **Budgets &
alerts** (fire below the business-case break-even, not at it) · **Committed use
discounts / Provisioned Throughput** · **Batch prediction** for non-latency work ·
**Context caching** for repeated long prompts · the **Flash→Pro cascade** as the
primary unit-cost lever.

Tie every number back to the unit economics in `04-business-case.md`.

---

## How to use this in an architecture artifact

Do **not** dump this list. Produce, per `05-architecture.md`:

1. A **service inventory table** — layer · chosen service · why · alternative
   rejected · cost driver. Every layer from §1–§12 that the solution touches gets a
   row; layers deliberately not used get one line saying why not.
2. A **mermaid component diagram** with the real service names as nodes.
3. A **sequence diagram** for the primary flow (request → retrieval → model →
   validation → HITL → write-back → audit).
4. The **controls matrix** drawing from §10.
5. The **decision trail** — what was rejected and why (BigQuery ML instead of custom
   training; Vertex AI Search instead of custom RAG; Agent Engine instead of GKE).

## Sources (verified 2026-07)

- [Gemini Enterprise Agent Platform — product](https://cloud.google.com/products/gemini-enterprise-agent-platform) · [launch blog](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform) · [docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform) · [release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes)
- [Agent Development Kit (ADK)](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/adk)
- [Vector Search](https://docs.cloud.google.com/vertex-ai/docs/vector-search/overview) · [BigQuery generative AI](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview) · [Document AI + BigQuery](https://docs.cloud.google.com/document-ai/docs/big-query-integration)
- [Model Armor](https://cloud.google.com/security/products/model-armor) · [release notes](https://docs.cloud.google.com/model-armor/release-notes) · [Security Command Center](https://cloud.google.com/security/products/security-command-center) · [secure AI on Google Cloud](https://cloud.google.com/blog/products/identity-security/mastering-secure-ai-on-google-cloud-a-practical-guide-for-enterprises/)

*Same pattern applies to `knowledge/aws/` and `knowledge/azure/` — build them when a
deal needs that depth.*
