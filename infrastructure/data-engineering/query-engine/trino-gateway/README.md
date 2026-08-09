[← Query engine](../README.md)

# Trino Gateway

<https://github.com/trinodb/trino-gateway>
<https://trinodb.github.io/trino-gateway/>

---

## The problem it solves

One Trino cluster is a single point of failure and a single upgrade window. Restarting it kills
every running query, so upgrades mean an outage — and a heavy query from one team affects
everyone.

Running several clusters fixes that and creates a new problem: clients need one endpoint, not a
list.

Trino Gateway is that endpoint:

| Capability | Why it matters |
|---|---|
| **Single endpoint** | clients connect once; cluster topology changes behind it |
| Routing | by user, by source, by query characteristics |
| **Graceful draining** | a cluster stops accepting new queries and finishes the running ones — which is what makes zero-downtime upgrades possible |
| Load balancing | across clusters, rather than everything hitting one |
| Isolation | ad-hoc queries and scheduled ETL on separate clusters |

Draining is the feature that changes operations. Without it, "upgrade Trino" means "cancel
everyone's queries".

## When to use it

- **more than one Trino cluster**, which is the point at which it becomes necessary
- upgrades must not cancel running queries
- workload isolation — interactive users should not be affected by a heavy scheduled job
- routing by team or by query profile

## When not to use it

- one cluster and no plans for a second — it is a component with nothing to do
- the problem is one badly-behaved query rather than cluster contention; Trino's own resource groups address that within a cluster

## The pattern it enables

The arrangement most platforms end up wanting:

| Cluster | For |
|---|---|
| `interactive` | analysts and BI tools — smaller, tuned for latency |
| `etl` | scheduled jobs — larger, tuned for throughput |
| `adhoc` | exploration, where a bad query hurts nobody important |

The gateway routes by user or source, and each cluster is upgraded independently.

---

## Notes

Default credentials:

```
username: admin
password:
```

The blank password is the default. Worth changing before anything is exposed — this sits in
front of every query the platform serves.

---

[← Query engine](../README.md)
