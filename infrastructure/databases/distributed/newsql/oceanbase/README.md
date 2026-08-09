[← NewSQL](../README.md)

# OceanBase

<https://github.com/oceanbase/oceanbase>
<https://github.com/oceanbase/ob-operator>

---

## What it is

A distributed relational database built at Ant Group, and proven at a scale most of this folder
cannot claim: it runs Alipay, and it holds TPC-C results at the top of that benchmark.

| Property | Detail |
|---|---|
| **Compatibility** | MySQL **and** Oracle dialects |
| Consensus | Paxos, per partition |
| **Multi-tenancy** | first-class — tenants isolated inside one cluster |
| HTAP | row and columnar storage in one engine |
| Scale | proven at financial-transaction volume |
| Licence | Apache 2.0 (community edition) |

**Oracle compatibility** is the genuinely rare capability. Migrating off Oracle is otherwise a
rewrite, and a database that accepts PL/SQL and Oracle-dialect queries changes that calculation
substantially. For organisations with an Oracle estate and a licensing problem, that is the
reason to look at it.

The multi-tenancy model is also unusual: tenants are a real construct inside the cluster with
their own resources and isolation, rather than a naming convention over schemas.

## When to use it

- **migrating away from Oracle**, where dialect compatibility is the blocker
- very large scale, in a context where its production record is reassuring
- multi-tenancy as a database-level construct rather than an application concern
- HTAP with MySQL compatibility, as an alternative to [TiDB](../tidb/README.md)

## When not to use it

- **the ceiling has not been measured** — the standard warning in
  [`../README.md`](../README.md#2-the-cost-stated-first) applies
- PostgreSQL compatibility is what matters — [YugabyteDB](../yugabytedb/README.md)
- the documentation and community are a practical obstacle — see below
- a smaller operational surface is preferred

## Notes

Recorded plainly in the original notes:

> Too Chinese.

That is a blunt phrasing of a real evaluation criterion, and it is worth stating properly rather
than dismissing.

OceanBase's documentation, its issue tracker, its community discussions and most of the
operational knowledge around it are **primarily in Chinese**. The English documentation exists and
lags: it is thinner, updated later, and covers less of the operational surface.

For a database that would sit at the centre of a platform, that is a substantive adoption risk
rather than an inconvenience:

| Consequence | Detail |
|---|---|
| **Troubleshooting** | the answer to an obscure failure is likely to exist, in a language the team may not read |
| Documentation lag | English docs cover the happy path more than the edge cases |
| Community support | asking a question means asking in a forum where the working language differs |
| Hiring | very few engineers outside China have operated it |

None of that is a criticism of the software, which is genuinely impressive engineering with a
production record most of this folder lacks. It is a statement about **operability by a given
team** — which is a legitimate and frequently decisive selection criterion, and the same one that
would apply in reverse to an English-only project being adopted by a team that does not read
English.

The same consideration applies in a milder form to several projects in this catalogue with a
primary community outside the English-speaking world.

Nothing here is deployed. OceanBase is catalogued as the **Oracle-compatible** option, which is
the one thing in [`newsql/`](../README.md) nothing else provides.

---

[← NewSQL](../README.md)
