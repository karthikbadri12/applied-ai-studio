# Amazon Bedrock connector (model invocation)

**Method:** AWS SDK · **Category:** model · **Action:** invoke (not a data source)

## Auth
- **IAM role** (instance/task role or IRSA on EKS) — keyless, preferred. For local
  dev, a scoped IAM user with short-lived STS credentials, never long-lived keys in
  the repo.

## Least-privilege scoping
- Allow only `bedrock:InvokeModel` / `bedrock:InvokeModelWithResponseStream` on the
  **specific model ARNs** the `architecture` artifact approved. Deny everything else.
- Pin the region to the residency the controls matrix requires.

## Regulated-data handling
- Bedrock does not retain prompts/completions for model training, but confirm your
  data-class controls: use **Bedrock Guardrails** for PII redaction and content
  filtering, and only route a data class to Bedrock if `05-architecture.md` approved
  that class for this endpoint.
- Enable model-invocation logging to CloudWatch/S3 for the Article 7 audit trail.

## Note
This connector is how `coder` calls the model; the *choice* of model and the
routing/fallback cascade come from `model-selector` and `architecture`, not here.
