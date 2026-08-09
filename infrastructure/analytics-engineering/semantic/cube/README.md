[← Semantic layer](../README.md)

# Cube

<https://github.com/cube-js/cube>
<https://cube.dev/docs>

Chart: <https://github.com/gadsme/charts>

---

## The problem it solves

Metric definitions duplicated across BI tools, applications and notebooks — each slightly
different, none authoritative.

Cube puts them in one place and serves them to everything:

```javascript
cube('Orders', {
  sql: `SELECT * FROM analytics.orders`,
  measures: {
    revenue: {
      sql: 'amount',
      type: 'sum',
      filters: [{ sql: `${CUBE}.status != 'refunded'` }]
    }
  },
  dimensions: {
    region: { sql: 'region', type: 'string' }
  }
});
```

The refund exclusion is written once. Every consumer that asks for revenue gets it.

## What it provides beyond definitions

| Capability | Why it matters |
|---|---|
| **Pre-aggregations** | Cube maintains rollup tables and rewrites queries to hit them — often the difference between a 20-second dashboard and a 200ms one |
| **APIs** | SQL, REST and GraphQL, so applications consume the same definitions as dashboards |
| Access control | row and column level, applied regardless of which tool asks |
| Caching | the same question, asked repeatedly, answered once |

The pre-aggregation layer is the part that is hard to replicate by hand. It is what makes a
semantic layer a performance component as well as a governance one.

## When to use it

- **several different consumers** need the same metrics — a BI tool, an application, a notebook
- an application embeds analytics and needs a metrics API rather than raw SQL
- dashboard performance is a problem and pre-aggregation is the fix

## When not to use it

- dashboards are the only consumer — [Lightdash](../../viz/lightdash/README.md) reads dbt metrics directly, with nothing extra to run
- the modelling layer is not solid yet. A semantic layer over poorly modelled data moves the problem rather than solving it
- one team, one BI tool, and no disagreement about metrics has occurred

## The order that matters

1. Model the data properly — [`transform/`](../../transform/README.md)
2. Discover that more than one consumer needs the same numbers
3. **Then** add a semantic layer

Adopting it at step 1 produces a second transformation layer and a service to operate, for a
problem that does not exist yet.

---

[← Semantic layer](../README.md)
