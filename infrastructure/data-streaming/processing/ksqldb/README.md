[← Stream processing](../README.md)

# ksqlDB

<https://github.com/confluentinc/ksql>
<https://docs.ksqldb.io/>

Deployment variants: [`ksqldb/`](ksqldb/) · [`ksqldb-sasl/`](ksqldb-sasl/) ·
[`ksqldb-tls/`](ksqldb-tls/)

---

## What it is

SQL over Kafka topics. Streams and tables are declared in SQL, and the continuous queries run
as Kafka Streams applications underneath.

```sql
CREATE STREAM orders (id VARCHAR, amount DOUBLE)
  WITH (KAFKA_TOPIC='orders', VALUE_FORMAT='JSON');

CREATE TABLE revenue_by_region AS
  SELECT region, SUM(amount) FROM orders GROUP BY region
  EMIT CHANGES;
```

Its defining property is that it is **Kafka-native**: no separate cluster, no separate state
store, no additional system — the state lives in Kafka topics, and processing runs as Kafka
Streams.

## When to use it

- **Kafka is the whole world**, and adding another system is unattractive
- SQL is the interface the team wants
- transformations that stay within Kafka — topic in, topic out

## When not to use it

- results should be **queryable as tables** by external clients — [RisingWave](../risingwave/README.md) does that over the PostgreSQL protocol
- the estate is not Kafka-centric
- complex event-time semantics and large state — [Flink](../flink/README.md)
- stateless plumbing — [Benthos](../benthos/README.md)

## ksqlDB or RisingWave

The closest comparison, and the difference is where results live:

| | ksqlDB | RisingWave |
|---|---|---|
| State lives in | Kafka topics | its own storage |
| Results consumed by | Kafka consumers | **any PostgreSQL client** |
| Extra system | none | yes |
| Sources | Kafka | Kafka and others |

If everything downstream reads from Kafka anyway, ksqlDB adds nothing to operate. If dashboards
or applications need to **query** the results, RisingWave removes a serving layer.

## Licensing

ksqlDB is under the Confluent Community License, not Apache. Worth establishing early, since it
restricts offering it as a service and is a common reason teams choose otherwise.

---

## Notes

Done:

- Integrated with the Kafka ecosystem, with **TLS** enabled — [`ksqldb-tls/`](ksqldb-tls/)
- Integrated with the Kafka ecosystem, with **SASL** enabled — [`ksqldb-sasl/`](ksqldb-sasl/)

Both matter more than they look: ksqlDB authenticates to Kafka as a client, so a secured cluster
means the configuration has to carry through to every stream it creates.

---

[← Stream processing](../README.md)
