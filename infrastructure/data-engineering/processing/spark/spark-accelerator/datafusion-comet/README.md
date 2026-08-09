[← Spark accelerators](../README.md)

# Apache DataFusion Comet

<https://github.com/apache/datafusion-comet>

---

## What it is

A Spark accelerator built on [DataFusion](../../../../query-engine/datafusion/README.md), the Rust query
engine — offloading Spark's physical plan to native, vectorised execution.

Apache project, actively developed, and part of the broader DataFusion ecosystem that is
increasingly what other data tools are built on.

## The blocker for a lakehouse

> **Delta and Iceberg are not yet supported.**
>
> - <https://github.com/apache/datafusion-comet/issues/174>
> - <https://github.com/apache/datafusion-comet/issues/329>

For a platform built on either, that is decisive. [Gluten](../gluten/README.md) supports both, which
makes it the practical choice today regardless of how the engines compare.

Worth tracking: if these land, the comparison changes.

## When to use it

- plain Parquet on object storage, without a table format
- you want the DataFusion ecosystem, and Rust rather than C++ as the native engine
- evaluating where the technology is going, ahead of adopting it

## When not to use it

- Delta or Iceberg are in use — see above
- you need it working in production now; Gluten is further along for that case

---

## Notes

Build prerequisites:

```bash
sudo apt install openjdk-11-jdk
java -version

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Both toolchains are needed — JVM for the Spark plugin side, Rust for the native engine.

Background: <https://www.linkedin.com/feed/update/urn:li:activity:7211134200320565249/>

---

[← Spark accelerators](../README.md)
