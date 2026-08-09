[← Query engine](../README.md)

# Presto

<https://github.com/prestodb/presto>
<https://github.com/prestodb/presto-helm-charts>
<https://prestodb.io/>

---

## What it is

The original federated SQL engine, created at Facebook. **Trino forked from it in 2019** when
the original creators left — the fork was called PrestoSQL and was renamed Trino in 2020.

Both projects continue. They share an origin and have diverged since.

| | Presto (prestodb) | Trino |
|---|---|---|
| Backing | Meta, Linux Foundation | Starburst, Trino Software Foundation |
| Momentum | steadier, enterprise-oriented | faster-moving, larger community |
| Cloud | the engine behind AWS Athena | broad ecosystem adoption |
| Connectors | many | more, and more actively developed |

## When to use it

- an **existing Presto deployment** that works
- alignment with the Meta or Linux Foundation lineage matters
- AWS Athena is in the picture, which is Presto-derived — worth understanding the shared behaviour

## When not to use it

- **starting fresh.** Trino has the larger community, more connectors and more written material, which is where most new deployments go
- you want the most active development on the features that matter to a lakehouse

## Why it is mapped here

Two practical reasons rather than nostalgia.

**Athena is Presto.** Understanding Presto's behaviour explains Athena's — its limits, its
query patterns, and why certain things are slow. This repository documents
[Athena cost auditing](../../../cloud-computing/aws/), and the engine underneath is this one.

**The fork is frequently confusing.** Documentation, blog posts and Stack Overflow answers from
before 2020 refer to "Presto" and may apply to either. Knowing where the split happened is what
makes older material usable.

## Related

[Trino Gateway](../trino-gateway/README.md) is Trino-side. For Presto, the equivalent routing and
isolation concerns exist and are addressed differently.

---

[← Query engine](../README.md)
