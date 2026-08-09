[← Agents](../README.md)

# LangGraph

<https://github.com/langchain-ai/langgraph>

---

## The problem it solves

Agent frameworks that describe teams of collaborating personas hide the thing that actually
decides whether the system works: **the control flow**. When an agent gets a bad tool result,
what happens next? When a human needs to approve a step, where does the process stop and how
does it resume? When the process dies halfway through, what state survives?

LangGraph answers those by making the flow explicit. You build a **graph**: nodes are functions,
edges are transitions, and conditional edges branch on the state. State is a typed object that
each node updates. Cycles are allowed — which is what makes it an agent framework rather than a
DAG runner, because "call the model, call a tool, call the model again" is a loop.

The two features that matter most in practice are downstream of that design:

| Feature | Why it matters |
|---|---|
| **Checkpointing** | state is persisted per step, so a run can be resumed instead of restarted |
| **Human-in-the-loop** | the graph can interrupt before a node, wait for approval, and continue |

Both are only possible because the framework knows where you are in the process. A framework
that treats the agent as an opaque loop cannot offer either.

Like CrewAI and Swarm, it is a **library you import**, not something you deploy. LangChain sells
a hosted/self-hosted server product around it; nothing of that is in this repository.

## When to use it

| Situation | Why LangGraph fits |
|---|---|
| The process has real branches and loops you want to see | the graph *is* the specification |
| A step has side effects that need human approval | interrupt-before is a first-class feature |
| Runs are long and must survive a pod restart | checkpointed state, resumable |
| You need to debug why an agent did something | the node sequence is inspectable, not inferred from logs |
| The team already uses LangChain | the integrations carry over |

## When not to use it

| Situation | Use instead |
|---|---|
| A linear, three-step pipeline | plain Python with three function calls |
| You want something running this afternoon | [CrewAI](../crewai/README.md) is faster to a demo |
| The flow is a business workflow with SaaS connectors | [n8n](../n8n/README.md) |
| You want agents managed by Kubernetes | [kagent](../kagent/README.md) |
| The LangChain dependency surface is unwelcome | a direct provider SDK plus your own loop — this is a smaller job than it looks |

That last row deserves saying out loud. An agent loop is roughly: call the model, if it asked
for a tool then run the tool and append the result, repeat until it stops. Writing that yourself
is perhaps fifty lines and removes an entire dependency tree. Frameworks earn their place at
checkpointing, branching and observability — not at the loop itself.

## Notes

The only thing recorded for LangGraph in this repository was the project URL:

- <https://github.com/langchain-ai/langgraph>

Nothing is deployed. As with the other libraries in this folder, the deployment artefact is the
application image that imports it.

---

[← Agents](../README.md)
