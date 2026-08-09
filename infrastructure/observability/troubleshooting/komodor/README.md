[← Troubleshooting](../README.md)

# Komodor

<https://github.com/komodorio/helm-charts>

UI: <https://app.komodor.com/>

---

> **SaaS.** The agent runs in your cluster; the data and the interface live in Komodor's
> platform. That is the first thing to decide about it.

## The problem it solves

The most common question during an incident is **"what changed?"** — and Kubernetes makes it
surprisingly hard to answer. Events expired an hour ago, the previous ReplicaSet is gone, and
nobody remembers whether that ConfigMap was edited yesterday or last week.

Komodor builds a continuous timeline of changes across the cluster — deploys, config changes,
scaling, node events — and correlates them with what broke, so the answer is a timeline rather
than an archaeology exercise.

## When to use it

- "what changed before this broke" is the recurring question
- you want change history without building the pipeline for it yourself
- a team without the capacity to operate a full observability stack

## When not to use it

- **cluster data cannot leave the environment** — this is the deciding constraint, not a preference
- you already export events and keep deploy history in Git, which covers much of the same ground
- you want self-hosted; the open-source part here is the Helm chart, not the platform

## The self-hosted equivalent

For the change-timeline problem specifically, [Sloop](../../events/sloop/README.md) reconstructs object
history locally, and exported events plus Git history cover the rest — with more work and no
external dependency.

---

[← Troubleshooting](../README.md)
