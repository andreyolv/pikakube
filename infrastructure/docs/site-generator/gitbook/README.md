[← Site generators](../README.md)

# GitBook

<https://github.com/GitbookIO/gitbook>

---

## What it is

A **hosted** documentation platform with a WYSIWYG editor, synchronised bidirectionally with a
Git repository. That makes it the odd entry in this folder: everything else here is a generator
you run, and this is a product you subscribe to.

The distinction that matters is who writes:

| | GitBook | The generators in this folder |
|---|---|---|
| Written in | a web editor | a text editor, in the repository |
| Review | in the platform | pull requests |
| Hosting | theirs | yours |
| Git sync | bidirectional | the repository *is* the source |
| Cost | subscription | free |
| Audience for authoring | **anyone** | people comfortable with Git |

## When to use it

- **the people who must write are not engineers** — product, support, customer success
- an editing experience is what stands between having documentation and not having it
- hosting, search and access control should be somebody else's problem
- customer-facing documentation where presentation matters and there is no front-end effort to
  spend on it

## When not to use it

- documentation should live beside the code and be reviewed in the same pull request — every
  other tool in this folder
- vendor lock-in for the documentation of a platform is unattractive
- the content is technical and its authors are engineers, who will find the editor slower than
  their own
- there is no budget; this is the only paid option here

## The honest framing

The reason to choose GitBook is almost never technical. It is that **non-engineers will write in
it and will not write in a repository**, and documentation that exists beats documentation that
would have been better structured.

Its bidirectional Git sync softens the trade — the content is genuinely in a repository, so it
can be extracted later. It does not remove it: the editing workflow, the review process and the
hosting are all in the platform, and moving away means rebuilding those.

For a platform team documenting its own infrastructure, the case is weak. For a company
documenting a product to customers, with writers who are not engineers, it is often correct.

Note also that the historic open-source GitBook CLI is effectively unmaintained. The current
product is the hosted one, and evaluating it means evaluating a subscription.

## Notes

Not used here, and it is the least likely of the five to be. This repository's documentation is
written by an engineer, in the repository, reviewed as code — which is the exact case GitBook is
not for.

Mapped for completeness, and because "why not GitBook" is a question with a real answer worth
recording: the audience for authoring is one person who is comfortable with Git, so the thing it
sells is not the constraint.

---

[← Site generators](../README.md)
