[← MySQL poolers](../README.md)

# ProxySQL

<https://github.com/sysown/proxysql>

---

## The problem it solves

A proxy between applications and MySQL that does considerably more than pool connections — and
pooling is usually not why it is deployed.

| Capability | Why it matters |
|---|---|
| **Read/write splitting** | writes to the primary, reads to replicas, decided by the proxy |
| **Query routing** | rules by user, schema, or matched query pattern |
| **Query rewriting** | fix a pathological query at the proxy while it is patched properly |
| Query caching | identical repeated reads answered without touching MySQL |
| Failover awareness | routing follows the primary when it moves |
| Connection multiplexing | the pooling part |

**Read/write splitting is the usual reason.** Without a proxy, "use the replica for this query" is
a decision in application code — repeated in every service, implemented differently, and wrong in
at least one of them. Moving it to the proxy makes it configuration.

**Query rewriting is an incident tool.** Rewriting a bad query at the proxy buys the time to fix
it properly, without a deploy. It is genuinely useful and it is also how invisible behaviour
accumulates — a rewrite nobody remembers configuring, still active two years later.

## When to use it

- **read replicas exist**, and the application should not have to know about them
- failover should not require an application change
- connection counts are genuinely high — thousands rather than hundreds
- a proxy-level cache is a plausible answer to repeated identical reads

## When not to use it

- **MySQL is a source system** the platform reads from — which is the position here; see
  [`../README.md`](../README.md#how-this-applies-to-pikakube)
- one database, no replicas — it is a component with nothing to route
- the routing rules would exist only in the proxy, undocumented
- PostgreSQL — [PgCat](../../postgres/pgcat/README.md) does read/write splitting there

## The configuration problem

The thing to plan for before deploying it, because it undermines GitOps quietly.

ProxySQL is configured through a **MySQL-protocol admin interface at runtime**. Rules are inserted
into its internal tables, loaded to runtime, and saved to disk:

```sql
INSERT INTO mysql_query_rules (rule_id, match_pattern, destination_hostgroup, apply)
VALUES (1, '^SELECT', 2, 1);
LOAD MYSQL QUERY RULES TO RUNTIME;
SAVE MYSQL QUERY RULES TO DISK;
```

That is convenient and it means the live configuration is **runtime state**, not a manifest.
Without deliberate handling, it drifts from anything in Git immediately, and rebuilding the proxy
means reconstructing rules from memory.

Options, in order of preference:

| Approach | Detail |
|---|---|
| **Config file in a ConfigMap** | ProxySQL reads an initial config; keep it authoritative and treat runtime changes as temporary |
| Init container | applies rules from Git on startup |
| Accept the drift | only with an explicit export-and-commit habit, which nobody maintains |

## The availability point

ProxySQL sits in the path of **every query**. That makes it a single point of failure unless it is
deployed with the same care as the database it fronts:

- more than one instance, behind a Service
- its own metrics exported, or query latency becomes unattributable
- one more hop to consider when debugging

## Notes

Mapped as the MySQL answer in [`pooler/`](../../README.md).

For this platform it solves nothing today, and the reason is structural rather than technical:
MySQL appears here as a **source** — the application database data is extracted from via CDC or
dumps — rather than something the platform serves. There is no read fleet to balance and no
application traffic to route.

It is catalogued for the case where MySQL is being *served* rather than *read*, which is the point
at which read/write splitting stops being optional and starts being the thing that keeps the
primary alive.

---

[← MySQL poolers](../README.md)
