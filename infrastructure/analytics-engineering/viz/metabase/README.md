[← Visualisation](../README.md)

# Metabase

<https://github.com/metabase/metabase>
<https://www.metabase.com/docs/latest/>

Community chart: <https://github.com/pmint93/helm-charts>

---

## The problem it solves

Most BI tools are built for people who write SQL and then claim to be self-service. Metabase
is genuinely usable by people who do not — the question builder produces real queries from
clicks, and the model layer hides joins so that "revenue by region last quarter" does not
require knowing the schema.

That is the whole reason to choose it. For a data platform whose consumers are not analysts,
it is the difference between dashboards existing and not.

It is also **cheap to run**: a single service and a metadata database.

## When to use it

- **business users** need to answer their own questions
- cost matters — it is inexpensive to operate and the open-source edition is genuinely usable
- fast time to first dashboard

## When not to use it

- you need deep customisation, unusual chart types or heavy control — [Superset](../superset/README.md)
- dashboards should be **code**, reviewed in pull requests — [Evidence](../evidence/README.md)
- dbt should own the metric definitions — [Lightdash](../lightdash/README.md)

---

## Notes

### There is no official Helm chart

<https://github.com/metabase/metabase/issues/13581>

The community chart above is what most deployments use. Worth knowing before planning a GitOps
rollout, since it means depending on a third-party chart for a core tool.

### Limitations worth reading before committing

- [Serialization](https://www.metabase.com/docs/latest/installation-and-operation/serialization) — exporting and importing content between instances. This is how dashboards move between environments, and its constraints shape whether that is practical
- [Configuration file](https://www.metabase.com/docs/latest/configuring-metabase/config-file) — what can be configured declaratively, which decides how much of it fits GitOps
- [Caching](https://www.metabase.com/docs/latest/configuring-metabase/caching) — matters as soon as dashboards are refreshed by many people against a warehouse that bills per query

The serialization one is the most consequential. "How do dashboards get from staging to
production" has a real answer here, and it is not as smooth as manifests.

---

[← Visualisation](../README.md)
