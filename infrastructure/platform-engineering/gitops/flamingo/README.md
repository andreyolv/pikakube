[← GitOps](../README.md)

# Flamingo

<https://github.com/flux-subsystem-argo/flamingo>

---

## The problem it solves

The Flux-versus-Argo-CD argument usually reduces to one thing: Flux has the better controller
architecture, Argo CD has the UI people want. Flamingo — the Flux Subsystem for Argo — is the
attempt to stop choosing.

It runs Flux as the reconciler and Argo CD as the **viewer**. Flux `Kustomization` and `HelmRelease`
objects are surfaced in the Argo CD interface as Applications, so the resource tree, health status
and diff view all work, while the actual reconciliation is being done by Flux controllers reading
Flux CRDs.

That resolves the specific complaint recorded in [`argocd/`](../argocd/README.md): the objections
there are about Argo CD's architecture and secret handling, not its dashboard. Flamingo keeps the
dashboard and moves the architecture underneath it.

## When to use it

- Argo CD is already established as the interface teams use, and replacing it is a political problem
  rather than a technical one
- you want Flux semantics — `HelmRepository` as an object, `valuesFrom` secrets, per-function
  controllers — without removing the UI people have bookmarked
- a migration from Argo CD to Flux needs an intermediate state where both are true at once
- multiple teams disagree on the tool and a shared surface is worth more than a clean stack

## When not to use it

- there is no Argo CD in the picture — this adds a second system to get a UI, and
  [`flux-ui/`](../flux/flux-ui/README.md) is the cheaper answer to that
- the platform is committed to Flux and nobody misses the dashboard
- you are unwilling to run a component that sits between two upstreams and has to track both; the
  compatibility surface is the whole point of the project and also its risk
- the requirement is Argo CD's ecosystem (Rollouts, Workflows) rather than its UI — those work
  against Argo CD regardless

## Notes

The original note was the project link alone, with no commentary:

- <https://github.com/flux-subsystem-argo/flamingo>

What is checked in beside it is a single `flamingo.yaml` containing an `OCIRepository` pointing at
`oci://ghcr.io/flux-subsystem-argo/flamingo/manifests` at tag `latest`, and a `Kustomization`
reconciling the `./demo` path from it. That is the project's own demo bundle — an evaluation, not a
deployment. Two things follow from reading it:

- **It installs itself the Flux way.** The subsystem is delivered as an OCI artefact and reconciled
  by Flux, which is consistent with the argument the project is making.
- **The tag is `latest`.** For a demo that is fine; for anything else it defeats the point of GitOps,
  because the desired state in Git does not change when the deployed state does. Pin a version
  before this leaves evaluation.

The absence of any recorded opinion is itself informative. Every other tool in this folder that was
actually used produced commentary; this one produced a manifest and a link. It was looked at, not
adopted — which is consistent with the platform having already settled on Flux without needing to
keep an Argo CD interface alive.

---

[← GitOps](../README.md)
