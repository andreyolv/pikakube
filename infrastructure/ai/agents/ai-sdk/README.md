[← Agents](../README.md)

# AI SDK

<https://github.com/vercel/ai>

---

## The problem it solves

Every model provider ships its own SDK, its own message format, its own tool-calling shape and its
own streaming protocol. An application that calls two providers writes the same feature twice, and
an application that wants to switch providers rewrites the call site.

The AI SDK is a **provider-agnostic TypeScript toolkit**: one interface for text generation,
structured output, tool calling and the agent loop, with the provider chosen by swapping a model
object.

```ts
const { text } = await generateText({
  model: openai('gpt-5.6'),        // or anthropic(...), or an OpenAI-compatible endpoint
  prompt: 'summarise this incident',
})
```

Four capabilities, which is the whole surface worth knowing:

| Capability | What it is |
|---|---|
| **`generateText` / `streamText`** | one call or a token stream, the same across providers |
| **Structured output** | a Zod schema in, a typed object out — no prompt-and-parse |
| **Tools** | typed functions the model may call, validated against their schema |
| **`ToolLoopAgent`** | the call-model-run-tool-repeat loop from [§1 of the parent](../README.md#1-what-an-agent-actually-is), with step limits |

Alongside it, **AI SDK UI** — `@ai-sdk/react` and equivalents for Svelte and Vue — carries the
streaming half into the browser: a hook that holds the message list and consumes the stream, so the
chat interface is not written by hand for every application.

**It is the first entry in this folder that is not Python.** CrewAI, LangGraph and Swarm assume a
Python service; the AI SDK assumes the agent lives inside the web application that already exists —
Next.js, or any Node runtime. That is not a small difference in practice: it decides whether an AI
feature is a new deployment or a route in a service that is already running.

## When to use it

- the product is a **TypeScript web application** and the AI feature belongs inside it
- a **streaming chat interface** is the interface — this is what AI SDK UI exists for
- structured extraction, where a Zod schema is already the contract used elsewhere in the codebase
- provider portability matters — evaluating two models, or keeping a fallback
- a **single agent with tools**, bounded by step limits, rather than a multi-agent design
  ([§3 of the parent](../README.md#3-why-multi-agent-is-usually-premature) is the argument)

## When not to use it

| Situation | Use instead |
|---|---|
| The application is Python | [CrewAI](../crewai/README.md), [LangGraph](../langgraph/README.md), or a provider SDK plus your own loop |
| Long runs that must survive a restart, with branches and approval gates | [LangGraph](../langgraph/README.md) — checkpointing and interrupt-before are the reason it exists |
| Agents defined as cluster resources, with RBAC and GitOps | [kagent](../kagent/README.md) |
| Non-engineers author the flow | [Langflow](../langflow/README.md) |
| Central key custody, rate limits and cost attribution across teams | not an SDK problem — [`../../ai-gateway/`](../../ai-gateway/README.md) |

The fourth row is the one to be explicit about. The SDK's most convenient path is Vercel's hosted
**AI Gateway**, which is a commercial service and not what this repository runs. Everything in
[`ai-gateway/`](../../ai-gateway/README.md) — [LiteLLM](../../ai-gateway/litellm/README.md),
[Envoy AI Gateway](../../ai-gateway/envoy-ai-gateway/README.md) — is the in-cluster answer to the
same question, and the SDK reaches it the same way it reaches anything else: an OpenAI-compatible
base URL. Point the provider at the gateway, not at the model.

## Notes

**Nothing is deployed.** The deployment artefact is the application image that imports it, as with
every library in this folder. Node 22 or newer; Apache-2.0.

Three things that are infrastructure concerns rather than application ones, and are found the hard
way:

> **Streaming dies in the proxy, not in the code.** Token streaming is a long-lived HTTP response.
> An Ingress that buffers responses delivers the whole answer at once — the feature appears to work
> and feels broken. On ingress-nginx that is `proxy-buffering: "off"` and a
> `proxy-read-timeout` longer than the longest generation, set per route.

> **A tool-using run is minutes, not milliseconds.** Default timeouts and pod
> `terminationGracePeriodSeconds` are sized for request/response traffic; a rollout that evicts a
> pod mid-run loses the run, because nothing here is checkpointed. If a run must survive that,
> the requirement is durable execution and this is the wrong layer for it.

> **Model access is a credential in a web pod.** The provider key sits in the service that serves
> browser traffic, which is the argument for a gateway holding the real key and issuing a scoped
> one — see [`../../ai-gateway/`](../../ai-gateway/README.md).

Its own two boundaries, worth stating so the SDK is not asked for what it does not have:
OpenTelemetry instrumentation is available but marked experimental, so tracing detail per step is
still [Langfuse](../langfuse/README.md)'s job; and there is no evaluation story at all, which is
the named gap in [§9 of the parent](../README.md#9-how-this-applies-to-pikakube).

Local models are the one nice consequence of provider-agnosticism in this cluster: the in-cluster
[Ollama](../../llm/ollama/README.md) speaks an OpenAI-compatible API, so a development build can
target it and a production build a hosted provider, with the model object as the only difference.

---

[← Agents](../README.md)
