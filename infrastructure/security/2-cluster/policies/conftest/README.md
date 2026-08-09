[← Admission policies](../README.md)

# Conftest

<https://github.com/open-policy-agent/conftest>

---

## The problem it solves

[Gatekeeper](../gatekeeper/README.md) enforces Rego policy **at admission** — the last honest
checkpoint, and also the latest possible one. By then the manifest is merged, the pipeline is green,
and the person who wrote it has moved on. The rejection surfaces as a failed reconcile rather than
as a review comment.

Conftest runs **the same Rego, against files, in CI**. Same language, same policy logic, hours
earlier and attached to a diff.

```bash
conftest test deployment.yaml
conftest test --policy ./policy manifests/
```

That is the whole idea, and it is the reason it belongs in this folder rather than in a scanners
folder: it is not another manifest checker, it is **the shift-left half of the policy story**.

## The pairing that makes it worth adopting

| | [Gatekeeper](../gatekeeper/README.md) | Conftest |
|---|---|---|
| Runs | in the cluster, at admission | in CI, on files |
| Sees | every object, from every path | only what CI is pointed at |
| Language | **Rego** | **Rego** |
| Timing | after merge | **before merge** |
| Bypassable | no | yes — anything not going through CI |
| Feedback | a failed reconcile | a pull-request comment |

Neither replaces the other, and the reason is the "bypassable" row.
[`../README.md`](../README.md#1-where-admission-sits) makes the point that CI is not a boundary:
`kubectl apply` from a laptop, a controller creating objects, or a Helm hook all skip it entirely.
Admission is the only checkpoint everything passes through.

But admission is a bad **feedback** mechanism. It says no at the point where saying no is most
expensive.

Running both — the same policy source, evaluated in CI and enforced at admission — is the shape
worth aiming at, and it is only possible because both speak Rego.

## More than Kubernetes

The other reason to know about it: conftest tests **any structured configuration**, not just
manifests.

| Format | What you would check |
|---|---|
| Kubernetes YAML | the same rules Gatekeeper enforces |
| **Terraform / HCL** | an S3 bucket without encryption, a security group open to the world |
| **Dockerfile** | a forbidden base image, `USER root`, an unpinned tag |
| JSON, TOML, INI, CUE | anything with a schema and a rule |
| `docker-compose` | for the parts of an estate that are not Kubernetes |

That breadth overlaps [checkov](../../manifest-scan/checkov/README.md), and the difference is who
writes the rules: checkov ships a large library of built-in policies, conftest ships **none** and
expects you to write them. Which is better depends on whether the requirement is "cover the common
mistakes" or "enforce our specific rules".

## When to use it

- **Gatekeeper is already deployed**, and the same policies should fail in CI as well
- organisation-specific rules that no built-in policy library covers
- policy needed over Terraform or Dockerfiles as well as manifests
- Rego is already a skill on the team — this is the way to get more value from it

## When not to use it

- **Rego is not already in play.** Learning it to gate a pipeline is a real cost, and
  [Kyverno](../kyverno/README.md)'s YAML plus its CLI covers the same shift-left case without it
- a library of ready-made security rules is what is wanted —
  [checkov](../../manifest-scan/checkov/README.md) or [kube-linter](../../manifest-scan/kube-linter/README.md)
- **as the enforcement point.** It is a CI check, and CI is bypassable — see the table above
- structural validation is the actual need — that is
  [flux-schema](../../../../devops/scanners/manifest/flux-schema/README.md) or
  [kubeconform](../../../../devops/scanners/manifest/kubeconform/README.md)

## Render first

The same caveat that applies to every file-based check in this repository: **Helm templates are Go
templates, not YAML.** Conftest must run on `helm template` or `kustomize build` output, or it is
testing something that never reaches the cluster.

Conftest can also **pull policies from an OCI registry** (`conftest pull`), which is the mechanism
for sharing one policy set across repositories rather than copying Rego between them. On a platform
already running a registry — see [`devops/image/oci-registry/`](../../../../devops/image/oci-registry/README.md)
— that is a small addition rather than new infrastructure.

## Notes

Added to the catalogue from <https://github.com/open-policy-agent/conftest>. It is an Open Policy
Agent project, Apache 2.0, and a CNCF-hosted one.

Nothing is deployed — it is a CLI, and unlike the other three tools in this folder it does not run
in the cluster at all. That is worth stating plainly, because it sits here for its **relationship**
to Gatekeeper rather than because it is admission control.

**Where this lands for pikakube.** [Kyverno](../kyverno/README.md) is what is actually deployed here,
not Gatekeeper — which weakens the main argument, since the shared-Rego story needs Gatekeeper on the
other end. Kyverno has its own CLI (`kyverno apply`, `kyverno test`) that fills the same shift-left
slot in YAML, and for a platform standardised on Kyverno that is the more consistent choice.

Conftest becomes the right answer here in two cases: if Rego enters the picture through Gatekeeper,
or if policy is needed over **Terraform and Dockerfiles** as well as manifests — where Kyverno's CLI
does not reach and conftest does.

The broader point it illustrates is the one worth taking regardless of tool:
[`../README.md`](../README.md#4-audit-vs-enforce) argues for starting in audit mode, and a CI check
is audit mode with better ergonomics — the policy runs, the failure is visible, and nothing is
blocked until you decide it should be.

---

[← Admission policies](../README.md)
