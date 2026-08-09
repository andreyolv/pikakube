[← Visualisation](../README.md)

# Redash

<https://github.com/getredash/redash>
<https://github.com/getredash/contrib-helm-chart>

---

## The problem it solves

Query-centric BI. The unit is a **saved query** rather than a dashboard: write SQL, run it,
visualise the result, share the link, optionally schedule a refresh and an alert.

That is a genuinely different workflow from Metabase or Superset. It suits people whose work is
"answer this question with SQL and send it to someone", where a dashboard is an occasional
by-product rather than the goal.

| Feature | Detail |
|---|---|
| Query snippets and parameters | reusable SQL with inputs |
| Scheduled refresh | queries run on a schedule, results cached |
| **Alerts on query results** | notify when a value crosses a threshold |
| Many data sources | including databases, APIs and Google Sheets |

The alerting is worth noting: alerting on an arbitrary SQL result is something the other BI
tools do less directly, and it covers simple data-quality checks without another system.

## When to use it

- analysts work **query-first**, and sharing a result matters more than curating dashboards
- lightweight alerting on a query result is useful
- an existing Redash deployment that works

## When not to use it

- self-service for non-SQL users — [Metabase](../metabase/README.md)
- rich dashboards and many chart types — [Superset](../superset/README.md)
- dashboards as code — [Evidence](../evidence/README.md)

## Project status

Development has been intermittent since the Databricks acquisition. Worth checking current
maintenance activity before adopting it for something new — the tool works, but the trajectory
matters for a component people depend on daily.

The chart above is community-maintained, which is the usual sign to plan the deployment
carefully rather than assume it is looked after.

---

[← Visualisation](../README.md)
