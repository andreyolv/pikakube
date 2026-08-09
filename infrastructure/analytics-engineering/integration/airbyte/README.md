[← Integration](../README.md)

# Airbyte

<https://github.com/airbytehq/airbyte>
<https://github.com/airbytehq/airbyte-platform>
<https://docs.airbyte.com/>

---

## The problem it solves

Every source system speaks a different protocol, paginates differently, handles incremental
reads differently, and breaks differently. Writing a connector per source is a project; writing
thirty is a team.

Airbyte is a **connector catalogue** with a runtime attached — hundreds of sources and
destinations, each a container implementing a standard protocol, with sync scheduling, state
management and normalisation handled centrally.

The design consequence worth knowing: **connectors are containers**. That is why the catalogue
is large and why a custom connector is achievable — it is a program that speaks a defined
protocol on stdout, not a plugin inside a framework.

## When to use it

- many heterogeneous sources, and connector coverage is the constraint
- a new source should take hours, not a sprint
- **small distributed teams** — the UI means adding a source does not require the data platform team
- you want EL only, with transformation left to [dbt](../../transform/dbt/README.md)

## When not to use it

- very high volume, where per-connector container overhead becomes the cost — [SeaTunnel](../seatunnel/README.md)
- the source is PostgreSQL and CDC latency matters — [PeerDB](../peerdb/README.md) is specialised for it
- streaming ingestion — [`data-streaming/`](../../../data-streaming/README.md)

## Before committing to a source

The questions that decide whether a connector is viable in production, rather than in a demo:

| Check | Why |
|---|---|
| Does it support **incremental** sync? | full refresh of a large table has a ceiling you will hit |
| What is the cursor field? | it decides whether resumption is correct after a failure |
| How does it handle **schema drift**? | sources add columns without warning |
| What happens mid-sync on failure? | a partial load is worse than no load |

Incremental support is the one to verify first. Connector quality varies substantially across
the catalogue, and the difference is usually here.

---

## Notes

Open issues worth reading before depending on specific behaviour:

- <https://github.com/airbytehq/airbyte-platform/pull/361>
- <https://github.com/airbytehq/airbyte/issues/64156>
- <https://github.com/airbytehq/airbyte/issues/65137>
- <https://github.com/airbytehq/airbyte/issues/12338>

---

[← Integration](../README.md)
