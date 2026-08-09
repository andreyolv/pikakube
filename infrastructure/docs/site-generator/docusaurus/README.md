[← Site generators](../README.md)

# Docusaurus

<https://github.com/facebook/docusaurus>

---

## The problem it solves

Documentation that is a **product** rather than a folder: several versions live at once, it is
translated, it has a blog, and the prose contains interactive components.

Those requirements are what MkDocs does not cover, and they are the entire reason to accept a
React build in exchange.

| Capability | Why it is the differentiator |
|---|---|
| **Versioning** | v1, v2 and v3 published simultaneously, with a switcher — built in, not a plugin |
| **i18n** | translations as a first-class concept, with per-locale routing |
| **MDX** | React components inside the Markdown — live examples, interactive widgets |
| Blog | release notes and announcements alongside the documentation |
| Plugin ecosystem | search, OpenAPI rendering, analytics |

## When to use it

- documentation for a **released product** where old versions must stay published
- more than one language
- interactive examples embedded in the prose, not linked from it
- a front-end team already works in React, so the stack is free

## When not to use it

- internal platform documentation — the weight is real and unrewarded
  ([MkDocs](../mkdocs/README.md))
- nobody on the team wants to maintain a Node project to publish Markdown
- the content is prose and will stay prose
- versioning enabled "just in case", which multiplies every future edit

## The cost, stated plainly

It is a React application. That means `node_modules`, a build that can break on a dependency
upgrade, and MDX syntax errors that fail the build rather than rendering oddly.

MDX is the specific trap: once components are embedded, the content is no longer portable
Markdown. Migrating away later means rewriting rather than copying.

Versioning has a similar shape. It is excellent, and it means a correction to a paragraph must be
applied to every published version — which is correct behaviour and considerably more work than
people expect when they enable it before needing it.

## Docusaurus or MkDocs

| | Docusaurus | MkDocs + Material |
|---|---|---|
| Stack | React, Node | Python |
| Config | JavaScript | one YAML file |
| Versioning | built in, strong | via `mike` |
| i18n | built in | plugin |
| Components in content | **yes, MDX** | no |
| Time to a working site | an afternoon | ten minutes |
| Portability of the content | reduced by MDX | plain Markdown |

Both produce a good site. The question is only whether the three capabilities in the middle rows
are needed — if not, the bottom two rows decide it.

## Notes

Not used here. It is mapped as the answer for the case
[MkDocs](../mkdocs/README.md) does not cover, so that "we need versioned documentation" has a
recorded destination rather than becoming a discussion.

---

[← Site generators](../README.md)
