[← Crossplane](../README.md)

# Crossview

<https://github.com/crossplane-contrib/crossview>

---

## The problem it solves

Crossplane's failure mode is not the install, it is **debugging a composite**. A claim reports
`Ready: False` and the reason is three levels down: the XR fanned out into managed resources, one
provider is rejecting one field, and finding it means walking the ownership chain with
`kubectl describe` on resource types nobody remembers the names of.

Crossview is a dashboard for exactly that chain. It reads the Crossplane objects — providers, XRDs,
compositions, composite resources, claims, managed resources — and shows them with their status
conditions, events and relationships, watching live through Kubernetes informers rather than
polling. It also handles multiple kube contexts, which matters because a Crossplane control plane
is usually not the cluster the workloads run in.

A generic dashboard from [`dashboards/`](../../../../kubernetes/managed/dashboards/README.md) will
list the same objects — they are ordinary custom resources. What it will not do is understand that
this XR owns those five managed resources, which is the whole question during an incident.

## When to use it

- Crossplane is running and someone other than its author has to debug a composite
- compositions are being written, and seeing what an XR actually produced shortens the loop
- more than one control plane, and switching contexts in a UI beats switching kubeconfigs

## When not to use it

- Crossplane is not deployed yet — which, in this repository, is the case; see
  [`crossplane/`](../README.md)
- there is no appetite for the dependencies: the default `session` auth mode needs **PostgreSQL**,
  and the chart bundles one. `auth_mode: none` drops the database and drops authentication with it,
  which is a local-only arrangement
- the access-control objection in [`dashboards/`](../../../../kubernetes/managed/dashboards/README.md)
  section 2 is unanswered. This one reads Crossplane resources cluster-wide through its own
  ClusterRole, so whoever reaches the UI sees the whole control plane regardless of their own RBAC

## Notes

- <https://artifacthub.io/packages/helm/crossview/crossview> — the chart on Artifact Hub.
- The project is in `crossplane-contrib`, not `crossplane` — community, not core. Releases are
  frequent and the version numbers move fast (v4.x already), which is worth knowing before pinning
  expectations to it.

### What is checked in

An `OCIRepository` at chart **4.6.0** with tag and digest, a `HelmRelease` and a namespace. The
chart is published to GHCR as an OCI artefact, so this follows the normal
[pattern](../../../../gitops/flux/README.md) rather than needing a `HelmRepository` — upstream also
serves a classic repository from GitHub Pages, which is not used here.

Two things in the values are deliberate:

- **`secrets.dbPassword` and `secrets.sessionSecret` are empty.** The chart creates its Secret from
  any non-empty string it finds there, so committing a real value would commit a credential. Fill
  them in before applying, or replace each with the `secretKeyRef` form the chart supports and keep
  the Secret out of Git.
- **`database.enabled: true`** keeps the bundled PostgreSQL, whose image is `postgres:latest`. That
  is fine for a lab and is not a tag to leave unpinned for anything else — point
  `config.database.host` at a real instance instead, for example one from
  [CloudNativePG](../../../../../databases/sql/README.md).

`ingress.enabled: false`: reaching it is a `kubectl port-forward` on port 80 of the service, which
is the right default while the authentication story above is unresolved.

---

[← Crossplane](../README.md)
