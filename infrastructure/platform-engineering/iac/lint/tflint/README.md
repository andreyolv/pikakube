[← IaC linting](../README.md)

# TFLint

<https://github.com/terraform-linters/tflint>
<https://github.com/terraform-linters/tflint-ruleset-terraform>
<https://github.com/terraform-linters/tflint-ruleset-aws>
<https://github.com/terraform-linters/setup-tflint>

---

## The problem it solves

`validate` checks that HCL is well-formed. `plan` checks it against a real cloud API, which costs
credentials and a round trip. TFLint sits between them: it embeds provider schemas as plugins, so it
can tell you that an instance type does not exist, that an argument was deprecated, or that a value
is outside the allowed set — **without any credentials at all**.

It also enforces the things `validate` has no opinion about: unused declarations, missing variable
types, module source pinning, and naming conventions.

The provider plugin is where nearly all the value is. Without one, TFLint runs a small set of generic
rules; with the AWS, Azure or Google plugin installed it knows the actual API surface, and that is
the difference between a style checker and a correctness checker.

It works on OpenTofu as well as Terraform — the configuration language is the same, which is the
whole point of the fork described in [`engine/`](../../engine/README.md).

## When to use it

- any repository containing HCL, from the first file
- **in CI, on the pull request**, before `plan` — it is the check that runs without handing a branch
  cloud credentials
- as a pre-commit hook as well, so CI is rarely the first place a problem appears
- when module source pinning and variable typing should be enforced rather than remembered

## When not to use it

- as a **security or policy scanner** — it is not one. Public buckets, unencrypted volumes and open
  security groups need Checkov, Trivy, tfsec or Conftest/OPA, and expecting TFLint to cover them
  leaves the gap unnoticed
- as a replacement for `plan`; it does not know what exists in the account or what will change
- on Pulumi or CDK code — this is an HCL tool
- with every rule enabled at once, which produces a backlog large enough that the tool gets removed

## The pieces you actually install

TFLint is three things in a trench coat, and the split is not obvious from the project page. Getting
it wrong is how a repository ends up with a linter that runs, passes, and checks almost nothing.

| Piece | What it is | Do you install it? |
|---|---|---|
| **tflint** | the engine — parses HCL, loads plugins, applies configuration | yes |
| [**tflint-ruleset-terraform**](https://github.com/terraform-linters/tflint-ruleset-terraform) | the **language** ruleset — the rules about Terraform itself | **no: it is bundled** |
| [**tflint-ruleset-aws**](https://github.com/terraform-linters/tflint-ruleset-aws) | the **provider** ruleset — 700+ rules about AWS resources | **yes, explicitly** |
| [**setup-tflint**](https://github.com/terraform-linters/setup-tflint) | the GitHub Action that installs the engine on a runner | in CI |

**The language ruleset is built in** (TFLint v0.46+), so `tflint -v` reports its bundled version and
there is nothing to declare. It owns the checks that apply regardless of provider: module sources
pinned to a version, variables and outputs carrying types and descriptions, deprecated syntax,
declarations that nothing references, naming conventions. Those are the rules most worth turning on
early, because they are about hygiene rather than about a cloud API, and they never produce a
finding that depends on credentials.

**The provider ruleset is the one that has to be declared, and it is where the value is.** Without
it, TFLint is a style checker; with it, it knows the AWS API surface — an instance type that does not
exist, an argument the provider has deprecated, an enum value outside the allowed set. Both the
plugin and its version go in `.tflint.hcl`, and `tflint --init` fetches it:

```hcl
plugin "aws" {
  enabled = true
  version = "0.48.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}
```

Two things to know before relying on it: a large share of the 700+ rules — the best-practice and
naming ones — are **disabled by default** and must be enabled deliberately, and the same applies for
Azure and Google via their own rulesets. The default state is therefore quieter than the rule count
suggests, which is a good default and a poor assumption.

**`setup-tflint` installs the engine in CI, and that is all it does.** Three consequences follow, all
of them recorded elsewhere on this page and all of them routinely missed:

- **`tflint --init` still has to run** after the install, or the plugin is absent and the job passes
  having checked the generic rules only. A green pipeline that verifies nothing is worse than no
  pipeline
- **give it a token.** Plugins are fetched from GitHub releases, and an unauthenticated runner hits
  the anonymous rate limit exactly when several jobs run at once. The action takes a token input for
  this
- **pin the action to a commit SHA, and the TFLint version explicitly** — the same rule as any
  third-party action ([GitHub Actions §8](../../../../devops/cicd/github-actions/README.md#8-anti-patterns)),
  compounded here because the tool being installed adds rules between releases

## Notes

The original note was a single link with no commentary:

- <https://github.com/terraform-linters/tflint>

Nothing is configured and there is nothing here to lint —
[`engine/`](../../engine/README.md) contains no HCL, and the only `.tf` file in this repository is
`tf-codes/main.tf` under
[tf-controller](../../../gitops/flux/tf-controller/README.md), which is empty. TFLint is recorded as
the tool to use, ahead of any code existing to use it on.

Three things to settle when that changes, none of them obvious from the project page:

- **Install a provider plugin and pin it.** The generic ruleset is thin. `.tflint.hcl` declares the
  plugin and its version, and `tflint --init` fetches it. Without this step the tool appears to work
  and catches almost nothing.
- **Pin TFLint itself in CI.** New releases add rules, and an unpinned linter makes unrelated pull
  requests start failing for reasons nobody changed.
- **Decide which rules fail the build.** Correctness rules can block from day one and nobody will
  argue. Style and naming rules on an existing codebase produce a wall of findings; enable those
  deliberately, in batches, with the fixes in the same pull request.

The reason this matters more than it looks: the
[tf-controller](../../../gitops/flux/tf-controller/README.md) example runs with `approvePlan: auto`,
which means an apply happens on an interval with no human reading a plan. In that configuration a
linter in CI is not a nicety — it is the last gate between a commit and a change to a real
subscription.

---

[← IaC linting](../README.md)
