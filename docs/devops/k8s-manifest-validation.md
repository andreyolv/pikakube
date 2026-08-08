# Progressive Validation Gates for Kubernetes Manifests in CI

## Problem:
- The Cluster as the First Validator: Without a CI gate, the API server is the first thing that ever reads the manifest. A typo, a wrong `apiVersion`, or a malformed field is discovered at apply time, which in a GitOps setup means a reconciliation error surfacing minutes after merge, in a controller log nobody is watching.

- Silent Field Drops: A misspelled field such as `resources.limits.memroy` is not an error to most tooling. Rule-based scanners deserialize manifests into typed objects and discard what they do not recognize, so the check passes, the manifest applies, and the setting simply never takes effect. Nothing in the pipeline reports a problem.

- Validating the Wrong Artifact: Helm charts and Kustomize overlays are not Kubernetes manifests. Running any validator against the templated source either fails to parse or validates something the cluster will never see, producing false confidence.

- Version Skew Between CI and Cluster: A manifest validated against one Kubernetes version may use an API removed in the version actually running. Validation that is not pinned to the target release reports success for objects the cluster will reject.

- Tool Coupling: Every tool in this space is either abandoned, tied to a schema source that lags Kubernetes releases, or opinionated in ways that do not match the organization. A pipeline designed around a specific binary has to be redesigned when that binary is deprecated, which in this ecosystem is a matter of when.

## Solution:
- Validation Designed as Ordered Gates, Not as a Tool Choice: The pipeline is defined by the questions it asks, in increasing order of cost and decreasing order of objectivity. Each gate is a replaceable implementation behind a stable contract of input, exit code, and report format, so a deprecated tool is swapped without touching the pipeline design.

- Gate 1 — Parse: Is this valid YAML at all? Catches indentation, duplicate keys, and the implicit type conversions that make YAML dangerous for configuration, such as unquoted values being coerced into booleans. Objective, instant, no Kubernetes knowledge required.

- Gate 2 — Render: Templates and overlays are expanded into the concrete manifests the cluster will receive. Every subsequent gate consumes this output and never the source, which is the single most common design error in manifest pipelines.

- Gate 3 — Schema Conformance: Does every object match the API schema for the target Kubernetes version, including custom resources? Objective and binary, and deliberately placed before any rule-based check, because scanners silently ignore the unknown fields that only schema validation detects. The target version is pinned to the running cluster and bumped as part of the upgrade process.

- Gate 4 — Reliability Opinions: Missing resource requests, absent probes, single replicas, no disruption budget. Opinionated by nature, therefore configurable and owned by the platform team rather than treated as absolute truth.

- Gate 5 — Security Policy: Privileged containers, host mounts, excessive capabilities, writable root filesystems. Kept separate from Gate 4 because the findings have a different owner, a different severity scale, and a different escalation path, even though both read the same files.

- Gate 6 — Organizational Policy: Rules that exist only for this platform, expressed as policy-as-code and executed by the same engine that enforces them at admission. Writing the rule once and running it in CI and in the cluster removes the drift between what the pipeline allows and what the cluster accepts.

- Gate 7 — Server-Side Validation (Optional): For pipelines that already provision an ephemeral cluster, a server-side dry run against a real API server is the highest-fidelity check available, since it exercises admission, defaulting, and webhooks. Reserved for critical paths given its cost.

- Shift-Left Parity: Gates 1 through 3 are cheap and deterministic, so they also run as pre-commit hooks. The developer sees the same failure locally that CI would produce, and the pipeline stops being the place where obvious mistakes are discovered.

- Progressive Enforcement: New gates are introduced in report-only mode, the existing backlog is quantified and remediated, and only then are they promoted to required status checks. Findings are published as inline comments on the changed lines rather than as walls of text in job logs.

## Skills:
- DevOps
- Platform Engineering
- CI/CD

## Tools:
- Kubernetes
- Helm
- Kustomize
- Github Actions
- pre-commit
