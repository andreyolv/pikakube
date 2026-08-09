[← AI gateway](../README.md)

# Envoy AI Gateway

<https://github.com/envoyproxy/ai-gateway>
<https://aigateway.envoyproxy.io/docs/capabilities/mcp/>

---

This folder and [`envoyproxy/`](../envoyproxy/README.md) are **the same project**, split across
two directories — that one holds the GitHub link, this one holds the deployment and the
documentation link. Recorded as an observation; neither is removed here.

---

## The problem it solves

The generic problem is in the [parent folder](../README.md): many applications, many providers,
keys everywhere, no cost attribution. Envoy AI Gateway's specific answer is that **it is not a
new gateway**. It is an extension of Envoy Gateway, which means the control plane, the data
plane and the API are ones a platform team may already run.

That inheritance is the argument for it:

| It inherits | Consequence |
|---|---|
| **Gateway API** | routing is expressed in the same resources as the rest of the cluster's ingress |
| **Envoy** as the data plane | a proxy with a decade of production history, not new code on the request path |
| **Envoy Gateway's** control plane | one control plane for ordinary HTTP and for AI traffic |
| Envoy's observability | standard access logs, metrics and tracing, plus token-aware additions |

On top of that it adds the AI-specific pieces, which are the reason the project exists:

| Addition | What it does |
|---|---|
| **Unified API** | clients speak one OpenAI-shaped API; the gateway translates per provider |
| **Provider credentials** | keys live in the gateway, not in every application |
| **Token-based rate limiting** | limits on tokens, not requests — the only unit that reflects cost |
| **Failover across backends** | a provider outage routes elsewhere instead of failing |
| **MCP support** | fronting MCP servers, per the second link above |

**Token-based rate limiting is the feature that justifies a dedicated AI gateway.** A request
limit is meaningless when one request can consume a hundred tokens or a hundred thousand.
Everything else here could be approximated with an ordinary gateway and discipline; that one
cannot.

The MCP capability is newer and the reason the documentation link was recorded: the same gateway
that fronts model providers can also front MCP servers, so tool traffic and model traffic share
one policy and observability path. That overlaps with what
[agentgateway](../agentgeteway/README.md) does, from the opposite direction.

## When to use it

| Situation | Why this one |
|---|---|
| The cluster already runs Envoy Gateway or Gateway API | it is an extension, not a new system |
| Applications call more than one provider | the unified API and failover are the point |
| Cost must be attributed per team or per application | token metrics at the gateway, before the invoice |
| Self-hosted models and hosted APIs must look the same to callers | a [vLLM](../../llm/vllm/README.md) backend and a hosted provider behind one route |
| You want the boring choice | Envoy on the data path is the least exciting option available, which is the compliment it sounds like |

## When not to use it

| Situation | Use instead |
|---|---|
| One application, one provider | the provider SDK. A gateway is infrastructure to operate |
| You do not run Gateway API and will not | [Higress](../higress/README.md), which is more self-contained |
| The traffic is mainly MCP and agent-to-agent | [agentgateway](../agentgeteway/README.md) targets that shape directly |
| You need per-request semantic caching today | check the current feature set rather than assuming; this area moves monthly |

## Notes

Recorded in the original notes, across this folder and its sibling:

- <https://aigateway.envoyproxy.io/docs/capabilities/mcp/> — recorded in this folder's note. It
  is the MCP capability page, not the project home, which says something about what was being
  evaluated: using the AI gateway as the front door for MCP servers as well as for model
  providers. See [`mcp/`](../../mcp/README.md) for why that placement is attractive — an MCP
  server is arbitrary code the model can invoke, and putting policy in front of it is the same
  argument as putting policy in front of any other backend.
- <https://github.com/envoyproxy/ai-gateway> — recorded in the
  [`envoyproxy/`](../envoyproxy/README.md) folder. Same project.

**What is deployed here.** Two `HelmRelease` resources into the `envoy-gateway` namespace:
`aieg-crd` from `oci://docker.io/envoyproxy/ai-gateway-crds-helm` and `aieg` from
`oci://docker.io/envoyproxy/ai-gateway-helm`, both at `v0.6.0`, both with empty values. `aieg`
declares `dependsOn: aieg-crd`, which is the ordering the
[kgateway manifests](../agentgeteway/README.md) are missing.

**It is deployed into the `envoy-gateway` namespace**, not a namespace of its own, and there is
no `namespace.yaml` in this folder — which is consistent with the design: this is an extension
of Envoy Gateway and lives with it. It also means Envoy Gateway itself must already be
installed; see [`network/gateway-api/`](../../../network/gateway-api/README.md) and
[`network/api-gateway/`](../../../network/api-gateway/README.md) for where that lives in this
repository.

**Empty values means no backends are configured.** The chart installs the control plane and its
CRDs; the actual routing — `AIGatewayRoute`, backends, credentials, token limits — is separate
resources that do not exist yet in this repository. What is deployed is the capability, not a
configuration.

---

[← AI gateway](../README.md)
