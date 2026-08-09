[← Sharing](../README.md)

# Delta Sharing

<https://github.com/delta-io/delta-sharing>

---

## The problem it solves

An **open protocol** for sharing data with someone outside your platform, without copying it and
without giving them credentials to your object storage.

The three things it is usually compared against are covered in [`../README.md`](../README.md);
the short version is that copying cannot be revoked, bucket credentials have no granularity or
audit, and building a query API means running a service that speaks a protocol only you implement.

Delta Sharing's mechanism removes most of the cost from the third option:

```
1. The PROVIDER runs a sharing server holding shares, schemas, tables and grants
2. The RECIPIENT presents a credential profile and asks for a table
3. The server authorises, then returns SHORT-LIVED PRE-SIGNED URLS
   for the Parquet files that make up the table
4. The recipient reads those files DIRECTLY from object storage
```

| Property | Why it follows |
|---|---|
| **No copy** | the recipient reads the provider's files in place |
| **Revocable** | drop the grant and the next request fails; issued URLs expire on their own |
| **Auditable** | every request passes the grant check on the server |
| **Granular** | grants are per share, schema and table — not per bucket |
| **The server does not carry the data** | it issues URLs; the bytes move from object storage directly |
| **Recipient needs nothing special** | see below — this is the underrated part |

**The server not being in the data path is the design's best property.** A modest service can serve
very large tables, because it never touches a byte of them. It scales with the number of grant
requests, not with data volume.

## The recipient does not need Databricks or Spark

This is the point most often missed. The recipient side is a **credential profile file** — a small
JSON `.share` file with an endpoint and a bearer token — plus any client that implements the
protocol.

| Recipient has | Can read a share |
|---|---|
| Python and pandas | **yes** — the reference connector loads a table into a DataFrame |
| [Spark](../../../../data-engineering/processing/spark/README.md) | yes, as a data source |
| Neither, but can make HTTPS requests | yes — it is a documented REST protocol over Parquet files |
| Databricks | yes, and this is where it came from |

The protocol is open and the specification is public, so *"can our partner read this"* has a good
answer without a procurement conversation. Compare a vendor sharing feature, where the answer is
"they can if they buy the same product".

## When to use it

- an **external** party needs ongoing access to a dataset that must stay current
- revocation is a requirement — a contract ends, a partnership does
- the recipient's tooling is unknown or outside your control
- there would otherwise be one bespoke export pipeline per partner
- the alternative on the table is copying files, which is the option that cannot be undone

## When not to use it

- the consumer is **internal** — that is a catalog and permissions problem; see
  [`metadata-catalog/`](../../../metadata-catalog/README.md)
- a genuine one-off extract that will never be refreshed; an export is less machinery, provided
  everyone understands it is permanent
- row- or column-level policies are the actual requirement — grants here are per table, so share a
  curated view instead, and see [`anonymization/`](../../../anonymization/README.md)
- there is no appetite to run a **public-facing authenticated service**, which is what this is
- the tables to be shared are [Iceberg](../../table-formats/iceberg/README.md) — see the notes

## What it costs to run

Worth being explicit, because "no copy, no credentials" makes it sound free:

| Concern | Detail |
|---|---|
| **A public endpoint** | the sharing server is reachable from outside; it is production infrastructure with an authentication surface |
| **Pre-signed URL expiry** | short-lived, but a leaked URL is readable until it expires |
| Object storage reachability | the recipient fetches files directly, so the storage endpoint must be reachable too, not just the server |
| **Egress** | not copying does not mean not paying; the bytes still leave |
| Grant lifecycle | grants outlive the reason they were created unless someone reviews them |
| Table maintenance | a shared table still needs compaction and snapshot expiry — see [`table-formats/`](../../table-formats/README.md) |

The reachability row catches people. The elegant part of the design — the server hands out URLs and
the recipient reads storage directly — means **object storage itself must be reachable by the
recipient.** For a self-hosted [MinIO](../../storage/minio/README.md) behind a cluster boundary,
that is a networking decision, not a configuration flag.

## Notes

Recorded reference:

- [delta-io/delta-sharing](https://github.com/delta-io/delta-sharing)

Nothing is deployed. What exists in this repository is on the consuming side: the
[Delta notebooks](../../table-formats/delta/notebooks/README.md) include a Delta Sharing walkthrough
against a public share profile, which is the cheapest possible way to understand the protocol —
read someone else's share before deciding whether to publish one.

**The caveat that matters for this platform.** The protocol is named for Delta and was built around
the Delta transaction log, while the recorded direction across [`lakehouse/`](../../README.md) is
**Iceberg on MinIO**. Sharing Iceberg tables through it is not the default path, and protocol
support for formats beyond Delta has moved over time — verify against the current specification and
the specific server and client versions before assuming it drops in. The
[UniForm](../../interoperability/uniform/README.md) route exists in the opposite direction (a Delta
table readable as Iceberg), which does not help here.

**The reason to keep the folder anyway** is the one in [`../README.md`](../README.md): when an
external sharing request arrives without preparation, the answer is always a copy, and a copy is
the single option that cannot be revoked. Knowing the mechanism in advance is most of the value,
whether or not this specific implementation is the one that gets used.

---

[← Sharing](../README.md)
