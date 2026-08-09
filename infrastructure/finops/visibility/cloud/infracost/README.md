[← Cloud cost visibility](../README.md)

# Infracost

<https://github.com/infracost/infracost>
<https://github.com/infracost/actions>
<https://github.com/infracost/vscode-infracost>

---

## The problem it solves

Cloud cost is discovered after the fact. Something is merged, applied, and appears on an invoice
weeks later — when the resource is running, something depends on it, and removing it is a project.

Infracost prices infrastructure as code **before it is applied**. It parses a Terraform plan or the
HCL directly, looks each resource up in a pricing API, and produces the monthly cost — and, more
usefully, the **delta** the change introduces. Wired into CI, that delta becomes a comment on the
pull request, next to the diff, at the only moment when changing the answer is free.

It is the only serious tool in this category. The CLI is Apache-2.0; the hosted dashboard
(Infracost Cloud) is the commercial part, and the CLI works without it.

## When to use it

- **Terraform in pull requests**, which is where nearly all of its value is
- when infrastructure changes are reviewed by people who do not price them mentally
- catching the expensive mistakes that look identical in a diff to the cheap ones — an instance
  family bumped one size, a disk tier changed, a NAT gateway added per subnet
- locally, before opening the pull request — the VS Code extension shows cost inline in the editor

## When not to use it

- **with Crossplane**, or anything else that reconciles continuously instead of producing a plan.
  There is no plan to price — see the notes
- as a build gate. A cost check that fails builds gets bypassed, then deleted
- for Kubernetes cost. It prices the node pools the plan declares and knows nothing about the pods
  that determine how many exist — [`kubernetes/`](../../kubernetes/README.md)
- for what is actually running. It prices what the code says, which drifts from reality
- as the FinOps programme. It is preventive, and it does not attribute a single euro of existing
  spend

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/infracost/infracost>** — the CLI. Apache-2.0, actively maintained, and the
piece that does the work. Pricing comes from a hosted pricing API (a free key is required, and it
can be self-hosted); the CLI submits resource attributes, not your Terraform state.

**<https://github.com/infracost/vscode-infracost>** — the VS Code extension. Cost annotations inline
in the editor while writing the Terraform, which is earlier still than the pull request. Underrated:
it removes the round trip entirely for the person making the change.

**<https://github.com/infracost/actions>** — the GitHub Actions integration. See the complaint below.

**"not support for crossplane" — <https://github.com/infracost/infracost/issues/937>** — *"Add
support for Crossplane"*, opened September 2021 and **closed** without shipping it. This is a
structural limitation, not an oversight. Infracost prices a **plan** — a declared set of resources
with attributes, produced before anything is applied. Crossplane has no plan phase: you apply a
Composite Resource and a controller reconciles cloud resources toward it, continuously. There is
nothing to price ahead of time.

The consequence for a platform moving toward Crossplane is that pull-request cost estimation simply
stops being available for whatever moves. The realistic mitigations are (a) pricing at design time
rather than review time, and (b) leaning harder on after-the-fact tools — the cluster-side
[`kubernetes/`](../../kubernetes/README.md) tools and cloud cost exporters — because prevention is
no longer on the table.

**"Preferable via the GitHub App, but then you need to be an owner of the GitHub organisation. Via
GitHub Actions it is absolute rubbish."** Both halves of this are worth keeping.

The **GitHub App** is the good path: installed once at organisation level, it comments on pull
requests across every repository with no per-repository workflow to maintain, no secrets to
distribute, and nothing to keep in step as the repositories multiply. The catch is exactly as
recorded — installing an App requires GitHub **organisation owner** rights, which the person adopting
the tool usually does not have. That is an access problem, not a technical one, and it is the most
common reason Infracost is evaluated and then not adopted.

**<https://github.com/infracost/actions/tree/master/diff>** — the fallback path, and the target of
the second complaint: *"totally abandoned, no updates, a rubbish abstraction that ridiculously
requires creating a checkout step beforehand."*

The substance: `actions/diff` is a thin composite action wrapping CLI commands. It does not manage
its own inputs, so the workflow has to check out the repository, set up Terraform, and arrange
credentials before it runs — at which point the action is adding indirection rather than removing it.
Calling the CLI directly is more code in the workflow and less to be surprised by.

The practical reading: **if you can get the GitHub App installed, use it.** If you cannot, prefer
invoking the CLI in the workflow over the composite actions, and treat this repository as a source
of examples rather than as a dependency.

**Nothing is deployed for this in the repository**, and nothing should be — Infracost is a CI
concern, not a cluster component. Its place is `devops/cicd/`, not here. What this folder records is
the evaluation and the two reasons it has not been adopted: the organisation-ownership barrier, and
the Crossplane gap.

---

[← Cloud cost visibility](../README.md)
