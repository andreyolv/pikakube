[← AI gateway](../README.md)

# Higress

<https://github.com/alibaba/higress>

---

## The problem it solves

Higress is Alibaba's cloud-native gateway — Istio and Envoy underneath — that covers ingress,
API gateway and AI gateway in one deployment. Where
[Envoy AI Gateway](../envoy-ai-gateway/README.md) is an extension you add to an existing Envoy
Gateway installation, Higress is a **complete gateway that happens to have an AI mode**.

That difference decides which one fits. If the cluster has no Gateway API story yet, Higress
brings its own; if it already has one, Higress is a second gateway.

Its distinguishing feature is the **plugin model**. Higress runs WASM plugins, written in Go,
Rust or other languages that compile to WASM, and much of its AI functionality ships as plugins
rather than as core code:

| Plugin area | What it does |
|---|---|
| Provider routing | one API surface, many upstream model providers |
| Token rate limiting | quotas measured in tokens rather than requests |
| Prompt/response caching | serve repeats without paying the provider again |
| Content safety | moderation hooks on prompts and responses |
| Prompt templating and rewriting | shaping requests centrally rather than per application |

The plugin model is the real advantage and the real risk. It means the gateway is extensible
without forking, and it means a meaningful share of the behaviour you depend on lives in
components with their own maturity, separate from the gateway's release.

Two practical caveats, stated plainly rather than as objections:

**The centre of gravity is Chinese.** The project is widely used in that ecosystem, and while
there is English documentation, the deepest material, the issue discussions and the fastest
answers are frequently in Chinese. That is a real cost for a team that cannot read it, and it is
the single most common reason it gets ruled out elsewhere.

**It brings Istio.** Higress is built on Istio and Envoy. Check carefully how that interacts
with whatever service mesh the cluster already runs before installing it — see
[`network/service-mesh/`](../../../network/service-mesh/README.md) for where that concern lives
here.

## When to use it

| Situation | Why Higress fits |
|---|---|
| You want ingress, API gateway and AI gateway from one component | it is designed as one product, not three integrations |
| The cluster has no Gateway API installation to extend | Higress does not assume one exists |
| The AI features you want are its plugins — caching, moderation, token limits | they ship as plugins rather than as roadmap |
| You want to write gateway logic yourself | the WASM plugin model is the most open one in this folder |

## When not to use it

| Situation | Use instead |
|---|---|
| Envoy Gateway or another Gateway API implementation is already running | [Envoy AI Gateway](../envoy-ai-gateway/README.md) — extend, do not add a second gateway |
| A service mesh is already deployed | check the Istio interaction first; this can be a genuine conflict |
| Nobody on the team can follow Chinese-language sources | the support surface is narrower than it looks |
| The problem is MCP and agent-to-agent traffic | [agentgateway](../agentgeteway/README.md) |

## Notes

The only thing recorded for Higress in the original notes was the project URL:

- <https://github.com/alibaba/higress> — the project. Envoy and Istio based, with WASM plugins
  and an AI gateway mode.

**Nothing is deployed.** There are no manifests in this folder. Higress is mapped as the
alternative to Envoy AI Gateway, not adopted — and given that
[Envoy AI Gateway is deployed](../envoy-ai-gateway/README.md) at `v0.6.0` in the `envoy-gateway`
namespace, adopting Higress as well would mean running two gateways for one job. Its role here
is comparison.

---

[← AI gateway](../README.md)
