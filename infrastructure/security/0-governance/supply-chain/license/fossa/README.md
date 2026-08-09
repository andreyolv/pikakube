[← License compliance](../README.md)

# FOSSA

<https://github.com/fossas/fossa-cli>
<https://github.com/fossas/fossa-action>

---

## The problem it solves

Licence compliance stops being a scan and becomes a **process** as soon as anyone has to
review findings, grant exceptions, track obligations and produce attribution for a shipped
product. At that point the missing piece is not detection — it is workflow: a queue, reviewers,
policies with owners, exceptions that expire, and a record that stands up to an audit.

FOSSA is the commercial SaaS for that. The CLI (`fossa-cli`) resolves dependencies from the
build and uploads the result; the platform does licence identification, applies organisational
policy, routes findings to reviewers, tracks obligations, and generates attribution reports.
`fossa-action` is the GitHub Action wrapper that puts the CLI in a workflow.

The trade against [ORT](../ort/README.md) is direct and worth naming: FOSSA buys the workflow,
the maintained licence knowledge base and somebody else's operational burden, in exchange for
money and for dependency metadata leaving the organisation. ORT gives the same technical
capability and keeps everything in-house, at the cost of building the process yourself.

## When to use it

- compliance is an **ongoing programme** with legal reviewers, not a periodic check
- a commercial product is distributed and attribution reports are a recurring deliverable
- the organisation wants a maintained licence knowledge base rather than curating upstream
  metadata itself
- policy has to be enforced across many repositories and teams uniformly, with a central view
- there is budget, and engineering time is the scarcer resource

## When not to use it

- a personal or internal-only project. The exposure does not justify a commercial platform —
  see the assessment in [`../README.md`](../README.md#10-how-this-applies-to-pikakube)
- when dependency metadata cannot leave the organisation. It is SaaS; the dependency graph goes
  to a third party, which is itself a review in some environments
- when open source and self-hosting are requirements — [ORT](../ort/README.md) covers the same
  technical ground
- as a cheap CI gate. [grant](../grant/README.md) over an existing SBOM does that for nothing
- if there is no reviewer. A workflow product with nobody in the workflow is an expensive
  scanner

## Notes

Original references recorded for this tool:

> <https://github.com/fossas/fossa-cli>
> <https://github.com/fossas/fossa-action>

Both repositories are open source; **the platform they report to is not**. That is the shape of
the product and it is worth being explicit about, because "FOSSA is on GitHub" leads people to
assume it can be run standalone. The CLI without an account produces very little.

The other thing worth knowing is *how* the CLI resolves dependencies: it prefers to work from
the **build**, invoking or observing the package manager rather than parsing manifests
statically. That is more accurate for languages where the resolved graph depends on build
configuration — Gradle and Maven especially — and it is also why CI integration can be fiddly:
the analysis needs the build environment, not just the source tree. Budget for that when
estimating adoption effort, since it is the part that differs most from tools that read
lockfiles.

---

[← License compliance](../README.md)
