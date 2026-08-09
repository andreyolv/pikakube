[← Architecture decision records](../README.md)

# Log4brains

<https://github.com/thomvaill/log4brains>

---

## What it adds over a template

[MADR](../madr/README.md) is a template. Log4brains is a CLI plus a generated static site around
the same idea:

| Capability | Detail |
|---|---|
| `log4brains adr new` | scaffolds a numbered file with the template filled in |
| **A generated site** | ADRs published, searchable, with a timeline |
| Status tracking | draft, proposed, accepted, superseded — rendered as a state |
| **A knowledge-base view** | tags, and a browsable index rather than a directory listing |
| Preview | live reload while writing |
| CI publishing | to GitHub Pages, like any static site |

The genuine addition is **discoverability at volume**. Fifteen ADRs in a folder are browsable by
looking at the filenames. Eighty are not, and at that point a searchable site with tags and a
timeline stops being decoration.

## When to use it

- enough ADRs that finding the relevant one is a real problem
- ADRs should be published to people who will not browse the repository
- a scaffolding command genuinely helps, because writing starts more often than it finishes
- the timeline view is useful — several teams, decisions over years

## When not to use it

- **starting out** — [MADR](../madr/README.md) is the right first step, and this can be adopted
  later over the same files
- a small repository where a folder listing is enough
- adding a Node dependency and a build step to publish Markdown is unattractive
- the tooling would become the reason ADRs do not get written

## The trap worth naming

Choosing ADR tooling before writing an ADR is the most common way this practice fails to start.
The obstacle was never the format or the browsing experience — it is the discipline of writing
the reasoning down at the moment of the decision.

A repository with `docs/adr/0001-*.md` and no tooling is doing this correctly. One with a
Log4brains site and four ADRs written in a single retroactive afternoon is not.

Log4brains reads a conventional ADR folder, so this is a decision that can be deferred without
cost: start with MADR, and adopt the site if browsing ever becomes the problem.

## Notes

Not used here, and it is deliberately not the recommendation — see
[`madr/`](../madr/README.md).

The original note in this repository put it directly:

> Nice, but unnecessary. Simplicity — what matters is the information, not the format or the
> tool.

That is the correct read, and it is why this folder recommends the template. The value is in the
writing; the site is what you build when there is enough written to need one.

Worth reading regardless of tooling:
[the ADR collection](https://github.com/joelparkerhenderson/architecture-decision-record) for
templates and background, and
[the actions-runner-controller ADRs](https://github.com/actions/actions-runner-controller/tree/master/docs/adrs)
as an example of the practice in a real project.

---

[← Architecture decision records](../README.md)
