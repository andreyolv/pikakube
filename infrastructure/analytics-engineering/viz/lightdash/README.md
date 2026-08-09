[← Visualisation](../README.md)

# Lightdash

<https://github.com/lightdash/lightdash>
<https://github.com/lightdash/helm-charts>

---

## The problem it solves

In most BI tools, metrics get defined **in the tool** — which means they get defined again in
the next tool, slightly differently, and two dashboards disagree about revenue.

Lightdash reads metrics and dimensions **directly from dbt**. The definition lives in the
`.yml` next to the model, in Git, reviewed in a pull request — and the BI tool consumes it
rather than re-creating it.

```yaml
# in a dbt model's schema.yml
columns:
  - name: amount
    meta:
      metrics:
        total_revenue:
          type: sum
```

That metric now exists everywhere Lightdash is used, defined once.

## When to use it

- **dbt is the source of truth**, and metric definitions belong with the models
- the team is comfortable that metric changes go through a pull request
- you want a semantic layer without operating [Cube](../../semantic/cube/README.md)

## When not to use it

- dbt is not in use — the entire model depends on it
- business users need to define their own metrics ad hoc; here that requires a code change
- you need Superset's breadth of chart types or database support

## The trade, stated plainly

Metric definitions become **engineering artefacts**. That is the benefit — versioned, reviewed,
consistent — and it is also the cost: an analyst who wants a new metric opens a pull request
rather than clicking.

For a platform that already treats [dbt](../../transform/dbt/README.md) as the modelling layer, that is
usually the right trade. For a team where analysts move faster than review cycles, it is not.

## Where it sits against a semantic layer

Lightdash gives you one metric definition **for Lightdash**. [Cube](../../semantic/cube/README.md) gives
you one definition for **any consumer** — BI tools, applications, notebooks.

If dashboards are the only consumer, this is the lighter answer and needs nothing extra to run.

---

[← Visualisation](../README.md)
