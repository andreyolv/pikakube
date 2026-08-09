[← Architecture decision records](../README.md)

# MADR — Markdown Any Decision Records

<https://github.com/adr/madr>

---

## What it is

A **template**, not a tool. A Markdown file with an agreed set of headings, a numbering
convention, and a short guide to filling it in.

There is nothing to install, no build step and no dependency. Adopting it means copying a
template into `docs/adr/0001-some-decision.md` and writing.

That minimalism is the point, and it is why this is the recommendation in
[`../README.md`](../README.md#3-the-format-is-not-the-point): the value of an ADR is in having
written the reasoning down, and any tooling between the decision and the file is friction on the
part that matters.

## The template

```markdown
# Use Flux instead of Argo CD for GitOps

## Status
Accepted

## Context and problem statement
...the forces at play, the constraints, what was already true...

## Decision drivers
* the workflow is manifest-first
* the number of components to operate matters on a single cluster

## Considered options
* Flux
* Argo CD
* Both, for different workloads

## Decision outcome
Chosen: **Flux**, because ...

### Consequences
* Good: fewer components, reconciliation is the whole model
* Bad: no UI, so cluster state is inspected with kubectl

## Pros and cons of the options
### Argo CD
* Good: the UI is genuinely useful for visualising sync state
* Bad: more components, and the UI becomes a second source of truth
```

The last two sections carry the value. "Chosen: Flux" is a fact readable from the repository;
the rejected option and its actual merits are the decision.

## When to use it

- **starting ADRs at all** — this is the lowest-friction way
- a small or medium repository where files in a folder are enough to browse
- the format should stay readable on GitHub with no tooling
- the team will not adopt anything that requires installing something

## When not to use it

- enough ADRs that browsing and searching them is a real problem —
  [Log4brains](../log4brains/README.md)
- a published, indexed site is required for a wide audience
- the organisation already has a mandated format

## Practical conventions

| Convention | Why |
|---|---|
| `docs/adr/NNNN-title-in-kebab-case.md` | sortable, linkable, and greppable |
| Four-digit numbers | avoids renumbering later |
| **Never edit an accepted ADR** | supersede it with a new one; the history is the point |
| `Superseded by ADR-0012` in the status | the trail stays followable |
| An `0000-use-adrs.md` | the decision to use ADRs is itself an ADR, and it explains the folder |
| One decision per file | otherwise superseding one supersedes the others |

The immutability convention is the one people break first, usually with good intentions —
updating an ADR when the decision changes destroys exactly the record it existed to keep.

## Notes

**The recommendation for this repository**, and the reasoning is in
[`../README.md`](../README.md#7-how-this-applies-to-pikakube): the decisions and their
alternatives are already documented across the capability READMEs. What is missing is a record
of which option was chosen *here* and why, and that is a folder of Markdown files rather than a
project.

[`docs/docs-standard.md`](../../../../docs/docs-standard.md) at the repository root already
proposes a `docs/tech/adr/` folder. It does not exist yet, and MADR is what would fill it.

The starting set is already visible: Flux over Argo CD, nip.io for the local cluster,
CloudNativePG over the other Postgres operators, READMEs rendered by GitHub instead of a
generated site, and the capability-based folder taxonomy itself — which shapes the whole
repository and is recorded nowhere.

---

[← Architecture decision records](../README.md)
