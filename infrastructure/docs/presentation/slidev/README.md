[← Presentations](../README.md)

# Slidev

<https://github.com/slidevjs/slidev>

---

## What it is

Slides for developers, built on Vue. Markdown is the source, and the deck is a real application —
which is what makes the features possible.

| Capability | Why it is the reason to choose it |
|---|---|
| **Embedded Monaco editor** | live-editable, runnable code in the slide |
| Animations and transitions | click-through reveals, `v-click` directives |
| **Presenter mode** | notes, a timer, and the next slide on a second screen |
| Drawing | annotate over the slide while presenting |
| Mermaid, LaTeX | rendered inline |
| Vue components | anything you can build, embedded in the deck |
| Export | PDF, PNG, or a hosted single-page application |

The live code editor is the genuine differentiator. A technical talk that involves showing code
running, and changing it in response to a question, is a different experience from a screenshot.

## When to use it

- a **conference talk** or a public technical presentation
- live code is part of the material
- animation and build-up genuinely help the explanation
- hosting the deck as a site afterwards is useful

## When not to use it

- an internal update, an architecture walkthrough, a sprint review —
  [Marp](../marp/README.md) is one file and enough
- somebody needs to open it in PowerPoint — Marp exports PPTX, this does not
- nobody wants to maintain a Vue project to present five slides
- it would be presented once and never again

## The cost

It is a Node project: `node_modules`, a dev server, and a build that can break on a dependency
upgrade. For a deck presented once, that is a lot of scaffolding.

There is also a subtler cost. Once a deck uses Vue components and custom layouts, it stops being
portable Markdown — reusing the content elsewhere means extracting it, not copying it.

## Slidev or Marp

| | Slidev | Marp |
|---|---|---|
| Setup | a project | **a file** |
| Live code | **yes** | no |
| PPTX export | no | **yes** |
| Editor preview | dev server | VS Code, as you type |
| Right for | a conference talk | everything else |

## Notes

Not used here. Mapped as the answer for the case [Marp](../marp/README.md) does not cover — a
public technical talk where live code is part of the point.

For the realistic use in this repository — an onboarding walkthrough of the platform, built from
the existing capability READMEs — Marp is the fit, because the content is prose and Mermaid
diagrams rather than runnable code.

---

[← Presentations](../README.md)
