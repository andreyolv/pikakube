[← Connection pooling](../README.md)

# MySQL poolers

Where the problem is smaller, and the tool that solves it does considerably more.

Tools covered: [`proxysql`](proxysql/README.md)

---

## Why this folder is short

MySQL handles connections with **threads**, not processes. A connection costs a thread and a
buffer rather than a full OS process, so the ceiling is an order of magnitude higher than
PostgreSQL's and the failure is gradual rather than abrupt.

| | PostgreSQL | MySQL |
|---|---|---|
| Per connection | a process | a thread |
| Practical ceiling | a few hundred | several thousand |
| Failure under pressure | hard refusal — `too many clients` | gradual degradation |
| Pooler | effectively mandatory | worth having, not urgent |

The consequence: on MySQL a pooler is rarely adopted *because of* connection exhaustion. It is
adopted for **routing** — and that is what ProxySQL is actually for.

## ProxySQL

It pools, and then it does the things a proxy positioned between application and database can
do:

| Capability | Why it matters |
|---|---|
| **Read/write splitting** | writes to the primary, reads to replicas, decided by the proxy rather than the application |
| **Query routing** | rules by user, schema, or query pattern |
| Query caching | identical repeated queries answered without touching the database |
| **Query rewriting** | a bad query fixed in the proxy while the application is patched properly |
| Failover awareness | routing follows the primary when it moves |
| Connection multiplexing | the pooling part |

Read/write splitting is the usual reason to deploy it. Without a proxy, "use the replica for
this query" is a decision in application code, repeated in every service and wrong in at least
one of them.

Query rewriting deserves a note as an **incident tool**: rewriting a pathological query at the
proxy buys the time to fix it properly, without a deploy. Useful, and equally a way to
accumulate invisible behaviour nobody remembers configuring.

## When to use it

- **read replicas exist** and the application should not have to know about them
- failover should not require an application change
- a proxy-level query cache is a plausible answer to repeated identical reads
- connection counts are genuinely high — thousands, not hundreds

## When not to use it

- MySQL is a **source system** the platform reads from, not something it serves traffic to.
  That is the usual position here — see [`../../../sql/mysql/`](../../../sql/mysql/README.md)
- there is one database and no replicas: it is a component with nothing to route
- the routing rules would live nowhere but in the proxy, undocumented

## The operational caution

ProxySQL sits in the request path of every query. That makes it a **single point of failure**
unless it is deployed with the same care as the database:

| Concern | What it means |
|---|---|
| Availability | more than one instance, behind a service |
| Configuration | its rules are runtime state in its own admin interface — capture them in Git |
| Observability | proxy metrics, or query latency becomes unattributable |
| Debugging | one more hop between the application and the answer |

The configuration row is the one that bites. ProxySQL is configured through a MySQL-protocol
admin interface at runtime, which is convenient and drifts from any manifest immediately unless
that is handled deliberately.

## How this applies to pikakube

MySQL appears in this repository primarily as a **source** — the application database a data
platform extracts from, via CDC or logical dumps, rather than one it serves.

In that position ProxySQL solves nothing: there is no read fleet to balance and no application
traffic to route. It is mapped here for the case where MySQL is being *served* rather than
*read*, which is the point at which read/write splitting stops being optional.

---

[← Connection pooling](../README.md)
