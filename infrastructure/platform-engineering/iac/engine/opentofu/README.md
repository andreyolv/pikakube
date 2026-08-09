[← IaC engines](../README.md)

# OpenTofu

<https://github.com/opentofu/opentofu>
<https://github.com/opentofu/setup-opentofu>

---

## The problem it solves

OpenTofu is Terraform, forked at the last version published under the Mozilla Public License and
donated to the Linux Foundation after HashiCorp moved Terraform to the Business Source Licence.

The compatibility is the point. Same HCL, same state file format, same provider protocol, same
module registry — an existing Terraform codebase runs with the binary name changed. Migration is
mechanical rather than a rewrite, which is what makes the fork a real option rather than a protest.

Since the fork it has added things of its own, and two are worth knowing because Terraform does not
have them:

- **State encryption**, built in. The state file is the credential store nobody admits to having —
  see [`iac/`](../../README.md) section 3 — and encrypting it at rest is otherwise the backend's
  problem.
- **Early variable evaluation**, which allows variables in places HCL previously would not accept
  them, including backend configuration.

## When to use it

- new infrastructure code where HCL is the right level and the licence should be unambiguous
- an existing Terraform estate where BSL is a legal or policy problem
- the team is more comfortable reviewing a declarative description than reading a program — see
  [`engine/`](../README.md) section 2
- provider coverage is the deciding factor; the Terraform provider ecosystem works here unchanged

## When not to use it

- Terraform Cloud, Sentinel or another HashiCorp-specific product is part of the workflow
- an existing Terraform estate is working and the licence is genuinely not a concern — migrating for
  features alone does not pay
- the resources are Kubernetes objects; that belongs to [`gitops/`](../../../gitops/README.md), not
  to any engine
- continuous reconciliation is the requirement rather than reviewed applies — see
  [`cloud/`](../../cloud/README.md) or
  [tf-controller](../../../gitops/flux/tf-controller/README.md)

## Notes

Two links were recorded, and the second says more than it appears to:

- <https://github.com/opentofu/opentofu> — the project.
- <https://github.com/opentofu/setup-opentofu> — the **GitHub Action** that installs the binary in a
  workflow, the OpenTofu equivalent of `hashicorp/setup-terraform`. Recording the action alongside
  the project means the intended execution model was CI rather than a laptop, which is the correct
  instinct: applies from a workstation leave no audit trail and take no lock.

Nothing else was written. In a folder where [Pulumi](../pulumi/README.md) attracted two blunt
dismissals, an entry with no complaints attached is a quiet endorsement — OpenTofu was looked at, it
behaved as expected, and there was nothing to record.

Nothing is provisioned here. If that changes, the setup-action link is the right starting point and
the rules in [`iac/`](../../README.md) section 3 are the things to settle before the first `apply`:
a remote backend with locking, state treated as a secret, pinned providers, and state split by
lifecycle rather than one file for the estate.

One thing OpenTofu makes cheaper than Terraform does: with built-in state encryption there is no
excuse for an unencrypted state file, and the setting belongs in the backend block from the first
commit rather than after the first audit.

---

[← IaC engines](../README.md)
