[← AI gateway](../README.md)

# agentgateway

<https://github.com/agentgateway/agentgateway>
<https://github.com/kgateway-dev/kgateway>

---

**Two things about this folder before anything else.**

The directory name `agentgeteway/` is a **typo** for `agentgateway`. Noted, not renamed — a
rename touches the GitOps path and is not a documentation change.

The manifests in this folder do not deploy agentgateway. They deploy **kgateway** — the
`kgateway-crds` and `kgateway` charts, at `v2.1.1`, into the `kgateway` namespace. The folder
name and its contents disagree, and the second link in the original notes is the explanation:
kgateway is the control plane, agentgateway is the data plane it can drive.

---

## The problem it solves

The gateways in the sibling folders are built for **LLM provider traffic**: many applications
calling OpenAI, Anthropic, Bedrock and a self-hosted model, and needing one place for keys,
routing, rate limits and cost.

agentgateway aims at a different and newer shape of traffic: **agents talking to tools, and
agents talking to agents**. Concretely, that means MCP and A2A rather than only the
OpenAI-shaped chat completions API. The problems it targets are the ones that appear once tool
calling is real:

| Problem | Why a proxy is the right place for it |
|---|---|
| Every agent wires up its own MCP servers | one endpoint that federates many MCP servers behind it |
| Tool access is granted per-application, ad hoc | authorisation policy on tool calls, centrally |
| Nobody can see which tools were invoked | the proxy sees every call, so tool-level observability exists |
| Agent-to-agent calls have no governance | A2A traffic goes through the same policy path |

The pairing with kgateway is the deployable story. kgateway is a Gateway API control plane —
the project formerly known as Gloo Gateway, now CNCF — and it can configure agentgateway as the
proxy for AI and MCP traffic. So the control plane is the familiar one, expressed in Gateway API
resources, and the data plane is the agent-aware one.

## When to use it

| Situation | Why agentgateway fits |
|---|---|
| MCP servers are numerous and every agent connects to them directly | a federating proxy is the fix, and it is the same argument as a service mesh |
| Tool invocation needs authorisation independent of the agent's code | policy at the proxy, not in each application |
| Agent-to-agent traffic is real and ungoverned | A2A support is a design goal, not an afterthought |
| You already run kgateway or Gateway API | the control plane is not new work |

## When not to use it

| Situation | Use instead |
|---|---|
| The problem is provider keys, cost and failover for LLM calls | [Envoy AI Gateway](../envoy-ai-gateway/README.md) — that is what it is built for |
| You have three MCP servers and two applications | direct connections; a proxy is not yet earning its place |
| You do not run Gateway API and do not want to | the whole deployment model assumes it |
| You need something settled | this is among the newest projects in this repository — expect change |

The two categories overlap and will overlap more. If the only requirement today is "one place
for provider keys and per-team token limits", the AI gateway answers it with less new
machinery.

## Notes

Recorded in the original notes:

- <https://github.com/agentgateway/agentgateway> — the proxy itself. Written in Rust, aimed at
  MCP, A2A and LLM traffic. CNCF sandbox.
- <https://github.com/kgateway-dev/kgateway> — the Gateway API control plane that can drive it.
  Previously Gloo Gateway, from Solo.io, donated to CNCF. This is the project the manifests in
  this folder actually install, and the same organisation behind
  [kagent](../../agents/kagent/README.md) in the agents folder — a consistent bet on one
  ecosystem rather than four unrelated ones.

**What is deployed here.** Two `HelmRelease` resources — `kgateway-crds` and `kgateway`, both
from `oci://cr.kgateway.dev/kgateway-dev/charts/...` at tag `v2.1.1`, both with empty values,
into the `kgateway` namespace. Both `OCIRepository` sources live in `flux-system`.

Two observations on that:

**The CRD release is not declared as a dependency.** The `kgateway` release does not `dependsOn`
`kgateway-crds`, unlike the equivalent pair in
[kagent](../../agents/kagent/README.md) and
[Envoy AI Gateway](../envoy-ai-gateway/README.md), which both do. Flux will retry until the CRDs
exist, so it converges — but the first reconciliation can fail noisily for no reason, and the
fix is one field.

**The tag is not pinned by digest**, where the kagent releases in this repository are. A tag can
move; a digest cannot. Worth being consistent about.

---

[← AI gateway](../README.md)
