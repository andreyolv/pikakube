[← Progressive delivery](../README.md)

# Argo Rollouts

<https://github.com/argoproj/argo-rollouts>
<https://github.com/argoproj/argo-helm>
<https://argo-rollouts.readthedocs.io/>

Examples: [`canary-example/`](canary-example/) · [`k8s-deployment-modes/`](k8s-deployment-modes/)

---

## The problem it solves

Progressive delivery with fine-grained control over each step — and a **UI** for watching and
intervening.

Its structural choice is the opposite of [Flagger](../flagger/README.md): instead of managing a canary
around an existing `Deployment`, it replaces `Deployment` with a **`Rollout`** resource. More
control, at the cost of changing every manifest that participates.

What that buys:

| Capability | Detail |
|---|---|
| Explicit steps | set weight, pause, set weight, pause — including indefinite pauses |
| **Manual gates** | a human promotes, when policy requires it |
| `AnalysisTemplate` | reusable metric checks, from Prometheus, Datadog, Wavefront or a job |
| Experiments | run two versions side by side to compare, without releasing |
| Blue/green **and** canary | both are first-class, not variations |

## When to use it

- **Argo CD** is the GitOps tool — same ecosystem, and the UI integrates
- releases need **manual approval** at a defined point
- you want per-step control rather than a uniform ramp
- someone will actually use the UI, which is a real part of the value

## When not to use it

- you would rather not change the workload resource type — [Flagger](../flagger/README.md) leaves `Deployment` alone
- Flux is the GitOps tool, where Flagger is the native pairing
- traffic is too low for canary percentages to mean anything

---

## Notes

```bash
kubectl argo rollouts version

kubectl argo rollouts get rollout rollouts-demo --watch

kubectl argo rollouts promote rollouts-demo

kubectl argo rollouts abort rollouts-demo
```

The `--watch` view is the one worth knowing: it shows step progress, traffic weight and
analysis results live in the terminal, which is often faster than the UI during an actual
release.

---

[← Progressive delivery](../README.md)
