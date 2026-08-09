[← Service level](../README.md)

# Pyrra

<https://github.com/pyrra-dev/pyrra>

Grafana examples: <https://github.com/pyrra-dev/pyrra/tree/main/examples/grafana>

---

> Simple and good — the one to start with if SLOs are new to the platform.

## The problem it solves

Same generation problem as [Sloth](../sloth/README.md): correct multi-window burn-rate rules from a short
definition. Pyrra adds the piece that changes behaviour — **a UI showing remaining error
budget**.

That matters more than it sounds. An error budget expressed only as PromQL is a rule file
nobody opens. A page showing "68% of this month's budget left" is something a team looks at
before deciding whether to ship, which is the entire point of having one.

Definitions are CRDs (`ServiceLevelObjective`), reconciled into `PrometheusRule` objects — so
it fits GitOps while still being live.

## When to use it

- SLOs are **new** to the team, and visibility is what will make them stick
- you want budgets visible without building dashboards first
- CRDs suit the workflow better than a generation step

## When not to use it

- you want generation only, with nothing running — [Sloth](../sloth/README.md)
- definitions must be portable across vendors — [OpenSLO](../openslo/README.md)

## Why it is the recommended starting point

The failure mode of SLOs is not technical. It is that they get defined, generate some alerts,
and then nobody consults the budget — at which point they are an elaborate threshold alert.

The UI is what prevents that, and it is why this is the one to reach for first even though
Sloth produces equivalent rules.

---

[← Service level](../README.md)
