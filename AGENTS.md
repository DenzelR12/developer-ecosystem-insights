# Agentic Engineering Workflow

This project uses an explicit multi-agent workflow so automation remains reviewable and safe.

## Roles

### Planner
- Restates the business question as measurable entities, events, dimensions, and time windows.
- Identifies source systems and known coverage gaps.
- Writes a metric contract before implementation.

### Builder
- Implements the smallest change that satisfies the approved contract.
- Adds typed input validation, structured errors, and tests with the implementation.
- Never embeds secrets, tokens, or private customer data in code or fixtures.

### Verifier
- Runs unit tests and checks expected failure modes: expired data, malformed schema, rate limiting, and row-count anomalies.
- Confirms each published metric has source metadata and a caveat.

### Adversarial reviewer
- Tries to break assumptions before release.
- Checks for double counting, misleading funnels, unsupported causal claims, silent partial API responses, and metrics that combine incompatible populations.
- Blocks publication if a quality gate is bypassed or a caveat is missing.

## Release gate

A change can be released only when:

1. Tests pass.
2. Input schema validation passes.
3. Freshness, null-rate, and volume-anomaly quality gates pass.
4. Metric definitions document aggregation behavior and limitations.
5. A reviewer has checked that the output is suitable for the intended audience.

## Principle

The system should fail closed rather than publish a number that looks precise but cannot be defended.