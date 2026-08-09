[← Agents](../README.md)

# CrewAI

<https://github.com/crewAIInc/crewAI>

---

## The problem it solves

Multi-step LLM work has no natural structure. Left alone it becomes one enormous prompt, or a
pile of `if` statements around API calls that nobody can reason about.

CrewAI imposes a vocabulary on it: an **agent** has a role, a goal and a set of tools; a **task**
has a description and an expected output; a **crew** is a group of agents executing tasks under
a process — sequential, or with a manager agent delegating. The abstraction is deliberately
anthropomorphic: you describe a team rather than a control flow.

What you actually get is boilerplate removal. The tool-calling loop, the retry, the passing of
one task's output into the next task's context, the parsing — CrewAI owns all of it, and you
write the roles.

It is a **Python library**, not infrastructure. Nothing is deployed to the cluster; it ships
inside an application image like any other dependency. That is the reason it is worth
distinguishing from `kagent` or `langflow` in the parent folder.

## When to use it

| Situation | Why CrewAI fits |
|---|---|
| The work genuinely decomposes into distinct roles with distinct tools | the role/goal model matches the problem instead of being decoration |
| You want a working multi-step pipeline quickly | it is the fastest of the frameworks here from zero to something running |
| The output is a document, a report, a research summary | tolerant of latency, and a human reads the result |
| Prototyping, to find out whether the task is even feasible | cheap to throw away |

## When not to use it

| Situation | Use instead |
|---|---|
| Single-step task — one prompt, one answer | call the provider API directly; a framework adds nothing |
| The control flow matters — branches, loops, resume after failure | [LangGraph](../langgraph/README.md), which models exactly that |
| The steps are deterministic and only one of them needs an LLM | ordinary code with one LLM call inside it |
| Latency or cost is a constraint | every agent turn is another round trip, and they compound |
| Side effects need to be safe | there is no rollback for a tool call that already ran |

The last two are the ones that end pilots. A four-agent crew where each agent takes three turns
is twelve model calls for one user request, and the cost and latency are the product of the
whole chain, not the average of it.

## Notes

The only thing recorded for CrewAI in this repository was the project URL:

- <https://github.com/crewAIInc/crewAI>

Nothing is deployed. There are no manifests in this folder and there is nothing to deploy —
CrewAI runs inside an application, so the deployment artefact is whatever image that application
builds. Its presence here is a comparison entry against LangGraph and Swarm, not a platform
component.

---

[← Agents](../README.md)
