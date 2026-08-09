[← Review](../README.md)

# PR-Agent

<https://github.com/The-PR-Agent/pr-agent>

---

## The problem it solves

A large pull request arrives with a one-line description and no obvious place to start reading.
The reviewer either spends an hour reconstructing the intent from the diff, or approves it.

PR-Agent puts an LLM in the pull request and drives it with explicit commands rather than a single
opaque "review" button:

| Command | What it does |
|---|---|
| `/describe` | generates a title, a description and a walkthrough of the changed files |
| `/review` | posts a review: findings, a rough effort estimate, a security note |
| `/improve` | suggests concrete code changes, as committable suggestions |
| `/ask` | answers a question about the diff |

The command model is the design decision worth noting. A reviewer asks for the analysis they want,
when they want it, rather than receiving a wall of comments on every push. That keeps the signal
usable, which is the failure mode of every automated reviewer.

It works across GitHub, GitLab and Bitbucket, and against several model providers rather than one
— which matters, because the model is where the data goes.

## When to use it

- Where pull requests are **large and descriptions are thin**. `/describe` alone pays for a lot of
  it: the reviewer gets a map before reading the diff.
- As a **first pass** that catches the mechanical things — a missing error path, an unhandled nil,
  the fourth copy-pasted block where the variable was not renamed — so that human attention goes to
  design.
- On demand, invoked by a reviewer. This is much better behaved than running automatically on
  every push.
- When the model can be pointed somewhere acceptable: a self-hosted model, or a provider under an
  agreement that covers source code.

## When not to use it

- As **the** reviewer. It has no access to the ticket, the incident that motivated the change, or
  the conversation that preceded it, and it cannot be accountable for the outcome. It annotates; a
  person approves.
- As a **merge gate**. A false positive then stops delivery, and the predictable response is that
  someone disables the tool entirely.
- Automatically on every push, unfiltered. Comment volume is the way this category fails: once
  reviewers learn to scroll past the bot, the real comments go past with it.
- Before the cheap checks exist. An LLM reporting formatting and unused imports is an expensive way
  to run [`../../format/`](../../format/README.md) and [`../../lint/`](../../lint/README.md).
- Where the diff **cannot leave the network** and no self-hosted model is available. This is a
  hard blocker, not a configuration detail.
- As a substitute for smaller pull requests. Summarising a two-thousand-line change treats the
  symptom.

## Notes

The original note for this folder records only the upstream repository:

- <https://github.com/The-PR-Agent/pr-agent>

That is the link as recorded, and it is the one to follow. The project has changed organisation
names over its life, so searching for it by name returns several stale locations; the URL above is
what the note captured.

Status: **catalogued, not evaluated and not deployed.** There is no manifest, no configuration and
no trial recorded.

The decision that has to be made before it can be installed — and it is not a technical one — is
where the diff goes. Every command sends the changed code to a model. That question has to be
answered first, and it also decides between this tool and
[Open Code Review](../open-code-review/README.md), the other LLM reviewer catalogued here.

If the answer is "nowhere", the useful tool in this folder is
[reviewdog](../reviewdog/README.md), which needs no model at all.

---

[← Review](../README.md)
