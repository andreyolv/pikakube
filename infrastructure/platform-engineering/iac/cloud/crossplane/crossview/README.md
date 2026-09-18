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

- **`adminPassword`, `dbPassword` and `sessionSecret` are `secretKeyRef`s.** The chart takes either
  a literal string — which it bakes into its own `crossview-secrets` Secret, so committing one
  would commit a credential — or a `secretKeyRef`, which it wires straight into the env and leaves
  out of that Secret. These three use the second form and read from a `crossview-auth` Secret that
  is **not in Git**; create it once per cluster before applying:

  ```sh
  kubectl create secret generic crossview-auth -n crossview \
    --from-literal=db-password="$(openssl rand -hex 16)" \
    --from-literal=admin-password='<pick one>' \
    --from-literal=session-secret="$(openssl rand -hex 32)"
  ```

  Leaving a value as `""` instead is not a working default: the chart drops empty keys entirely, so
  PostgreSQL comes up with no `POSTGRES_PASSWORD` and crash-loops on `Database is uninitialized and
  superuser password is not specified`, which leaves the app's `wait-for-db` init container hanging
  at `Init:0/1`. Only `adminUsername` stays a literal — it is not a credential.
- **`database.enabled: true`** keeps the bundled PostgreSQL, whose image is `postgres:latest`. That
  is fine for a lab and is not a tag to leave unpinned for anything else — point
  `config.database.host` at a real instance instead, for example one from
  [CloudNativePG](../../../../../databases/sql/README.md).

`ingress.enabled: false`: reaching it is a `kubectl port-forward` on port 80 of the service, which
is the right default while the authentication story above is unresolved.

---

[← Crossplane](../README.md)
