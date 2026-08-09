[← Right-sizing](../README.md)

# KRR — Kubernetes Resource Recommender

<https://github.com/robusta-dev/krr>

---

## The problem it solves

Every other tool in this folder wants to be installed first: a controller, CRDs, an admission
webhook, a namespace, a chart to review. That is a lot of ceremony before you know whether the
cluster has a right-sizing problem at all.

KRR is a **CLI**. It connects to the Kubernetes API to list workloads and to the Prometheus you
already have for their usage history, and prints a table of what each container requests against
what it should. Nothing runs in the cluster. Nothing is mutated. There is no agent to remove
afterwards.

It reads from Prometheus and Prometheus-compatible stores, so on a platform that already has a
metrics pipeline it works on the first run. The default strategy sizes CPU requests from a high
percentile of observed usage and memory requests from the observed peak plus a margin, over a window
of a couple of weeks — the asymmetry described in [`rightsizing/`](../README.md) section 2, applied
sensibly out of the box. Output can be a table, JSON, YAML, CSV or HTML, which makes it easy to feed
into a report or a pipeline.

## When to use it

- **first.** Before deciding whether any controller in this folder is worth deploying — it answers
  "how big is the gap" in one command
- producing the initial wave of pull requests, workload by workload
- a periodic report — run it on a schedule and publish the biggest gaps
- clusters where installing a mutating controller is not going to be approved
- checking another tool's recommendations against an independent implementation

## When not to use it

- **without Prometheus, or without enough retention.** The recommendation is only as good as the
  history behind it; a short window produces a confident number that misses the peak
- as a continuous control — it is a report, not a controller. Nothing enforces or re-checks
- as the surface application teams read; [Goldilocks](../goldilocks/README.md) is the page for that
- for workloads with seasonal peaks outside the query window, unless the window is widened
  deliberately
- expecting it to fix anything: the output is a list of changes somebody still has to make

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/robusta-dev/krr>** — the project, from Robusta. Open source, and the same
recommendations also surface inside Robusta's commercial platform — worth knowing so the free CLI is
not mistaken for a trial of something.

Two properties are the reason to reach for it before anything else here:

- **No in-cluster component.** No CRDs, no webhook in the pod-creation path, nothing to leave behind.
  The blast radius of trying it is zero, which is not true of any other tool in this folder.
- **It reads history you already have.** VPA's recommender starts from nothing and needs days to
  become trustworthy; KRR queries weeks of existing Prometheus data on its first run. On a platform
  with a real metrics stack — see [`observability/metrics/`](../../../../observability/metrics/README.md)
  — that difference is the whole argument.

**Nothing is deployed for this in the repository, and nothing should be.** It is a CLI run against a
cluster, so the artefact is a command and a habit rather than a manifest. The useful next step is
making it recurring: a scheduled run that publishes the largest request-versus-usage gaps, so the
list arrives without anyone remembering to ask for it.

**One caveat on interpreting the output.** KRR reports per-container recommendations against current
requests and shows what could be saved. That saving is only realised if the freed capacity actually
lets nodes go away — which needs consolidation, from [`node/`](../../node/README.md). Right-sizing on
a fixed node pool improves density and saves nothing.

---

[← Right-sizing](../README.md)
