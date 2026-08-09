[← Flux](../README.md)

# tf-controller / tofu-controller

<https://github.com/flux-iac/tofu-controller>

---

## The problem it solves

Flux reconciles Kubernetes objects. Terraform provisions everything else. Between them sits the
question of who runs `terraform apply` — and the usual answer is a CI job, which reintroduces
everything GitOps was adopted to remove: a pipeline with cloud credentials, state that drifts between
runs, and no continuous reconciliation.

tf-controller makes Terraform a Flux resource. A `Terraform` custom resource points at a Flux
`GitRepository`, names a path containing `.tf` files, and the controller plans and applies it on an
interval, writing the result back as status. Drift in the cloud is corrected the same way drift in a
Deployment is.

It also supports a **plan-and-approve** flow: with `approvePlan` unset, the controller produces a
plan and waits for the plan's ID to be written into the resource before applying. That gives the
review gate Terraform users expect, expressed as a commit rather than a pipeline approval button.

The rename matters for finding things: the project began as **tf-controller** under Weaveworks and is
now **tofu-controller** under the `flux-iac` organisation, defaulting to OpenTofu. Chart names, image
names and documentation URLs are split across both spellings, which is exactly what the checked-in
manifests show.

## When to use it

- cloud infrastructure and Kubernetes workloads should live in one repository with one reconciliation
  model
- Terraform is already the tool and moving to a Kubernetes-native control plane like
  [`iac/cloud/`](../../../iac/cloud/README.md) is not on the table
- **drift correction** on cloud resources is wanted, not just apply-on-merge
- the CI system should not hold long-lived cloud credentials

## When not to use it

- **the project's maintenance status is the first thing to check.** It was orphaned when Weaveworks
  ceased operations and re-homed under `flux-iac`; activity since then has been uneven. A controller
  that holds cloud administrator credentials and applies state on a timer is the worst place to
  discover a project has stalled
- the resources are AWS, Azure or GCP objects that a native controller already covers — ACK, ASO or
  Config Connector give the same reconciliation without a second state model, see
  [`iac/cloud/`](../../../iac/cloud/README.md)
- Terraform state is already managed by a remote backend with locking that a separate team owns
- the blast radius is uncomfortable: this puts `terraform apply` on a timer, inside the cluster,
  with credentials attached

## Notes

### Links from the original note

- <https://github.com/flux-iac/tofu-controller> — the project, under its current home.
- <https://github.com/flux-iac/helloworld> — the upstream example repository the getting-started
  guide reconciles. It is the minimal working `Terraform` resource, useful for confirming the
  controller works before pointing it at anything real.
- <https://flux-iac.github.io/tofu-controller/use-tf-controller/with-azure/> — the Azure guide. This
  is the one that was followed: it is where the `ARM_*` environment-variable pattern in the
  checked-in example comes from, and it matches the Azure orientation of the rest of this platform.
- <https://github.com/flux-iac/tofu-controller/issues/1132> — a recorded issue, kept without
  commentary. It was hit or read during evaluation; the note does not say which, and the honest
  reading is that it is a known problem worth checking before adopting rather than a resolved one.

### What is checked in

A `HelmRepository` at `https://flux-iac.github.io/tofu-controller` and a `HelmRelease` installing
chart **`tf-controller` at 0.15.0** — while the values reference in the same file points at
`charts/tofu-controller/values.yaml`. Both spellings in one manifest, which is the rename showing
through the packaging rather than a mistake.

The example is a two-file Azure setup:

- `example/secret.yaml` — a `Secret` named `azure-terraform-credentials` with empty
  `ARM_SUBSCRIPTION_ID`, `ARM_TENANT_ID`, `ARM_CLIENT_ID` and `ARM_CLIENT_SECRET`. A template; the
  values are supplied elsewhere.
- `example/terraform.yaml` — a `Terraform` resource reading from the `flux-system` `GitRepository`,
  with the credentials injected into the runner pod via `envFrom`.

Two details in that resource are worth reading closely:

- **`approvePlan: auto`.** The controller applies without review. For a hello-world that is the
  point; for anything that can delete a database it removes the gate that makes Terraform tolerable.
  The alternative — omitting the field and approving by writing the plan ID into the resource — is
  the mode most estates should run in.
- **`envFrom` a `Secret` of cloud credentials.** This is the trade being made: the runner pod holds
  Azure service-principal credentials and applies on a one-minute interval. It is strictly better
  than the same credentials in a CI system, and it is still a standing grant of cloud write access
  inside the cluster. Scope the service principal narrowly.

### Two things that are stale

- **The path is wrong.** `spec.path` reads
  `./infrastructure/platform-engineering/gitops/tf-controller/tf-codes`, but this folder now lives at
  `gitops/flux/tf-controller/`. The `Terraform` resource would fail to find its source. Left as
  recorded; fix the path before reusing it.
- **`tf-codes/main.tf` is empty.** Zero bytes. The scaffolding for the Terraform code exists and the
  code was never written, which places this folder firmly at "evaluated, not adopted".

### Where this sits against the alternatives

This is the bridge between [`gitops/`](../../README.md) and [`iac/`](../../../iac/README.md), and it
is one of two ways to cross it. The other is [`iac/cloud/`](../../../iac/cloud/README.md) — ACK, ASO,
Config Connector — which expresses cloud resources as CRDs directly and has no Terraform, no state
file and no runner pod. tf-controller wins when there is existing Terraform worth keeping; the native
controllers win when there is not.

---

[← Flux](../README.md)
