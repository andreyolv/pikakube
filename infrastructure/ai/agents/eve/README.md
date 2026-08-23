[← Agents](../README.md)

# Eve

<https://github.com/vercel/eve>

---

## What it is

A framework for building agents where **the filesystem is the authoring interface**. Vercel's
premise is that an agent is not a configuration object but a directory, and every capability lives
at a conventional path:

```
my-agent/agent/
├── agent.ts          # model and runtime configuration
├── instructions.md   # the system prompt
├── tools/            # typed functions the model may call
├── skills/           # procedures loaded on demand
├── channels/         # where messages arrive — HTTP, Slack, Discord
└── schedules/        # cron jobs
```

`npx eve@latest init` scaffolds that tree; `npm run dev` runs it with a terminal UI. TypeScript,
Zod for tool schemas, and model selection at runtime — the quick start uses hosted models through
Vercel's AI Gateway, but the provider is a configuration line.

**The consequence of the design is the reason to care about it.** An agent's behaviour — its
prompt, its tools, its scheduled work, its entry points — is a set of reviewable files. Compare
that with [Langflow](../langflow/README.md), where the flow is canvas JSON and
[the parent's anti-pattern table](../README.md#8-anti-patterns) records that it *cannot be reviewed
as a diff*. Eve is the opposite pole of the same axis: the whole agent is a pull request.

## Where it sits in this folder

Neither column of [the parent's split](../README.md#2-three-different-things-live-in-this-folder)
fits cleanly, which is worth stating rather than glossing over:

| | Libraries — CrewAI, [AI SDK](../ai-sdk/README.md) | Platforms — kagent, Langflow | **Eve** |
|---|---|---|---|
| You | import it into an application | operate it for other teams | **scaffold an application from it** |
| The agent is | code you wrote, calling a library | a record in a platform's database | **a directory of files** |
| Deployment artefact | your application image | Helm releases and CRDs | **the scaffolded app, deployed as one** |

It is closer to the library column — nothing here is a platform other teams share — but it brings
its own runtime, its own project layout and its own entry points, which a library does not. The
honest description is an **application framework**: it decides the shape of the service, not just
the calls inside it.

The `skills/` directory is the same idea catalogued in
[§7.10 of `ai/`](../../README.md#710-skills-prompts-and-context-for-agents) and used by
[Hermes Agent](../hermes-agent/README.md) — capability distributed as instructions rather than as
code. The difference is who writes them: in Eve a person commits them, so
[the review question Hermes raises](../hermes-agent/README.md) — what reviewed the behaviour the
agent taught itself — does not arise here.

## When to use it

- a **long-lived agent with entry points**, rather than an AI feature inside an existing request
  path — something reachable over HTTP, in Slack, and on a schedule
- the behaviour should be **diffable and owned in Git**, by people who write TypeScript
- prototyping quickly, and keeping the prototype reviewable
- the deployment target is Vercel, where the channels and schedules map onto platform primitives
  with nothing to operate

## When not to use it

| Situation | Use instead |
|---|---|
| An AI feature inside an application that already exists | [AI SDK](../ai-sdk/README.md) — the same ecosystem, no new service |
| Agents as cluster resources, with RBAC, GitOps and metrics | [kagent](../kagent/README.md) |
| Explicit control flow, checkpointing, human approval mid-run | [LangGraph](../langgraph/README.md) |
| Python teams | nothing here — it is TypeScript |
| Anything you cannot afford to migrate | it is **beta**, under Vercel's beta terms |

## Notes

Apache-2.0, TypeScript, and **in beta** — the README says APIs and behaviour may change before
general availability, which for an application framework means the project layout itself is not yet
a stable contract. That is the single most important line in an evaluation: adopting it commits the
shape of the service, not just a dependency version.

**What running it here would actually require.** The framework's convenient path is Vercel, and
Vercel supplies the pieces the conventions imply. On this cluster nothing supplies them, so each
one becomes a manifest:

| Convention | What it needs off-Vercel |
|---|---|
| `channels/http` | a Service and an Ingress, with response buffering off if it streams |
| `channels/slack`, `channels/discord` | a public endpoint and the app credentials, held as secrets |
| `schedules/` | either the framework's own scheduler in a long-running pod, or a `CronJob` per schedule — pick one, not both |
| "durable" agents | whatever store the runtime uses for run state, provisioned and backed up |

That last row is the one to check before anything else, because it is what the word *durable* in
the project's own description is doing. The general point applies to every framework whose
conventions assume one host: **the conventions are free on the platform they were designed for and
become infrastructure everywhere else.**

Nothing is deployed here; this is a mapping. If it is ever adopted, the beta status and the
durability question are the two things to settle first, and both are decisions rather than
configuration.

---

[← Agents](../README.md)
