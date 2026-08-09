[← Presentations](../README.md)

# Marp

<https://github.com/marp-team/marp>

---

## What it is

Markdown slides with almost no ceremony. One file, `---` between slides, and a VS Code extension
that previews as you type.

```markdown
---
marp: true
theme: default
---

# Platform overview

---

## Why capability-based folders

- one axis per level
- the tree is the navigation
```

That is a complete deck. There is no project to scaffold, no dependency to install if the VS Code
extension is used, and the file renders as ordinary Markdown anywhere else.

## When to use it

- **any internal deck** — architecture walkthrough, onboarding, design review, sprint update
- the content should stay portable Markdown
- **PPTX export matters**, because someone will need to edit it in PowerPoint
- the deck should be built from documentation that already exists

## When not to use it

- a conference talk with live-editable code and animation —
  [Slidev](../slidev/README.md)
- fine-grained control over layout and transitions
- the deck is the deliverable and its appearance is most of the value

## What makes it worth it here

| Property | Consequence |
|---|---|
| **Renders Mermaid** | the decision tree in a capability README appears in the deck without being redrawn |
| Plain Markdown | the file is readable and diffable with no tooling |
| **PPTX export** | the organisational reality that somebody will want to edit it |
| CLI | `marp deck.md -o deck.pdf`, so it builds in CI |
| VS Code preview | writing and seeing the slide at the same time |

The first row is the reason to prefer it over any binary format: the diagram in the presentation
is the *same* diagram as in the documentation, not a screenshot that will be wrong next quarter.

## Practical notes

| Concern | Detail |
|---|---|
| Themes | a handful built in; custom themes are CSS |
| **PPTX fidelity** | expect layout drift — it is an export, not a native format |
| Images | relative paths, which must resolve at build time |
| Long content | there is no auto-fit; a slide that overflows simply overflows |
| Speaker notes | HTML comments, exported to PDF and PPTX |

The overflow behaviour catches people out. Marp does not shrink text to fit, so a slide with too
much on it silently runs off the bottom — which is arguably correct, and is worth knowing before
presenting.

## Notes

Not used here yet, and the case is straightforward: this repository already contains the content
a platform talk needs — capability trade-offs, decision trees, anti-patterns — in Markdown, with
Mermaid diagrams Marp renders directly.

The realistic first deck is an **onboarding walkthrough**: the capability structure, what runs
where, and why the choices were made. Built from the existing READMEs, in one file, with no
possibility of showing an architecture diagram that stopped being true.

Worth pairing with [`decision-record/`](../../decision-record/README.md): a deck is a delivery
mechanism, and the durable record of the decisions it presents belongs in an ADR.

---

[← Presentations](../README.md)
