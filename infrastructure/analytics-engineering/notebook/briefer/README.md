[← Notebooks](../README.md)

# Briefer

<https://github.com/briefercloud/briefer>

---

## The problem it solves

Exploration and publication are usually two tools. An analyst explores in
[Jupyter](../jupyter/README.md), finds something worth sharing, and then rebuilds it in a BI tool —
duplicating the query and creating a second place where the logic lives.

Briefer combines them: notebooks and dashboards in one product, collaborative, where the same
document that did the exploration becomes the thing that gets shared.

| Feature | Detail |
|---|---|
| Notebook and dashboard | one artefact, two presentations |
| SQL and Python together | query, then process the result in Python |
| Collaboration | multiple people in the same document |
| Scheduling | notebooks that refresh |
| Publishing | share a clean view without the code |

## When to use it

- the gap between "an analyst found something" and "the team can see it" is real friction
- teams collaborate on analysis rather than working alone
- you want one tool instead of a notebook plus a BI tool

## When not to use it

- the audiences are genuinely different — business users needing self-service are better served by [Metabase](../../viz/metabase/README.md), engineers by [Evidence](../../viz/evidence/README.md)
- notebooks should stay strictly for exploration, with everything published going through [dbt](../../transform/dbt/README.md) and a reviewed dashboard
- you want the largest ecosystem; this is a smaller, newer project

## The tension worth naming

Making it easy to publish a notebook is the feature, and it is also the risk. The discipline in
[`../README.md`](../README.md#2-the-problem-with-notebooks-in-production) — notebooks explore,
they do not run in production — gets harder to hold when publishing is one click.

Useful for a team that wants collaborative analysis and understands that boundary. Risky for
one that does not, because it removes the friction that used to enforce it.

---

[← Notebooks](../README.md)
