[← Diagrams](../README.md)

# Mermaid

<https://github.com/mermaid-js/mermaid>

---

## The problem it solves

A diagram that lives **inside the Markdown**, as text, rendered natively by GitHub, most IDEs and
every site generator in [`site-generator/`](../../site-generator/README.md).

Nothing to install, nothing to build, no image file to keep in sync with the prose around it.
The diagram is in the same file as the paragraph that introduces it, so it is edited by whoever
edits that paragraph and reviewed in the same diff.

That single property is why it is the default here and why it beats better-looking alternatives.

## What it draws

| Type | Used for |
|---|---|
| **`flowchart`** | decision trees, request paths — by far the most used |
| `sequenceDiagram` | protocol exchanges, failure sequences |
| `erDiagram` | data models |
| `stateDiagram-v2` | lifecycles, controller states |
| `gantt` | timelines |
| `C4Context` | architecture at the C4 levels |
| `gitGraph` | branching strategies |

## When to use it

- **explaining a concept, a flow, or a decision** — which is most diagrams in documentation
- the diagram belongs next to the text that discusses it
- it must be reviewable, so a change is visible in the diff
- rendering on GitHub without a build step is a requirement

## When not to use it

- **precise layout control is needed** — you get what the layout engine produces
- a polished cloud architecture diagram with vendor icons —
  [Diagrams](../diagrams/README.md) or [awsdac](../aws-dac/README.md)
- the diagram should be generated from real state —
  [KubeDiagrams](../kubediagrams/README.md)
- it is a sketch meant to explain, informally — [Excalidraw](../excalidraw/README.md)
- past roughly 20 nodes, where automatic layout stops producing something readable

## The layout limitation, and why it is useful

Mermaid decides the layout. Direction and grouping can be nudged, and individual node positions
cannot be set.

This is the standard complaint and it is largely a feature. A diagram that Mermaid lays out badly
is usually a diagram with too many nodes, and the correct response is to split it rather than to
gain manual control over an unreadable picture. The tool refusing to draw a knot neatly is
useful feedback.

Where it is a genuine limitation is the architecture diagram intended for a presentation, where
appearance is part of the job. That is what the code-based tools in this folder are for.

## Practical notes

| Concern | Detail |
|---|---|
| **GitHub support** | native in Markdown, in a ```` ```mermaid ```` fence; no plugin |
| MkDocs Material | rendered through `superfences` |
| Special characters | `[`, `(`, `"` in labels need quoting, and the failure is a blank diagram |
| Line breaks | `<br/>` inside a label |
| Comments | `%%` at the start of a line |
| Themes | limited; do not plan a visual identity around it |

The special-character row is the one that costs time. A single unquoted bracket in a node label
renders nothing at all rather than rendering imperfectly, and the error message is not helpful.
Quoting labels containing punctuation avoids it entirely.

## Notes

Recorded in the original notes: <https://github.com/mermaid-js/mermaid/issues/6109>

Mermaid is used throughout this repository — every capability README under
[`infrastructure/`](../../../) carries a decision tree written in it, rendered by GitHub with no
build step. That is the tool being used for precisely what it is good at.

One thing worth correcting: [`docs/mermaid/`](../../../../docs/mermaid/) at the repository root
holds 21 standalone `.mmd` files. That gives up Mermaid's only real advantage — living inline
with the text — while gaining none of the benefits of an image. Those diagrams belong inside the
documents that should be showing them.

---

[← Diagrams](../README.md)
