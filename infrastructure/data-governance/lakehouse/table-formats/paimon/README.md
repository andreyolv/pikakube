[← Table formats](../README.md)

# Apache Paimon

<https://github.com/apache/paimon>

---

## The problem it solves

A lake format built **streaming-first**, from the Flink community — it began life as Flink Table
Store before becoming a top-level Apache project.

The other formats in this folder added streaming capability to a batch design. Paimon starts from
the opposite end: the table is a **changelog** with a queryable current state, so streaming reads
and writes are the primary case rather than an extension.

| Capability | Detail |
|---|---|
| **Changelog as a first-class concept** | a streaming read consumes inserts, updates and deletes |
| **LSM-tree storage** | designed for high-frequency updates, unlike immutable-file formats |
| Primary keys | real upsert semantics, with merge engines to choose behaviour |
| Streaming and batch reads | over the same table |
| Deep Flink integration | it is the Flink ecosystem's answer |
| Spark and Trino support | present, and less mature than Flink's |

The LSM-tree choice is what separates it architecturally. Iceberg and Delta manage sets of
immutable files; Paimon maintains sorted runs that merge, which is a database's storage design
applied to a lake table — and it is why frequent small updates behave better here.

## When to use it

- **Flink is the processing engine**, which is the strongest reason
- the table is genuinely a stream: continuous upserts, consumed continuously
- a changelog stream out of the table is required, not just a snapshot
- streaming and batch must read the same table without a second copy

## When not to use it

- **Flink is not the engine** — Spark and Trino support exists and is thinner
- general analytical tables — [Iceberg](../iceberg/README.md) has far broader support
- **Azure or GCP object storage** — see the notes; this is a hard blocker
- the ecosystem matters: this is the youngest format here

## Notes

Recorded from actually trying it, and the findings are specific:

> Local — **OK**
>
> S3 and Hive — **the documentation is very poor**
>
> **No support for Azure and GCP**
>
> How do you connect S3 storage? Terrible docs, no example —
> [apache/paimon#1144](https://github.com/apache/paimon/issues/1144)

Two of those matter a great deal, in different ways.

**No Azure or GCP support** is not a documentation problem, it is a capability gap. For a platform
on either cloud, that ends the evaluation regardless of everything else. It is worth stating first
because it is the kind of thing discovered after a proof of concept rather than before one.

**S3 connection undocumented, with an open issue and no example** is the same failure recorded for
[Hudi](../hudi/README.md), and it confirms the pattern this folder keeps finding: **the format is
the easy part, and the object-storage integration is the least-tested path in these projects.**

"Local works" is the honest summary of where the evaluation got to. A lake format that works
against a local filesystem and not against the object storage the platform actually uses has not
been evaluated in any meaningful sense — and that is a statement about the project's maturity for
this use, not about its design.

## The honest position

Paimon's design is genuinely interesting and the right answer for a specific case: **Flink-first
streaming, on a supported storage backend**. In that context, having the changelog be the table
removes a whole layer of pipeline.

For this platform it is not viable today:
[MinIO](../../storage/minio/README.md) is S3-compatible storage, and the S3 path is the one with an
open issue and no working example. That is the blocker, and the multi-cloud gap makes it a poor
bet even if the S3 path were fixed.

[`../README.md`](../README.md#7-how-this-applies-to-pikakube) recommends
[Iceberg](../iceberg/README.md), which has documented S3 integration and the widest engine support.
Paimon is worth tracking — the streaming-first idea is sound, and the project is moving quickly.

---

[← Table formats](../README.md)
