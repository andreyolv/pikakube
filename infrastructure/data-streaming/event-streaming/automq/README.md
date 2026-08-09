[← Event streaming](../README.md)

# AutoMQ

<https://github.com/AutoMQ/automq>
<https://github.com/AutoMQ/charts>

---

## The problem it solves

The most painful part of operating Kafka is that **data lives on broker disks**. Scaling out
means moving partitions; a broker failure means re-replicating; and capacity planning means
sizing disks you cannot easily change.

AutoMQ keeps the Kafka protocol and replaces the storage layer with **object storage**. Brokers
become stateless.

| Consequence | Detail |
|---|---|
| **Scaling is instant** | add a broker, and it serves immediately — no partition movement |
| Failure recovery is fast | there is no data on the failed broker to re-replicate |
| Storage is elastic | S3 grows without capacity planning |
| **Cost drops substantially** | object storage against replicated local SSD, and no over-provisioning for peak |
| Kafka clients unchanged | it speaks the Kafka protocol |

The cost argument is the strongest one: Kafka's replication factor of three means three copies
on expensive disks, plus headroom. Object storage replaces all of it.

## When to use it

- **elasticity** matters — traffic varies enough that fixed capacity is wrong
- storage cost is a visible line item
- rebalancing pain is the reason Kafka is unpleasant to operate
- Kafka compatibility is required

## When not to use it

- **on-premise without object storage** — the whole design depends on it, and MinIO becomes a critical dependency underneath the log
- ultra-low latency at the tail; object storage adds latency that local disk does not have, mitigated but not eliminated
- you want the most established option; this is newer than the alternatives here

## The trade, stated plainly

Object storage in the write path is the entire bet. It buys elasticity and cost, and it makes
the log's durability depend on a service underneath it.

In a cloud that service is S3 and the trade is clearly good. On-premise it means
[MinIO](../../../site-reliability-engineering/storage/object-storage/minio/README.md) becomes load-bearing
for the event log — and that folder records why that category is in a difficult state right now.

## Related

Same architectural idea appears elsewhere: [Quickwit](../../../observability/logs/storage/quickwit/README.md)
for search, [Databend](../../../databases/analytical/databend/README.md) for warehousing. Separating
storage from compute on object storage is the recurring pattern of this generation of
infrastructure.

---

[← Event streaming](../README.md)
