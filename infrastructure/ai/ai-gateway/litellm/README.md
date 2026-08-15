[← AI gateway](../README.md)

# LiteLLM

<https://github.com/BerriAI/litellm>

<https://docs.litellm.ai>

The one option in this folder that is not a proxy borrowed from the network stack. It is an
application built for exactly this job — and it is the only one that answers *"who spent what"*
without a project of your own.

---

## Two products, one name

Read this before anything else, because the two are confused constantly and only one of them is
infrastructure. It is the same split [`agents/`](../../agents/README.md#2-three-different-things-live-in-this-folder)
makes between libraries you import and platforms you deploy:

| | **The SDK** | **The proxy (the gateway)** |
|---|---|---|
| What it is | a Python package your application imports | a service you deploy and everything calls |
| Who decides to use it | the application team | the platform team |
| What it gives you | one call signature across 100+ providers, retries, fallbacks, cost calculation | all of that, plus keys, budgets, rate limits, spend attribution, an admin UI |
| State it needs | none | **PostgreSQL** for keys and spend, **Redis** for caching and shared rate limits |
| Blast radius | one application | every model call in the organisation |
| Belongs in this folder? | catalogued for comparison | **yes — this is the gateway** |

The rest of this page is about the proxy. The SDK is a reasonable dependency for one application
and needs no platform decision; the day two teams both need it, the argument in
[§1](../README.md#1-the-problem-precisely) starts applying and the proxy is what it points at.

## The problem it solves

It is the same list as [§2](../README.md#2-what-a-gateway-centralises) — one credential store, one
API shape, routing, failover, caching, limits, attribution — with a different emphasis from the
Envoy-derived options. LiteLLM's centre of gravity is **the accounting**, not the dataplane:

| Capability | What it actually gives you |
|---|---|
| **Virtual keys** | a key per team, per application, per user, minted and revoked in the gateway. Provider keys stay in one place and no application ever holds one |
| **Budgets** | a hard spend limit attached to a key or a team, enforced in tokens and currency, with the request refused when it is exceeded |
| **Spend tracking** | per key, per model, per request, in a database you can query — the answer to the unallocated invoice |
| **Rate limits** | per key, in requests **and tokens**, shared across replicas through Redis |
| **Routing and fallbacks** | model aliases across deployments, retries, and failover to another provider when one degrades |
| **Caching** | exact-match and semantic caching in Redis — the [cost lever](../README.md#4-caching-the-real-cost-lever) |
| **Callbacks** | every request logged to [Langfuse](../../agents/langfuse/README.md), OpenTelemetry, S3 and others without touching application code |
| **Admin UI** | keys, teams, budgets and spend, managed by people who will not be writing YAML |

**Virtual keys plus budgets is the feature that decides adoptions.** Everything else in this folder
can route and can fail over; nothing else here hands a team a key with a monthly ceiling attached
and shows them what they spent. If the pain is *"the bill is one number and nobody can decompose
it"*, this is the tool that answers it directly.

Provider breadth is the second reason: 100+ providers behind an OpenAI-shaped API, covering
`/chat/completions`, `/embeddings`, `/images`, `/audio`, `/rerank` and batch endpoints. That
includes the self-hosted end — [vLLM](../../llm/vllm/README.md) and
[Ollama](../../llm/ollama/README.md) are just more backends — which is what makes *"hosted API,
second hosted API for fallback, and a model on the cluster"* one client instead of three.

## When to use it

- **cost attribution and budgets are the actual requirement.** This is the case where LiteLLM is not
  competing with the other options; it is the only one that does the job
- many providers, and applications that should not know which one they are talking to
- you want **per-team keys** the platform can revoke, instead of provider credentials copied into
  each application's secrets
- you want request-level observability into [Langfuse](../../agents/langfuse/README.md) or OTel
  without an application change
- **a self-hosted model and a hosted API should look identical** to callers
- you are already running Postgres and Redis, so the state it needs is not a new operational
  commitment

## When not to use it

- **two applications and one provider.** The gateway is on the critical path of every model call;
  the counter-argument in [§1](../README.md#1-the-problem-precisely) applies with full force
- when you already run **Gateway API** and want the AI gateway to be part of it —
  [Envoy AI Gateway](../envoy-ai-gateway/README.md) is the answer there, and it is the folder's
  default for that reason
- when the requirement is **infrastructure-grade**: an existing proxy fleet, the latency profile of a
  C++/Go dataplane, and no new stateful component. LiteLLM is an application with a database, and
  that is a different operational shape
- when the traffic is **agent-to-agent and MCP** rather than provider calls — that is
  [agentgateway](../agentgeteway/README.md)
- if you cannot accept a **Python-ecosystem service on the hot path**. This is a real consideration
  at high request rates, and the project's own work on a Rust core exists because of it
- when the features you want turn out to be the **enterprise ones** — see the notes

## The trade, stated plainly

| | **LiteLLM** | **Envoy AI Gateway** |
|---|---|---|
| What it is | a purpose-built application | an extension of a proxy you may already run |
| Keys, budgets, spend | **its main event** | not its job |
| Provider coverage | the broadest available, by a distance | the major providers |
| State required | Postgres + Redis | none of its own |
| Fits Gateway API | no — it is a separate service with its own API | **yes, natively** |
| Operational character | an app to run, upgrade and debug | configuration on existing infrastructure |
| Failure mode | your gateway is a Python service under load | your gateway is Envoy |

There is no universal answer here, and picking by feature count is how people end up operating a
database to route two applications. The question that resolves it: **is the problem the traffic, or
the money?** Envoy AI Gateway is the better answer for traffic. LiteLLM is the better answer for
money, and it is the more common problem.

## Notes

**Open source with an enterprise tier.** The core is open and genuinely capable; SSO, advanced
access control and several administrative features sit behind a commercial licence. That is a fair
model and it is worth establishing *before* an adoption, because the features most likely to be
required by the security review — single sign-on and fine-grained user management — are on the paid
side of the line. Check the current split against your actual requirements rather than against the
feature list.

**It is stateful, and that changes the operational story.** Postgres holds keys, teams and spend;
Redis holds the cache and the shared rate-limit counters. Losing Postgres does not merely degrade
the gateway — it takes the key store with it, which means backups, an upgrade path and a restore
test. Nothing else in this folder asks for that, and it is the honest cost of the accounting
features.

**A gateway that fails closed is an outage for everything.** True of any option here
([§9](../README.md#9-anti-patterns)), sharper for this one because the dependency chain is longer:
gateway → Postgres → Redis → provider. Run more than one replica, and decide deliberately what
should happen when the database is unreachable — refusing every request and serving requests without
tracking spend are both defensible, and both need to be chosen rather than discovered.

**Provider translation is maintenance, not magic.** Mapping 100+ providers onto one API shape means
tracking each provider's changes, and the mapping is occasionally behind or subtly lossy for
provider-specific features — reasoning parameters, cache controls, structured output. Pin the
version, and test the two or three providers you actually use after every bump.

**Where this fits in pikakube.** The decision here is already partly made and is worth stating
against, not around: [Envoy AI Gateway](../envoy-ai-gateway/README.md) is deployed at `v0.6.0` with
empty values, kgateway is deployed alongside it, and **no traffic goes through either** — the state
recorded in [§10](../README.md#10-how-this-applies-to-pikakube). That section also names the first
thing worth configuring: **cost attribution**, ahead of routing or failover, using the self-hosted
[Ollama](../../llm/ollama/README.md) backend and [kagent](../../agents/kagent/README.md) as the
first traffic.

That is precisely the requirement LiteLLM is built around and the one Envoy AI Gateway is weakest
at, which makes this the tension to resolve deliberately rather than by accumulation. Two gateway
control planes are already installed for overlapping jobs; **a third component is the wrong answer
to a folder that has too many.** The right reading of this page is as the fallback: configure token
accounting on what is deployed, and if it cannot answer *who spent what* per team with a budget
attached, LiteLLM is what replaces it — not what joins it.

---

[← AI gateway](../README.md)
