[← Service level](../README.md)

# Sloth

<https://github.com/slok/sloth>
<https://sloth.dev/>

---

## The problem it solves

Multi-window burn-rate alerting is the correct way to alert on an SLO, and writing it in PromQL
by hand is error-prone enough that most teams get it subtly wrong — wrong windows, wrong
factors, or rules that never fire.

Sloth takes a short SLO specification and **generates** the whole set: the SLI recording rules,
the multi-window burn-rate alerts, and metadata rules for dashboards.

Nothing runs in the cluster. It is a generator — output goes into Git as `PrometheusRule`
objects, which fits GitOps exactly.

```yaml
# roughly: objective, and the queries for good and total events
service: my-api
slos:
  - name: availability
    objective: 99.5
    sli:
      events:
        error_query: ...
        total_query: ...
```

## When to use it

- you want **correct** burn-rate rules without deriving them yourself
- GitOps — generated rules are reviewed and versioned like any other manifest
- no appetite for another component running in the cluster

## When not to use it

- you want to **see** remaining error budget in a UI — [Pyrra](../pyrra/README.md) includes one
- SLO definitions should be portable across tooling — [OpenSLO](../openslo/README.md) is the spec, and Sloth can consume it

## Dashboards

Community dashboards that pair with the generated metrics:

- <https://grafana.com/grafana/dashboards/14348-slo-detail/>
- <https://grafana.com/grafana/dashboards/8793-service-level-sli-slo/>
- <https://grafana.com/grafana/dashboards/14643-high-level-sloth-slos/>

## Sloth or Pyrra

Both generate the same class of rules. The difference is what else you get:

| | Sloth | [Pyrra](../pyrra/README.md) |
|---|---|---|
| Runs in cluster | no — a generator | yes, a controller and UI |
| Definition | YAML spec, generated ahead of time | CRDs, reconciled |
| Budget visibility | build your own dashboards | included |
| GitOps fit | very clean — output is plain manifests | CRDs in Git, UI reads live |

---

[← Service level](../README.md)
