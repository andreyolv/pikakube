[← Data Streaming](../README.md)

# Platforms

Packaged and managed distributions of the streaming stack.

Tools covered: [`confluent-platform`](confluent-platform/README.md) ·
[`conduktor-console`](conduktor-console/README.md) · [`memphis`](memphis/README.md)

---

## What this folder represents

Everything else in [`data-streaming/`](../README.md) is a component you assemble: a broker, a
registry, a processing engine, a serving layer. This folder is the alternative — **buy the
assembly**.

The trade is the same one as in [`observability/platforms/`](../../observability/platforms/README.md):
less to operate, in exchange for licensing, lock-in and less control.

## The three, and they are not the same kind of thing

| Tool | What it actually is | Detail |
|---|---|---|
| **Confluent Platform** | the full commercial Kafka distribution — brokers, Schema Registry, Connect, ksqlDB, Control Center | [→](confluent-platform/README.md) |
| **Conduktor Console** | a **management and governance UI** on top of Kafka you already run | [→](conduktor-console/README.md) |
| **Memphis** | an alternative message platform with a developer-oriented interface | [→](memphis/README.md) |

**Conduktor is the one worth separating out.** It does not replace anything — it sits in front
of an existing Kafka and provides what operating Kafka lacks: topic browsing, consumer group
inspection, RBAC over Kafka operations, and a view non-specialists can use.

That is a different purchase from a platform. It solves the "only two people can safely operate
Kafka" problem without changing the broker.

## When a platform makes sense

| Situation | Reason |
|---|---|
| Kafka is critical and the team is small | operating it well is a specialisation, and outages are expensive |
| Connect, Schema Registry and ksqlDB are all needed | assembling and versioning them together is real work |
| Support obligations exist | someone accountable when the log stops |
| Many teams share the broker | governance and RBAC become the bottleneck, not throughput |

## When it does not

| Situation | Reason |
|---|---|
| Strimzi already works | the operator covers the operational case well, and free |
| Only the broker is needed | you would be licensing a stack to use one part |
| Licensing terms conflict with the platform's position | worth checking early, not at renewal |

## The middle path

Common and often correct: **open-source Kafka with Strimzi, plus a management UI**.

That keeps the broker unencumbered while addressing the real day-to-day pain — visibility and
safe access for people who are not Kafka specialists. Conduktor is the commercial option here;
lighter open-source UIs exist and cover browsing without the governance layer.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Adopting a platform for the broker alone | licensing a stack to use one component | Strimzi |
| Running a platform **and** self-managed Kafka | two operational models, unclear ownership | decide, then consolidate |
| A UI with unrestricted Kafka access | deleting a topic from a console is one click | RBAC on the UI as seriously as on the cluster |
| Assuming the UI is the governance | it shows and controls; policy still needs defining | governance as configuration, not as a screen |

## How this applies to pikakube

Kafka runs with **Strimzi**, self-managed, which is the right call for this repository — the
operator handles the operational case and there is no licensing question.

Confluent Platform is mapped with examples for comparison. The realistic gap this folder points
at is not the broker: it is that **Kafka has no usable interface for anyone who is not
operating it**, and a management console is the piece that would change who can work with it
safely.

---

[← Data Streaming](../README.md)
