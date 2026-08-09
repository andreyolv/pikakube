# infrastructure/

The capability catalogue — the core of this repository.

## Contents

1. [How this folder is organised](#1-how-this-folder-is-organised)
2. [The disciplines](#2-the-disciplines)
3. [Where the boundaries are](#3-where-the-boundaries-are)
4. [How to read a folder](#4-how-to-read-a-folder)
5. [What is not here](#5-what-is-not-here)

---

## 1. How this folder is organised

Three levels, and **one axis per level**:

```
infrastructure/<discipline>/<capability>/<tool>/
```

| Level | Answers | Example |
|---|---|---|
| **Discipline** | which engineering domain owns this? | `databases/` |
| **Capability** | which problem is being solved? | `databases/tooling/pooler/` |
| **Tool** | which implementation? | `.../pooler/postgres/pgbouncer/` |

Two rules follow from that, and they are what keep the tree navigable:

**A folder is named for the problem, not the vendor.** `connection pooling`, not `pgbouncer-and-friends`. That is why a tool can be replaced without renaming anything around it.

**Tools are filed by where they shine, not by everything they can do.** Trivy scans images, filesystems, IaC and Kubernetes manifests; it lives under container scanning because that is what it is reached for. Playwright is a browser automation framework and sits in `web-scraping/` because that is how it is used here. Filing by full capability would put half the catalogue in three places at once.

## 2. The disciplines

| Discipline | What it covers |
|---|---|
| [`platform-engineering/`](platform-engineering/README.md) | the cluster itself — GitOps, IaC, IDP, and Kubernetes local/managed/on-premise |
| [`devops/`](devops/README.md) | the path from source to running workload — CI/CD, images, templating, registries, cleanup |
| [`security/`](security/README.md) | five rings, outermost to innermost — governance, cloud, cluster, container, code |
| [`network/`](network/README.md) | the pod dataplane up to API management — CNI, DNS, ingress, service mesh, certificates |
| [`observability/`](observability/README.md) | metrics, logs, traces, profiles and events — and what to do when one fires |
| [`site-reliability-engineering/`](site-reliability-engineering/README.md) | keeping it running — SLOs, chaos, progressive delivery, backup, storage |
| [`databases/`](databases/README.md) | SQL, NoSQL, distributed and analytical stores, plus the tooling that decides whether they survive |
| [`data-engineering/`](data-engineering/README.md) | orchestration, processing and query engines |
| [`data-streaming/`](data-streaming/README.md) | event log, stream processing, schema registry, real-time OLAP |
| [`data-governance/`](data-governance/README.md) | catalogue, lineage, quality, contracts and the lakehouse substrate |
| [`analytics-engineering/`](analytics-engineering/README.md) | transformation, semantic layer, notebooks and visualisation |
| [`software-engineering/`](software-engineering/README.md) | the application layer — APIs, messaging, serverless, testing, code quality |
| [`mlops/`](mlops/README.md) | the model lifecycle — experiment, track, register, deploy, monitor |
| [`ai/`](ai/README.md) | the AI application layer — LLM serving, agents, gateways, MCP |
| [`finops/`](finops/README.md) | cost visibility and optimisation |
| [`docs/`](docs/README.md) | documentation as code — site generators, diagrams, ADRs, API contracts |
| `cloud-computing/` | AWS and Azure services, and local emulators |
| `management/` | ways of working |

The last two are **not yet documented to this pattern** — they still hold `doc.md` notes.

## 3. Where the boundaries are

Several capabilities have neighbours in another discipline, and the boundary is the thing worth
writing down — otherwise the same tool gets evaluated twice under two names.

| Question | Here | Not here |
|---|---|---|
| Asynchronous work | [`software-engineering/messaging/`](software-engineering/messaging/README.md) — a broker delivers and forgets | [`data-streaming/`](data-streaming/README.md) — a log retains and replays |
| "Catalog" | [`data-governance/metadata-catalog/`](data-governance/metadata-catalog/README.md) — query engines ask it where the files are | [`data-governance/platform/`](data-governance/platform/README.md) — people ask it what the data means |
| Source code analysis | [`software-engineering/code-quality/static-analysis/`](software-engineering/code-quality/static-analysis/README.md) — is it maintainable? | [`security/4-code/sast/`](security/4-code/sast/README.md) — is it exploitable? |
| Time-series | [`databases/nosql/timeseries/`](databases/nosql/timeseries/README.md) — measurements that are *data* | [`observability/metrics/`](observability/metrics/README.md) — metrics *about the platform* |
| Model work | [`mlops/`](mlops/README.md) — the lifecycle | [`ai/`](ai/README.md) — the serving and application layer |
| Registries | [`devops/image/oci-registry/`](devops/image/oci-registry/README.md) — images and charts | [`software-engineering/artifact-registry/`](software-engineering/artifact-registry/README.md) — language packages |
| Scaling on events | [`devops/event-driven/`](devops/event-driven/README.md) — scale an existing workload | [`software-engineering/serverless/`](software-engineering/serverless/README.md) — a function platform |
| Certificates | [`security/2-cluster/certificates/`](security/2-cluster/certificates/README.md) — PKI and issuance | [`network/`](network/README.md) — where they get terminated |

The first row is the one that costs most when it is confused: adopting Kafka because "we need
queues" brings partitions, retention and consumer groups to solve a problem a broker solves with
none of them.

## 4. How to read a folder

Every folder carries a `README.md`, and there are two shapes.

**A capability README** — the problem, a decision tree, an anti-patterns table, and a section on
how it applies to this platform. Read this first; it is where the trade-offs are.

**A tool README** — the upstream links, what problem it solves, when to use it, when *not* to use
it, and a `## Notes` section.

**The `## Notes` sections are the part worth reading.** They carry what was found by actually
deploying the thing: charts that do not install, documentation that is wrong, projects that have
stalled, and defects in the manifests in this repository. That is the difference between this
catalogue and a list of landing pages — every tool here claims to solve its problem, and the
notes record which ones did.

Some recurring findings, as an illustration of what is in them:

- Helm charts that do not install their own CRDs before the resources that use them
- projects that are dead but still appear high in search results
- documentation that is complete for the happy path and absent for object-storage integration
- OCI packaging gaps that matter specifically in a Flux-based setup

## 5. What is not here

**Decisions.** This folder catalogues the solution space and explains the trade-offs. Which option
was chosen *for pikakube*, and why, is recorded only inside the "How this applies to pikakube"
sections — there are no ADRs. That gap is described in
[`docs/decision-record/`](docs/decision-record/README.md), which also lists the decisions that
would be worth writing down first.

**The cluster bootstrap.** That is [`clusters/`](../clusters/) — the Kind configurations and the
GitOps entry points.

**Anything running.** These are manifests and documentation. What is deployed at any moment is
whatever Flux has reconciled from them.

---

[← pikakube](../README.md)
