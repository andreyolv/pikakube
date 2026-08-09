[← Agents](../README.md)

# Hermes Agent

<https://github.com/nousresearch/hermes-agent>

---

## What it is

An agent you **run and talk to**, from Nous Research — not a library to build with, and not a
platform to run for other people. Its own description is *"the self-improving AI agent"*, and the
capabilities it claims are: creating skills from experience, improving them during use, persisting
what it learns, and searching its own past conversations.

It reaches the user through the places people already are — CLI, Telegram, Discord, Slack, WhatsApp,
Signal — and it executes commands in a terminal. It is model-agnostic: Nous Portal, OpenRouter,
OpenAI or a custom endpoint, switched with a command. MIT licensed, Python and Node.

That combination puts it in a category of its own in this folder — see
[`../README.md`](../README.md#2-three-different-things-live-in-this-folder), which splits libraries
from platforms. This is neither.

| | Libraries | Platforms | **Hermes Agent** |
|---|---|---|---|
| Example | CrewAI, LangGraph | kagent, Langflow | this |
| You | import it | operate it for others | **run it, and talk to it** |
| Configured by | code | manifests or a UI | conversation, and its own learned skills |
| Belongs to | an application team | the platform team | **a person** |

## The self-improving claim

This is the interesting part and the part to be careful about, so it is worth separating what the
mechanism is from what it implies.

The mechanism, as described: the agent writes skills from what it has done, refines them as it uses
them, and persists them so they survive the session. That is a real and coherent idea, and it is the
logical end of the trend recorded in
[`../../README.md`](../../README.md#710-skills-prompts-and-context-for-agents) — agent capability
being distributed as **instruction files** rather than as code. Everything in that section is a
human writing skills for an agent. This is an agent writing them for itself.

The implication is where the engineering question sits.
[`../README.md`](../README.md#4-the-reliability-problem) argues that agents have no rollback: a tool
call with side effects cannot be undone, and non-determinism means the same input does not
reproduce. Self-generated persistent skills sharpen that considerably:

| Question | Why it matters |
|---|---|
| **What reviewed the skill?** | behaviour changed, and no diff was proposed to anybody |
| **What happens when a learned skill is wrong?** | it is now the agent's default approach, applied silently |
| How is it rolled back? | if skills are files in Git, this is answerable; if not, it is not |
| Does the skill encode a one-off? | a workaround learned during an incident becomes standing behaviour |

None of that makes the idea bad. It makes **where the skills are stored** the first thing to check:
a skill directory under version control is reviewable and revertible, and one inside an opaque store
is not. That is the same argument
[`../README.md`](../README.md#4-the-reliability-problem) makes about aider committing its own work —
Git is the undo that agents otherwise lack.

## The security surface, stated plainly

Three properties that are individually reasonable and combine into something that needs thinking
about:

1. **It executes commands in a terminal**
2. **It is reachable from chat platforms** — Telegram, WhatsApp, Discord, Slack, Signal
3. **It persists self-authored behaviour**

[`../../README.md`](../../README.md) already records the general form of this concern: an agent that
reads untrusted input *and* holds a credential that can act is the combination to avoid. A chat
message is untrusted input, a terminal is action, and a learned skill makes the effect durable.

The practical consequences: whoever can message it can, in effect, ask it to run things; prompt
injection through a forwarded message or a pasted link is a live path; and the blast radius is
whatever the machine it runs on can reach. Run it somewhere it cannot reach anything that matters,
and treat the chat integrations as a public interface rather than a convenience.

## When to use it

- **a personal assistant** with real capability — running commands, remembering, scheduling
- reaching an agent from a phone matters more than embedding one in an application
- the self-improving skill loop is genuinely the thing being evaluated
- model portability is wanted — it is not tied to one provider

## When not to use it

- **building an agent into an application** — [`../README.md`](../README.md) is the folder for that,
  and CrewAI or LangGraph are the shapes
- providing agents as a platform capability to teams — [kagent](../kagent/README.md) makes them
  Kubernetes objects with RBAC and metrics
- anywhere the security combination above is not acceptable
- anything requiring reproducibility — an agent that changes its own behaviour is the opposite of
  that

## Notes

Added to the catalogue from <https://github.com/nousresearch/hermes-agent>.

**Two things were not verified and should be checked before adopting it.** The repository statistics
returned during this survey were not credible — star and commit counts an order of magnitude beyond
what a project of this age would have — so **maturity, release cadence and community size are
recorded here as unverified.** The README also describes migration tooling from a predecessor
project, which suggests a recent lineage change; worth understanding before depending on it.

Nothing is deployed. Like everything in
[`../../README.md`](../../README.md#79-coding-agents), this is a developer tool rather than a
platform component — it does not run in the cluster.

**Why it earns a page rather than a table row.** The coding agents in section 7.9 are variations on
one shape: an agent that edits a repository. This is a different shape — a persistent, multi-channel,
self-modifying assistant with shell access — and the questions it raises about reviewing learned
behaviour apply well beyond this particular project. That argument is the reason to keep it, more
than the tool itself.

---

[← Agents](../README.md)
