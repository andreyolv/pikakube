[← Agents](../README.md)

# kagent

<https://github.com/kagent-dev/kagent>

---

## The problem it solves

Every framework in this folder that you *import* — CrewAI, LangGraph, Swarm — leaves the same
question unanswered: where does the agent run, who restarts it, where do its credentials come
from, and how does anyone other than its author change it?

kagent answers that by making agents **Kubernetes objects**. An `Agent`, a `ModelConfig` and a
`ToolServer` are CRDs; a controller reconciles them. The agent's system prompt, its model, and
the tools it may call are declarative resources in Git, reconciled like everything else on the
cluster.

What that buys is not intelligence — it is operations:

| Concern | How it is handled once agents are CRDs |
|---|---|
| Deployment | GitOps, the same as every other workload |
| Credentials | Kubernetes Secrets, and whatever already fills them |
| Access control | RBAC on the CRDs — who may edit an agent is a normal question |
| Observability | a controller exposing metrics, not a script someone runs |
| Tools | `ToolServer` resources, MCP-based, shared between agents |

Its origin explains its bias: kagent came out of the Solo.io / service-mesh world and is aimed
squarely at **platform and SRE use cases** — an agent that can query Prometheus, read Kubernetes
resources or inspect an Istio config, running inside the cluster it is reasoning about. That is
the use case it is best at, and it is a narrower claim than "agent platform".

## When to use it

| Situation | Why kagent fits |
|---|---|
| Agents should be operated like workloads, not like scripts | CRDs, controller, GitOps, RBAC |
| The agent's job is cluster-facing — triage, diagnostics, querying observability | that is the ecosystem it comes from |
| Multiple teams need to define agents without each building a service | the CRD is the interface |
| Tools should be shared and centrally governed | `ToolServer` plus MCP, rather than per-application plugin code |

## When not to use it

| Situation | Use instead |
|---|---|
| The agent is a feature inside one product application | a library — [LangGraph](../langgraph/README.md) or [CrewAI](../crewai/README.md) — in that application's image |
| The flow needs precise, branching, resumable control | LangGraph; a CRD is a declaration, not a state machine |
| It is business workflow automation with SaaS connectors | [n8n](../n8n/README.md) |
| You are not on Kubernetes | the entire premise does not apply |
| You want a mature, settled platform | this is a young project; see the notes below |

The genuine risk is the one that applies to every Kubernetes-native wrapper: you inherit the
project's release cadence and its idea of what an agent is. When the CRD does not express what
you need, there is no gradual escape — you rewrite as an application.

## Notes

The only thing recorded for kagent in the original notes was the project URL:

- <https://github.com/kagent-dev/kagent>

Everything below is read from the manifests already in this folder, and they say more than the
note did.

**It is deployed, and it is deployed from a release candidate.** Flux pulls two OCI Helm charts,
`kagent-crds` and `kagent`, both pinned at tag `0.10.0-rc1` with an explicit digest, into the
`kagent` namespace. The CRD chart is a separate `HelmRelease` that the main one `dependsOn`, and
it upgrades CRDs with `CreateReplace`. Pinning by digest is right; running a release candidate
is a deliberate trade — the project moves fast and the stable tag lags the features. It is worth
knowing that is the position, rather than discovering it during an incident.

**The database is external, not bundled.** `database.postgres.bundled.enabled` is `false`, and
the connection URI is injected from the `postgres-app` Secret into `database.postgres.url`. The
`postgres/` folder next to the Helm manifests holds a CloudNativePG `Cluster`, an
`ExternalSecret` and a password resource. This is the correct shape: the chart's bundled
database is a convenience for demos, and using the cluster's real PostgreSQL operator means
kagent's state gets the same backup and failover story as everything else.

**The default model provider is Ollama, in-cluster.** `providers.default` is `ollama`, the model
is `llama3.2`, and the host is `http://ollama.ollama.svc.cluster.local:11434` — the
[Ollama](../../llm/ollama/README.md) deployment in this repository. So the whole path is
self-hosted: no external provider key, no data leaving the cluster. That is a real property and
worth naming. The cost of it is equally real — `llama3.2` is a small model, and small models are
noticeably weaker at multi-step tool use than the frontier hosted ones. Expect the ceiling on
what these agents can reliably do to be set by the model, not by kagent.

**Controller metrics are enabled** (`controller.metrics.enabled: true`), which means the
controller can be scraped like any other operator. That is the minimum bar for treating agents
as operated software rather than as experiments.

---

[← Agents](../README.md)
