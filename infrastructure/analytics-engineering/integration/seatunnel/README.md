[← Integration](../README.md)

# Apache SeaTunnel

<https://github.com/apache/seatunnel>
<https://seatunnel.apache.org/>

---

## The problem it solves

[Airbyte](../airbyte/README.md) runs a container per connector, which is what makes its catalogue large
and what makes it expensive at volume. SeaTunnel takes the opposite position: **throughput
first**, running on its own engine (Zeta) or on Spark or Flink.

That makes it the answer when the constraint is how much data moves, rather than how many
different sources there are.

| | Airbyte | SeaTunnel |
|---|---|---|
| Optimised for | connector coverage and ease | **throughput** |
| Runtime | container per connector | Zeta, Spark or Flink |
| Interface | UI-first | configuration files |
| Batch and streaming | mostly batch | both, in one model |

## When to use it

- **volume is the constraint** — terabyte-scale movement where per-connector overhead matters
- Spark or Flink is already operated, so the runtime is not a new thing
- batch and streaming ingestion should use one tool and one configuration model

## When not to use it

- connector breadth is what you need, and adding sources quickly matters more than throughput
- a UI is required so that non-platform people can add sources
- there is no existing Spark or Flink, and Zeta is another runtime to learn

## Configuration as the interface

Pipelines are declarative files — source, transform, sink — which fits GitOps naturally and
makes review possible. The trade is that adding a source is a code change rather than a form,
which is the opposite of Airbyte's positioning.

Neither is better. It decides **who can add a source**, and that is an organisational question.

---

[← Integration](../README.md)
