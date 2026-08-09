[← Agents](../README.md)

# Swarm

<https://github.com/openai/swarm>

---

## The problem it solves

Swarm is OpenAI's minimal illustration of two ideas, and it is explicitly labelled by its
authors as **experimental and educational** — not something to run in production.

The two ideas:

| Idea | What it means |
|---|---|
| **Routines** | an agent is just instructions plus a set of functions it may call |
| **Handoffs** | a function can return *another agent*, transferring the conversation to it |

That is the whole model. There is no orchestration engine, no state store, no scheduler. A
triage agent decides the request is about billing and hands off to the billing agent, which has
different instructions and different tools. Control passes; the conversation continues.

Its value here is **pedagogical**. Reading Swarm is the cheapest way to understand what the
larger frameworks in this folder are actually doing underneath their abstractions, because
Swarm has almost no abstraction to see past. It has been succeeded by OpenAI's Agents SDK, which
is the maintained path if you want this model in a real application.

## When to use it

| Situation | Why |
|---|---|
| Learning what "multi-agent" actually means mechanically | the source is small enough to read in one sitting |
| Deciding whether a heavier framework is justified | if Swarm's model is enough, the heavier framework is not |
| Illustrating handoffs to a team that has not built agents before | it is the clearest available example |

## When not to use it

Anything else. Concretely:

| Situation | Use instead |
|---|---|
| Production workloads | OpenAI's Agents SDK, or [LangGraph](../langgraph/README.md) |
| Anything needing persistence or resumption | [LangGraph](../langgraph/README.md) — Swarm is stateless between calls |
| Anything not on OpenAI models | a provider-agnostic framework, or an [AI gateway](../../ai-gateway/README.md) in front |
| Anything you expect to receive fixes | it is not an actively maintained product |

## Notes

The only thing recorded for Swarm in this repository was the project URL:

- <https://github.com/openai/swarm>

Nothing is deployed, and nothing should be. It is filed here as a reference point for the
multi-agent pattern, not as a candidate. If a decision needs to be made between the frameworks
in this folder, Swarm's role is to establish the floor: the minimum a framework has to beat
before it is worth the dependency.

---

[← Agents](../README.md)
