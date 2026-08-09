[← Event streaming](../README.md)

# Bufstream

<https://github.com/bufbuild/buf>
<https://github.com/bufbuild/protovalidate>
<https://buf.build/product/bufstream>

---

## The problem it solves

A [schema registry](../../schema-registry/README.md) is **advisory**. A producer that skips it
can publish anything, and the first sign of trouble is a consumer failing to deserialise —
after the bad data is already in the log, read by everyone else.

Bufstream moves validation into the **broker**. Messages that do not match the registered
schema are rejected at write time, so invalid data never enters the topic.

| | Conventional | Bufstream |
|---|---|---|
| Where schemas are checked | in the client, if it opts in | **in the broker** |
| A producer bypassing the registry | publishes anything | is rejected |
| Bad data discovered | by a failing consumer, later | at the write, immediately |
| Guarantee | convention | **enforced** |

That is a genuine difference in kind, not degree. "We have a schema registry" and "invalid
messages cannot exist in this topic" are different statements, and only the second is a
guarantee.

It is Kafka-protocol compatible, and built on object storage — so it also inherits the
elasticity properties of [AutoMQ](../automq/README.md).

## When to use it

- **data contracts must be enforced**, not merely documented — see [`data-governance/`](../../../data-governance/)
- Protobuf is the format, where Buf's tooling is strongest
- schema violations reaching consumers has already been a real incident

## When not to use it

- a conventional registry plus client discipline is sufficient — [Karapace](../../schema-registry/karapace/README.md) is open source and covers the common case
- Avro is the format; the Buf ecosystem is Protobuf-centred
- licensing and cost matter; check the terms before designing around it

---

## Notes

> The documentation is somewhat unclear.

Worth budgeting time for evaluation rather than assuming a quick assessment.

## The idea worth taking regardless

Even without adopting it, the principle applies: **a contract that is not enforced is
documentation**.

The same conclusion appears in [`schema-registry/`](../../schema-registry/README.md#the-structural-weakness)
and in [`data-governance/`](../../../data-governance/) — the enforcement point matters more than
the definition.

[protovalidate](https://github.com/bufbuild/protovalidate) is the related piece: validation
rules expressed **in** the Protobuf schema, so constraints travel with the contract rather than
living in each consumer.

---

[← Event streaming](../README.md)
