[← Visualisation](../README.md)

# Evidence

<https://github.com/evidence-dev/evidence>
<https://evidence.dev/>

---

## The problem it solves

Dashboards built in a UI have no diff, no review, no test, and no way to say what changed
between last month and this one. They are the last part of the data stack that is not code.

Evidence makes them **markdown plus SQL**, built into a static site:

````markdown
## Revenue by region

```sql regional_revenue
select region, sum(amount) as revenue
from analytics.orders
group by 1
```

<BarChart data={regional_revenue} x=region y=revenue />
````

That file goes through a pull request, gets deployed by CI, and the resulting site is static —
no server rendering queries per visitor.

## When to use it

- **engineers** build the dashboards, and review matters
- reports should be versioned and deployed like software
- a static site is a good fit: fast, cheap, and no BI server to operate
- narrative reports — text and charts together — rather than an exploration tool

## When not to use it

- **business users need to build their own** — this is the opposite end of the range from [Metabase](../metabase/README.md)
- ad-hoc exploration is the primary use; the audience here reads rather than slices
- interactive drill-down across arbitrary dimensions is required

## Where it genuinely wins

Recurring, narrative reporting. A monthly business review where the text explains the numbers,
both are versioned together, and last quarter's version can be reproduced exactly.

That is a real gap in the other tools: a dashboard shows the current state, and cannot easily
tell you what it said in March.

## The honest limit

It is not self-service. Every change is a code change, which is the point and also the ceiling
on adoption — one team can maintain reports for many readers, but readers cannot answer their
own new questions.

Pairs well with [Metabase](../metabase/README.md) alongside it: Evidence for the reports that matter and
are reviewed, Metabase for everyone else's questions.

---

[← Visualisation](../README.md)
