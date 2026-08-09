[← Admission control](../README.md)

# Open Policy Containers

<https://github.com/opcr-io/policy>

---

## The problem it solves

Read the name carefully, because it is easy to misread: this is **not** another image signature
verifier. Open Policy Containers (OPCR) is about the opposite direction of travel — it treats
**OPA policy itself as an OCI artefact**.

The observation behind it: policy has all the same distribution problems as application code —
it needs versions, immutable references, a registry, provenance, and a way to promote a tested
bundle from staging to production. Most OPA deployments solve none of that. Policy arrives as a
ConfigMap, as files baked into an image, or fetched from an HTTP bundle server with no
signature and no version discipline.

OPCR's `policy` CLI makes policy behave like a container image, with deliberately familiar
verbs:

```bash
policy build ./src -t myregistry.io/policies/authz:1.2.0   # compile Rego into an OCI artefact
policy push  myregistry.io/policies/authz:1.2.0            # store it in any OCI registry
policy pull  myregistry.io/policies/authz:1.2.0            # fetch it anywhere
policy run   myregistry.io/policies/authz:1.2.0            # evaluate it locally
```

What that buys:

| Property | Consequence |
|---|---|
| Policy has an immutable digest | "which policy was in effect" has an exact answer |
| Any OCI registry works | no new infrastructure — the registry you already run distributes policy too |
| Policy can be **signed** | with Cosign, like any other OCI artefact, and therefore verified before it is loaded |
| Policy can be promoted | tag, retag, promote across environments using the same mechanics as images |

The connection back to this folder closes the loop nicely: admission control verifies signed
images, and OPCR lets you verify the **signed policy** doing the verifying. An unsigned,
unversioned policy bundle is a supply-chain gap in the control plane of your supply-chain
controls.

## When to use it

- **OPA is used broadly, beyond admission control** — API authorisation, application-level
  authz, gateway policy — and policy distribution has become an unmanaged problem
- **You need to know exactly which policy was in force** at a point in time, for audit
- **Policy is promoted through environments** and you want the same immutable-digest promotion
  model you use for images
- **You want signed policy bundles**, verified before loading, using the tooling and registry you
  already have
- **Policy is authored by one team and consumed by many** — a registry with versioned, signed
  artefacts is a far better contract than a shared Git directory

## When not to use it

- **You expected an image verifier.** For "only signed images may run", the tools are
  [sigstore policy-controller](../sigstore-policy-controller/README.md),
  [Connaisseur](../connaisseur/README.md) and [Ratify](../ratify/README.md), or Kyverno's
  `verifyImages`. OPCR does not do this
- **Your policy is Kyverno.** Kyverno policies are Kubernetes resources, delivered by GitOps —
  which already gives versioning and provenance through the Git repository. OPCR solves a problem
  Kyverno users do not have
- **A handful of Rego files in one repository.** OCI packaging is overhead you do not need at
  that scale; OPA's native bundle mechanism is enough
- **Without checking the project's activity.** See the note below

## Notes

Original note recorded for this tool:

- <https://github.com/opcr-io/policy> — the `policy` CLI, from the Open Policy Containers
  project (built by the team behind Aserto). The repository documents the build/push/pull/run
  verbs, the OCI media types used for policy artefacts, and the signing and verification flow.

Two honest caveats:

- **Check the maintenance status before adopting it.** OPCR is a small project with a narrow
  audience, and its activity has been intermittent. Nothing here depends on it, so this is a
  cheap check to make before it becomes a dependency.
- **The name causes real confusion.** "Open Policy Containers" reads as "policy for containers",
  which is what its position in this folder suggests. It is actually *policy packaged as
  containers*. Anyone skimming this tree will misread it at least once — which is precisely why
  it is worth writing down.

No manifests are committed for this tool; it is a CLI and a packaging convention, not a cluster
component.

---

[← Admission control](../README.md)
