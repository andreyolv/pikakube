[← Lifecycle orchestration](../README.md)

# Keptn

<https://github.com/keptn/lifecycle-toolkit>
<https://keptn.sh/>

---

## The problem it solves

Kubernetes considers a deployment successful when the pods are Ready. That is a statement about
containers starting, not about the release working.

Keptn adds **evidence** around the deployment:

| Phase | What it can do |
|---|---|
| **Pre-deployment** | checks before anything rolls — is the dependency healthy, is the database migrated, is the change window open |
| **During** | observe the deployment as a whole, including timing |
| **Post-deployment** | run tests, then **evaluate an SLO** against real metrics |
| Outcome | mark the deployment succeeded or failed, based on that evaluation |

The SLO evaluation is the distinctive part. Instead of "the pods are Ready", the criterion
becomes "error rate stayed under 1% and p95 under 300ms for ten minutes after rollout" — and
the deployment is judged against it automatically.

## When to use it

- deployment success should be defined by **metrics**, not by pod status
- pre-deployment conditions genuinely exist — migrations, dependencies, change windows
- you want deployment lifecycle observability: how long each phase actually took

## When not to use it

- the requirement is safe **rollout** of one release — [Flagger](../../progressive-delivery/flagger/README.md) or [Argo Rollouts](../../progressive-delivery/argo-rollouts/README.md) do that more directly
- version promotion between environments — [Kargo](../kargo/README.md)
- there are no SLOs yet, which removes the main input. See [`service-level/`](../../service-level/README.md)

## The relationship to progressive delivery

They overlap and are not substitutes:

| | Progressive delivery | Keptn |
|---|---|---|
| Scope | one rollout, traffic shifting | the deployment lifecycle around it |
| Decides | promote or roll back this canary | did this deployment succeed at all |
| Timing | during traffic shift | before, during and after |

A canary controller answers whether to keep shifting traffic. Keptn answers whether the release
met its objective — which is a question that outlives the rollout window.

---

[← Lifecycle orchestration](../README.md)
