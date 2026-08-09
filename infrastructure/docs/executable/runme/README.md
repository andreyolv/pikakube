[← Executable documentation](../README.md)

# Runme

<https://github.com/stateful/runme>

---

## The problem it solves

A runbook is a Markdown file full of shell commands that nobody executes as a document — a person
reads it, copies a command, pastes it, and adapts it because something changed.

Because it is never executed, **nothing ever verifies it still works**. A deprecated flag, a
renamed resource, a moved path: the runbook still looks correct, and it is discovered to be wrong
by whoever is on call.

Runme makes the code blocks runnable **in place**, from a terminal UI, the CLI, or a VS Code
extension that renders the document with a run button on each block.

## The property that makes it adoptable

The file stays valid Markdown. It renders normally on GitHub, in any site generator, and for
anyone who does not have Runme installed.

That matters more than any feature: the runbook is not converted into a different format, it
gains a capability. Nothing is lost for readers who just want to read.

## What it adds

| Capability | Detail |
|---|---|
| **Run a block** | execute in place, output captured below it |
| **Variables between steps** | set once, carried through the document |
| Named blocks | run a specific step, or a sequence |
| Interactive prompts | ask for the namespace rather than assuming it |
| **CI execution** | `runme run` in a pipeline, so the runbook is tested |
| Skip flags | mark a block as documentation-only, not to be run |

The CI row is the whole argument. A runbook that can be executed can be executed on a schedule
against a test cluster, and a broken step becomes a build failure instead of an incident.

## When to use it

- **runbooks** — restore a backup, rotate a certificate, drain a node
- **onboarding and setup guides**, where verified instructions are rare and valuable
- demos and tutorials that should provably work

## When not to use it

- conceptual documentation — there is nothing to run
- architecture documentation, or an [ADR](../../decision-record/README.md)
- **destructive procedures**, where one click is not an improvement over deliberate copy-paste
- anything pointed at production without the target being explicit and required

## Notes

Not deployed here, and the fit is specific rather than general.

The candidate in this repository is the **cluster bootstrap** —
[`init.sh`](../../../../init.sh), [`finish.sh`](../../../../finish.sh) and the Kind
configurations under [`clusters/kind-configs/`](../../../../clusters/kind-configs/). Whether
that sequence currently works end to end is not verifiable by reading it.

This repository already demonstrates why that matters: the Kind configuration carries a
`hostPath` pointing at a directory that does not exist on this machine — a breakage a document
cannot show and an execution finds in seconds.

The candidates in order of value:

1. **Bootstrap and teardown** — the sequence that recreates the environment
2. **Restore drills** — the
   [Velero](../../../site-reliability-engineering/backup/velero/README.md) procedure, whose
   documentation records that the operator must be scaled to zero *before* the restore, or it
   recreates an empty volume first
3. **Onboarding** — the [Devbox](../../../../devbox.json) environment and first cluster

The restore drill has the highest consequence and is the clearest example of the general point:
a step order that is easy to write down and easy to get wrong under pressure is exactly the thing
that should be executed rather than read.

---

[← Executable documentation](../README.md)
