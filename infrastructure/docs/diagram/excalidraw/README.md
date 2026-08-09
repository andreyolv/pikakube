[← Diagrams](../README.md)

# Excalidraw

<https://github.com/excalidraw/excalidraw>

---

## The problem it solves

A hand-drawn whiteboard sketch — deliberately rough, quick to make, and the right tool for
**explaining an idea to a person**.

That sounds like the opposite of everything else in this folder, and it is a defensible position.
A generated diagram is complete and unreadable; an explanation requires leaving things out. The
three components that matter, the arrow carrying the interesting data, and none of the sidecars.

The sketchy rendering is part of why it works. A hand-drawn box does not claim to be
authoritative, which is honest — and it invites correction in a way a polished diagram does not.

## When to use it

- **explaining how something works**, to a person, quickly
- a design discussion where the diagram is the conversation
- a conceptual overview at the top of a document, before the detail
- collaborating live, which it does well

## When not to use it

- **as the source of truth for an architecture** — this is the failure mode of the whole
  category
- anything that must stay current as the system changes
- inside a Markdown document that should diff — [Mermaid](../mermaid/README.md)
- describing what is actually deployed — [KubeDiagrams](../kubediagrams/README.md)

## The property that decides it

`.excalidraw` files are JSON, so they are technically text and technically diffable. In practice
the diff is coordinates and element IDs — unreviewable, and it changes when anything is dragged.

So it inherits the problem of every drawing tool: **nothing connects it to the system it
describes**, and it is accurate on the day it is drawn. The mitigation is not technical:

- date the diagram, in the diagram
- use it for concepts that change slowly, not for topologies that change weekly
- when it must be current, it belongs in [Mermaid](../mermaid/README.md) or generated

The rule from [`../README.md`](../README.md#5-the-case-for-hand-drawn) applies: *"how does this
work?"* is a sketch, deliberately incomplete; *"what is deployed?"* is generated.

## Notes

Two boards are kept here:

| File | What it is |
|---|---|
| [`data-platform6.excalidraw`](data-platform6.excalidraw) | the data platform architecture |
| [`k8s-platform.excalidraw`](k8s-platform.excalidraw) | the Kubernetes platform |

The `6` in the first filename is worth reading as a warning: it implies five earlier versions,
which is what iterating on a binary-in-practice format looks like. There is no history to
consult, only the current file and a number.

Also in this folder: **`logo.JPG`**, which is a repository asset rather than a diagram and is in
the wrong place. It belongs wherever the portfolio site keeps its assets, not in a diagrams
folder.

Both boards are useful for the job they do — a conceptual overview of the platform — and neither
should be treated as a description of what is currently deployed. For that, this repository has
the manifests, and nothing that draws them.

---

[← Diagrams](../README.md)
