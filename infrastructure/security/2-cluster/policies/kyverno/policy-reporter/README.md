[← Kyverno](../README.md)

# Policy Reporter

<https://github.com/kyverno/policy-reporter>
<https://github.com/kyverno/policy-reporter-ui>

A UI, a metrics exporter and a notification router for `PolicyReport` resources. The thing that
makes audit mode readable.

---

## The problem it solves

Audit mode only works if somebody reads the results. Kyverno emits them as `PolicyReport` and
`ClusterPolicyReport` custom resources — one per namespace, listing every rule result for every
resource. On a cluster with a few hundred workloads and a dozen policies, that is thousands of
entries spread across dozens of objects, reachable only by `kubectl get polr -A -o yaml`.

Nobody does that twice. So the audit-first rollout described in
[`../../README.md`](../../README.md#4-audit-vs-enforce) — deploy in audit, collect violations, fix
or exempt, then enforce — stalls at step two, and the policy either never gets enforced or gets
enforced blind.

Policy Reporter reads those resources and provides three things:

| Component | What it gives you |
|---|---|
| The core service | Prometheus metrics: pass/fail counts by policy, namespace, severity, category |
| The UI (`policy-reporter-ui`) | a browsable view — filter by namespace, policy, severity, and see which resources are failing |
| Targets | push results to Slack, Teams, Elasticsearch, Loki, S3, a webhook, and others |

The third one is what turns it from a dashboard into a workflow: a new violation appearing can
notify the team that owns the namespace, rather than waiting to be discovered.

`PolicyReport` is a Kubernetes SIG standard (`wgpolicyk8s.io`), not a Kyverno invention, so Policy
Reporter also consumes reports from Trivy Operator, Falco, Kubescape and others. In practice that
makes it a general-purpose findings dashboard for the cluster, not just a Kyverno accessory.

## When to use it

- **Any time a policy is in audit mode.** Audit results with no reader are latency with no benefit.
- **During a policy rollout.** The workflow it enables is the one that works: add a policy in
  `Audit`, watch which namespaces light up, talk to those teams, then flip to `Enforce`.
- **To alert on new violations.** Not on the absolute count — that number is large and stable and
  therefore ignorable — but on a policy that started failing where it did not before.
- **When several report producers are in play.** One place for Kyverno, Trivy and Kubescape
  findings is better than three.
- **For metrics rather than the UI.** The exporter alone is useful even without the web interface:
  a Grafana panel of failures by policy over time makes progress visible, and progress is what
  keeps a policy programme alive.

## When not to use it

- **Everything is already in `Enforce`.** If nothing is in audit, there is little to report — the
  feedback is the rejection message the user already saw.
- **You already have a findings pipeline.** If reports are being shipped to a SIEM or a security
  platform, another UI is a second place to look.
- **You are not going to look at it.** Deploying a dashboard nobody opens is the same failure as
  audit mode with no reader, with an extra Deployment and an ingress. The honest test: who is
  expected to open this, and how often?
- **The cluster is tiny.** With a handful of workloads, `kubectl get polr -A` is genuinely enough.

Two operational notes that are easy to miss:

- **Report volume is real.** `PolicyReport` objects are stored in etcd and a cluster with many
  resources and many policies produces a lot of them. Kyverno's reports controller is separate from
  the admission controller partly for this reason. If report generation becomes expensive, narrowing
  what policies match is the fix, not turning off the reporter.
- **The UI is a view of cluster security posture.** Exposing it through an ingress means exposing a
  list of exactly which workloads fail which security policies. It needs authentication.

## Notes

There were no free-form notes in the original `doc.md` beyond the two repository links, which are at
the top of this file. What follows is the state of the deployment in this folder.

### How it is deployed here

`helm/helmrelease.yaml` installs chart `policy-reporter` 2.24.2 into the `kyverno` namespace with:

| Setting | Meaning |
|---|---|
| `dependsOn: kyverno` | Flux will not install it until the Kyverno HelmRelease is ready — correct, since it consumes CRDs Kyverno provides |
| `ui.enabled: true` | the web interface is deployed, not just the metrics exporter |
| `ui.displayMode: dark` | cosmetic |
| `global.plugins.kyverno: true` | enables the Kyverno-specific plugin, which adds policy details and the policy source to each result |

The Kyverno plugin is the setting worth understanding: without it, Policy Reporter shows generic
`PolicyReport` results; with it, it can show which Kyverno policy produced a result and link back to
the rule. Since Kyverno is the only report producer in this repo, leaving it off would lose most of
the context.

What is not configured: no `target` is set, so results are not pushed anywhere — no Slack, no Loki,
no webhook. The reporter is a pull-based dashboard here rather than a notification path. That is a
reasonable starting point and it is the difference between "we can look this up" and "we find out".

There is also no ingress in this HelmRelease, so reaching the UI means a port-forward. Given the UI
lists which workloads fail which security policies, that is a defensible default.

### Where it fits

Policy Reporter is the reader for the audit-mode half of
[`../README.md`](../README.md) and [`../examples/`](../examples/README.md), several of which are
deliberately set to `validationFailureAction: Audit`. Those policies produce reports and nothing
else; this is what makes them worth having.

The equivalent problem on the [Gatekeeper](../../gatekeeper/README.md) side has no equivalent
solution in this repo — violations live in each constraint's truncated `status`, and the workaround
recorded there is a `jq` pipeline over the controller's logs. That contrast is a fair part of the
argument for Kyverno over Gatekeeper on this platform.

---

[← Kyverno](../README.md)
