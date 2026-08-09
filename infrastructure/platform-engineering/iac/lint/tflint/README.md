[← IaC linting](../README.md)

# TFLint

<https://github.com/terraform-linters/tflint>

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
