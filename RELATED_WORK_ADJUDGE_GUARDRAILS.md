# Related Portfolio Work: AdJudge Guardrails

[AdJudge Guardrails](https://github.com/DenzelR12/adjudge-guardrails) applies the same data-product engineering principles demonstrated in Developer Ecosystem Insights to AI-assisted creative-quality review.

## Shared engineering principles

| Developer Ecosystem Insights | AdJudge Guardrails |
|---|---|
| API ingestion and source checks | Dataset, document, event, and warehouse source contracts |
| Schema validation and data-quality gates | Contract validation, freshness SLAs, and source quarantine |
| Freshness monitoring | Verified, stale, and unverifiable metric status controls |
| Defensible metric definitions | Versioned definitions, input hashes, source snapshots, and computation provenance |
| Fail-closed publication | Blocking of stale/unverifiable metric claims and human-review routing |
| Verification workflow | Human–LLM evaluation, incident forensics, and remediation evidence bundles |

## AdJudge Guardrails

AdJudge is an enterprise reference implementation for auditing and operationalizing AI-assisted multimodal creative review. It measures human–LLM disagreement and positivity bias, uses provenance-aware retrieval and verified metric evidence, routes high-risk cases to expert review, and designs for tenant-safe analytics, root-cause investigation, and human-approved remediation plans.

The project demonstrates how the observability and quality controls in a telemetry pipeline extend to AI decision systems: every source, metric, retrieval result, routing decision, and operational event should be traceable, versioned, and safe to challenge.

## Portfolio narrative

Together, these projects demonstrate a solution-architect approach to enterprise AI and data systems: define the decision, establish trustworthy source contracts, make metrics transparent, fail safely when evidence is insufficient, and give operators practical workflows to investigate and act on issues.
