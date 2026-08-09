[← Agents](../README.md)

# n8n

<https://github.com/n8n-io/n8n>
<https://github.com/n8n-io/n8n-hosting>
<https://github.com/n8n-io/n8n-hosting/tree/main/kubernetes>

---

**n8n is a workflow automation tool that has AI nodes. It is not an agent framework.** It is
filed here because that is where the AI nodes put it, but the comparison that matters is against
Zapier, Make and Airflow — not against LangGraph. Knowing which category it is in prevents the
usual disappointment, which is expecting agent-grade reasoning from a system whose real strength
is reliable connectors and a trigger.

---

## The problem it solves

Most "AI automation" is nine parts plumbing and one part model. A webhook fires, a record is
read from a database, a field is looked up in a SaaS system, something is summarised, a message
is posted to Slack, a row is written back. Exactly one of those steps needs an LLM. The other
eight are authentication, pagination, retries and date formats.

n8n is built for the eight. It gives you:

| Capability | What it removes |
|---|---|
| Several hundred pre-built connectors | writing and maintaining API clients for SaaS systems |
| Triggers — webhook, schedule, polling, queue | the scheduler and the listener you would otherwise build |
| Visual flow with per-node execution history | reading logs to work out which step failed on which item |
| Credential store | secrets scattered across scripts |
| Per-execution retry and error branches | the error handling nobody writes in a script |
| A code node | the escape hatch for the 5% the connectors do not cover |

Its AI nodes then let one step in that chain call a model, do retrieval, or run a small
tool-using loop. That is genuinely useful and it is genuinely a feature of a workflow tool, not
an agent platform. The loop is shallow, the state model is the workflow's, and the debugging
surface is the node list.

## When to use it

| Situation | Why n8n fits |
|---|---|
| The work is integration with one model call in the middle | that is precisely its shape |
| Internal automation that nobody wants to own as a service | a workflow is cheaper to keep alive than a microservice |
| Non-engineers need to build and change the automation | the canvas plus connectors is the whole point |
| You want it self-hosted rather than in Zapier | the hosting repository above is the maintained path |
| Ad-hoc, back-office, low-volume work | operationally cheap at that scale |

## When not to use it

| Situation | Use instead |
|---|---|
| You actually want an agent — a model looping over tools with memory | [LangGraph](../langgraph/README.md), [CrewAI](../crewai/README.md), or [kagent](../kagent/README.md) on-cluster |
| Data pipelines with dependencies, backfills and SLAs | `data-engineering/` — an orchestrator, not an automation tool |
| High-throughput or latency-sensitive paths | application code; this is not a serving layer |
| The workflow is business-critical and must be reviewed as a diff | code — a workflow JSON is a poor pull request, the same objection as [Langflow](../langflow/README.md) |
| You are building a product feature on top of it | it is a tool for internal glue, and the licence deserves reading first |

## Notes

Recorded in the original notes:

- <https://github.com/n8n-io/n8n> — the project.
- <https://github.com/n8n-io/n8n-hosting> — the official self-hosting repository: Docker
  Compose and Kubernetes examples for running it yourself.
- <https://github.com/n8n-io/n8n-hosting/tree/main/kubernetes> — the Kubernetes subfolder,
  called out separately in the notes because it is the only part relevant to this repository.
  It is a set of plain manifests, not a Helm chart, and it is the starting point for a
  deployment here.

**Nothing is deployed.** There are no manifests in this folder — only the pointers above. n8n is
mapped, not running.

**Read the licence before treating it as a platform component.** n8n is source-available under
its own Sustainable Use Licence rather than a standard OSI open-source licence, and that licence
places restrictions on offering n8n itself as a service to others. Running it internally for
your own automation is the intended use; anything that looks like reselling it is not. This is
not a reason to avoid it — it is a reason to read the terms once, deliberately, rather than
assuming they match the other charts in this repository.

**Two operational points if it is ever deployed**, both visible in the hosting repository:
it needs a database for workflow and execution state, and it has a queue mode for scaling
execution across workers. The single-container default is not the shape you want for anything
more than a trial.

---

[← Agents](../README.md)
