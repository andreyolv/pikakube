[← Documentation](../README.md)

# Executable documentation

Runbooks whose commands are run rather than copied — so they cannot quietly stop working.

Tools covered: [`runme`](runme/README.md)

---

## The problem it solves

A runbook is a Markdown file full of shell commands. Nobody executes it as a document — a person
reads it, copies a command, pastes it into a terminal, and adapts it because the namespace
changed.

The failure follows from that: **nothing ever verifies the commands still work.** A flag was
deprecated two versions ago, a resource was renamed, a path moved. The runbook still looks
correct, and it is discovered to be wrong at 3am by whoever is on call.

The copy-paste step also loses everything around it — which variables to set first, what the
output should look like, what to do if it does not.

Executable documentation makes the code blocks **runnable in place**: the same Markdown file,
with each block executed from the document, its output captured, and variables carried between
steps.

## What it changes

| | A normal runbook | An executable one |
|---|---|---|
| Commands are | copied out | run in place |
| Verified | never | can be executed in CI |
| Variables | described in prose | set once, carried between steps |
| Output | described, or a screenshot | captured from the run |
| Ordering | implied | enforced by the document |
| Drift | silent until an incident | a failing pipeline |

The row that matters is the second. A runbook that can be executed can be executed *on a
schedule*, against a test cluster, and a broken step becomes a build failure instead of an
incident.

That is the whole argument, and it is a strong one for exactly one class of document.

## Runme

[Runme](runme/README.md) runs the code blocks inside a Markdown file — from a terminal UI, from
the CLI, or from a VS Code extension that renders the document with a run button on each block.
The file stays valid Markdown, so it renders normally on GitHub and in any site generator.

That last property is what makes it adoptable: the runbook is not converted into a different
format, it gains a capability.

## Where it fits, and where it does not

| Document | Executable? |
|---|---|
| **Runbook** — restore a backup, rotate a certificate, drain a node | **yes**, this is the case |
| **Onboarding** — set up a local environment | **yes**; verified setup instructions are rare and valuable |
| Demo or tutorial | yes — a walkthrough that provably works |
| Incident playbook | partly; the diagnosis steps yes, the judgement no |
| Architecture documentation | no, there is nothing to run |
| Conceptual explanation | no |
| An [ADR](../decision-record/README.md) | no, and it is immutable anyway |

The one to be careful with is the incident playbook. Making destructive steps one click away is
not obviously an improvement — see the anti-patterns.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| A runbook never executed since it was written | commands rot silently and fail when it matters | run it, on a schedule |
| Making everything executable | conceptual documentation has nothing to run | runbooks and setup guides only |
| **Destructive commands one click away** | a delete that used to need copy-paste now needs a misclick | keep those manual, and say why |
| Executable steps against production by default | the document does not know which cluster it is pointed at | make the target explicit and required |
| Credentials in the document | it is a Markdown file in a repository | reference a secret |
| Captured output committed as truth | it was true on one cluster, on one day | capture it, and date it |
| A tool nobody has installed | the runbook now requires a dependency to read | it must render as plain Markdown, which Runme does |

## How this applies to pikakube

Nothing is deployed, and the fit here is specific rather than general.

This repository has one document that is unambiguously a runbook and would benefit immediately:
the **cluster bootstrap**. [`init.sh`](../../../init.sh) plus the Kind configurations under
[`clusters/kind-configs/`](../../../clusters/kind-configs/) are the sequence someone runs to
recreate the environment, and whether it currently works end to end is not verifiable by
reading it.

That is exactly the case the tool exists for — and this repository already demonstrates why the
problem is real. The Kind configuration carries a `hostPath` pointing at a directory that does
not exist on this machine, which is the kind of breakage a document cannot show and an execution
finds in seconds.

The other candidates, in order of value:

1. **Bootstrap and teardown** — `init.sh`, `finish.sh`, and the Kind configurations
2. **Restore drills** — the [Velero](../../site-reliability-engineering/backup/velero/README.md)
   restore procedure, which is the documented case of a step order that must be right
3. **Onboarding** — the [Devbox](../../../devbox.json) environment and first cluster

The restore drill is the one with the highest consequence. Its documentation records that the
operator must be scaled to zero *before* the restore, or it recreates an empty volume first — a
step order that is easy to write down and easy to get wrong under pressure.

---

[← Documentation](../README.md)
