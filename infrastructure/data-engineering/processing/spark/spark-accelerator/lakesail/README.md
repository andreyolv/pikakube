[← Spark accelerators](../README.md)

# LakeSail

<https://github.com/lakehq/sail>

---

> **Not an accelerator.** Everything else in this folder speeds up Spark. Sail is a **separate
> engine** that speaks a Spark-compatible API — a replacement, not a plugin.

## What it is

A Rust engine implementing the Spark Connect protocol, so PySpark code can point at it instead
of at a Spark cluster. The claim is substantially better single-node and small-cluster
performance, without the JVM.

The bet is different from the accelerators: rather than making Spark's execution faster, it
removes Spark from the picture and keeps the API.

## Why that distinction matters

| | Accelerator | LakeSail |
|---|---|---|
| Spark runs | yes — plan, optimiser, ecosystem | **no** |
| Unsupported operators | fall back to the JVM | there is nothing to fall back to |
| Risk | slower than plain Spark if fallbacks dominate | **incompatibility**, with no safety net |
| Reward | incremental speedup | no JVM at all |

The absence of a fallback path is the whole risk. An accelerator degrades; a replacement either
supports what you use, or it does not.

## Open issues worth reading first

- <https://github.com/lakehq/sail/issues/172>
- <https://github.com/lakehq/sail/issues/982>

Compatibility is the thing to verify, and these are where its edges are being worked out.

## When it is interesting

- **small to medium** workloads currently running on Spark because that is what the code was written against
- the JVM footprint is the problem — startup time, memory, operational weight
- the code is plain PySpark with no unusual API surface

## When it is not

- large distributed workloads, which is what Spark is genuinely good at
- production dependence today, given the compatibility risk
- the code uses UDFs, unusual APIs or third-party Spark extensions

## The honest framing

Genuinely interesting, and a different question from the rest of this folder. Worth watching
and worth testing against a real job — and the alternative for the small-workload case is
already documented and mature: [DuckDB](../../../duckdb/README.md), which does not need Spark
compatibility at all.

---

[← Spark accelerators](../README.md)
