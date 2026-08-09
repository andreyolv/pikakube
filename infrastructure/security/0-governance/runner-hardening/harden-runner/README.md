[← Runner hardening](../README.md)

# Harden-Runner

<https://github.com/step-security/harden-runner>

---

## The problem it solves

A GitHub Actions job runs arbitrary code from every dependency in the build, while holding
registry credentials, cloud credentials and — increasingly — a signing identity. If a
dependency's install script reads the environment and posts it to an external host, nothing in
the job log will say so. The runner is destroyed afterwards, so there is nothing left to
examine either.

Harden-Runner, from StepSecurity, is a single step added at the start of a job that installs an
eBPF-based agent on the runner and monitors what the job actually does:

| Capability | What it gives you |
|---|---|
| **Egress filtering** | default-deny outbound with an allow-list of permitted destinations |
| **Egress monitoring** | the full list of hosts a job contacted, per run |
| **File monitoring** | detects source files modified after checkout — the shape of a build-time backdoor |
| **Process monitoring** | what the job actually executed, including what dependency scripts ran |
| Insights per run | a network and process report linked from the workflow run |

The two that matter most are named in [`../README.md`](../README.md): **egress filtering**,
because exfiltration requires an outbound connection and a build's legitimate destinations are
few and enumerable; and **tamper detection**, because the artefact differing from the reviewed
source is the failure that signatures and provenance cannot catch on their own.

Its practical strength is the adoption path. `policy: audit` records destinations without
blocking anything, so the allow-list is derived from real builds rather than guessed — and the
list itself is usually the first interesting output, since builds routinely contact hosts
nobody expected.

## When to use it

- **GitHub Actions** workflows that handle credentials, publish artefacts, or sign anything
- before moving signing into CI — a signing identity on an unmonitored runner is the scenario
  this exists for
- when third-party actions and dependencies with install scripts are in the build, which is
  effectively always
- to answer "what does our build actually talk to?", which is worth knowing even with no
  intention of enforcing
- as an early, cheap control: one step per job, no infrastructure, free for public repositories

## When not to use it

- **outside GitHub Actions.** It is specific to Actions runners; GitLab, Jenkins, Buildkite and
  others need their own approach
- expecting it to replace pipeline configuration hygiene. It does not fix `pull_request_target`
  misuse, unpinned actions, over-scoped tokens or script injection — those are workflow
  problems, covered in [`../README.md`](../README.md#7-anti-patterns) and by linters in
  `4-code/pipeline/`
- in enforce mode as a first step. A default-deny allow-list applied without an audit period
  will break builds in ways that look like flaky infrastructure
- where an eBPF agent on the runner is not acceptable, or on runner images where it cannot load
- as a substitute for ephemeral self-hosted runners. Monitoring a runner that persists state
  between jobs addresses the smaller half of the problem

## Notes

Original reference recorded for this tool:

> <https://github.com/step-security/harden-runner>

Points worth adding, since only the link was recorded.

**Pricing shape.** It is free for public repositories, which is the case that matters here, and
commercial for private ones at the higher tiers. The Action itself is open source; the insights
dashboard and some policy features are the product.

**Audit before enforce, always.** The recommended sequence is `policy: audit` on every workflow
for a period, read the aggregated destination list, then convert it into `allowed-endpoints`
and switch to `policy: block`. Skipping the audit period produces broken builds attributed to
network flakiness, which is the fastest way to get the step removed.

**The destination list is the deliverable even without enforcement.** Most teams running audit
mode for the first time find their builds contacting hosts nobody could account for —
telemetry endpoints in build tooling, unexpected CDN mirrors, analytics in a transitive
dependency. That inventory is useful on its own and is the argument for turning it on before
there is any appetite for blocking.

**It complements provenance rather than duplicating it.** SLSA provenance says *which* workflow
built the artefact; harden-runner says *what that workflow did while it ran*. The build-time
backdoor scenario — reviewed source, modified during build, correctly signed and attested
output — is caught by the file monitoring here and by nothing in
[`supply-chain/`](../../supply-chain/README.md).

**Pin it like any other action.** The advice about pinning third-party actions to commit SHAs
applies to this one too. A security action referenced by mutable tag is the same exposure it
was installed to prevent.

---

[← Runner hardening](../README.md)
