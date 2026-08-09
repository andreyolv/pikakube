[← Spark](../README.md)

# Remote shuffle service

Tools covered: [`celeborn`](celeborn/README.md) · [`uniffle`](uniffle/README.md)

---

## The problem it solves

Between stages, Spark **shuffles**: every executor writes intermediate data to local disk, and
every other executor reads from it. That works on fixed clusters and breaks on Kubernetes.

| Consequence | Why |
|---|---|
| **Executors cannot scale down** | their local shuffle data is still needed by others |
| Losing an executor loses data | the stage recomputes, sometimes repeatedly |
| Local disk sizing becomes a constraint | large shuffles need large ephemeral volumes on every node |
| Spot instances are risky | a reclaimed node takes shuffle data with it |

The first row is the important one: **dynamic allocation does not really work without solving
this**, which removes the main reason to run Spark on Kubernetes in the first place.

A remote shuffle service moves that data off the executors into a separate, replicated service.
Executors become genuinely disposable.

## The tools

| Tool | Notes | Detail |
|---|---|---|
| **Apache Celeborn** | the more widely adopted option, originally from Alibaba | [→](celeborn/README.md) |
| **Apache Uniffle** | similar goal, from Tencent, with a pluggable storage backend | [→](uniffle/README.md) |

Both are Apache projects solving the same problem. Celeborn has more adoption; Uniffle is more
flexible about where shuffle data lands, including object storage.

## When this is worth adopting

- **dynamic allocation** is wanted, and executors must scale down mid-job
- **spot instances** run executors, where reclamation is routine
- shuffles are large enough that local disk sizing is a real constraint
- stage recomputation from lost executors is visible in job durations

## When it is not

- jobs are small and shuffles are trivial
- the cluster is fixed-size, where local shuffle is fine
- you are not yet running Spark at a scale where this shows

Adopting it before the pain exists is a distributed stateful service to operate, for a problem
nobody has measured.

## The honest note

Both are relatively immature operationally compared with Spark itself — see the deployment
problems recorded in [celeborn](celeborn/README.md). Worth knowing before committing: this
solves a real problem, and getting it running is not free.

---

[← Spark](../README.md)
