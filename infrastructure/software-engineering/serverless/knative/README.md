[← Serverless](../README.md)

# Knative

<https://github.com/knative/serving>
<https://github.com/knative/operator>

---

## The problem it solves

Knative is **not a function platform**, and treating it as one is the first mistake. It is two
independent components:

| Component | What it does |
|---|---|
| **Serving** | takes an ordinary container image and gives it request-driven autoscaling, **including to zero**, plus revisions and traffic splitting between them |
| **Eventing** | routes **CloudEvents** — sources, brokers, triggers with filters — between anything that can receive an HTTP POST |

Serving is the piece most people mean. You bring a container that listens on a port; Knative gives
you a URL, scales the deployment on concurrent requests rather than on CPU, drops it to zero when
idle, and holds each deploy as an immutable *revision* so traffic can be split or rolled back by
percentage.

That is why it is the substrate under other platforms rather than a competitor to them —
[OpenFunction](../openfunction/README.md) runs its sync workloads on exactly this.

## When to use it

- you already build containers, and what you want is **scale to zero plus revisions**, not a
  function abstraction
- traffic is bursty and concurrency-based autoscaling fits better than CPU-based
- you want percentage traffic splitting between revisions as a property of the platform
- you need **CloudEvents routing** with filtering, and would otherwise build it

## When not to use it

- you want your developers to write handlers rather than containers — that is
  [OpenFaaS](../openfaas/README.md) or [Fission](../fission/README.md)
- the workload is latency-sensitive; scale to zero means cold starts, and `minScale: 1` removes
  the reason you installed it
- **you install everything through Helm** — see the note below, which for this repository is
  decisive
- the cluster is small: Serving brings its own networking layer (a mesh, Contour, or Kourier) on
  top of whatever ingress already exists

## Notes

**No Helm chart.** This is the entire recorded note, and in this repository it settles the
question. Every other tool in [`serverless/`](../README.md) — and nearly every tool in
`infrastructure/` — is installed with a Flux `HelmRelease` pointing at a `HelmRepository`. Knative
does not publish one. It is distributed as **release YAML artifacts** (`serving-crds.yaml`,
`serving-core.yaml`, a networking layer, and the equivalents for Eventing) and as the **Knative
Operator**, which is itself a YAML release and which reconciles `KnativeServing` and
`KnativeEventing` custom resources.

The practical consequence for a GitOps repository:

| Route | What it means here |
|---|---|
| Flux `HelmRelease` | **not available** |
| Flux `Kustomization` over the release YAML | works, but you own version pinning and the upgrade order by hand |
| Install the operator, then commit a `KnativeServing` CR | the cleaner option — the operator handles component ordering and upgrades, and the committed CR stays small |

None of those is hard. All of them are *different from everything else in this repository*, which
is the actual cost: a second installation pattern to understand, review and debug. That is why
this folder contains a README and nothing else — no `helm/`, no `namespace.yaml` — while its
neighbours all have manifests.

The same finding is recorded against ActiveMQ Artemis in [`messaging/`](../../messaging/README.md).
It is worth stating as a general rule for this platform: **in a Flux repository, "no Helm chart"
is a real evaluation criterion**, not a footnote.

If Knative is adopted, the operator route is the one to take — the `knative/operator` repository
above is linked in the original note alongside `knative/serving` for exactly that reason.

---

[← Serverless](../README.md)
