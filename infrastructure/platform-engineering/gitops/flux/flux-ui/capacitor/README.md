[← Flux UIs](../README.md)

# Capacitor

<https://github.com/gimlet-io/capacitor>

---

## The problem it solves

Capacitor is a small web UI for Flux. It lists `GitRepository`, `Kustomization` and `HelmRelease`
objects, shows their reconciliation status and the workloads they produced, and puts pod logs and
Kubernetes events on the same page — so a failing deployment can be traced from the source object to
the container that will not start without changing tools.

It is deliberately not a platform. There is no authentication, no multi-tenancy and no RBAC of its
own; it renders what its service account can see. That keeps it light, and it also means the only
sensible way to expose it is behind something else.

## When to use it

- someone needs to look at Flux state and does not have or want a kubeconfig, and there is an
  authenticating proxy or ingress to put in front of it
- correlating "which source produced this pod" is done often enough that assembling it by hand is
  tedious
- a minimal viewer is wanted rather than a GitOps product with users and permissions

## When not to use it

- everyone who would look at it already has `kubectl` and the `flux` CLI — this is the recorded
  conclusion below
- it will only ever be reachable by port-forward, which requires the cluster access the UI was meant
  to avoid needing
- authentication, per-team visibility or an audit trail are requirements; it has none of these
- you want to install it as a Helm release — see the defect below

## Notes

### The Helm packaging is broken; use a Kustomization

> **"The `HelmRelease` does not work, because it loads a `readme.md` file inside the package.
> Therefore use a `Kustomization`, as the documentation suggests."**
> <https://github.com/gimlet-io/capacitor/tree/main/deploy/k8s>

A concrete, reproducible failure. The packaged chart pulls in a `readme.md` that is not a Kubernetes
manifest, and helm-controller fails rendering it — a template error rather than a deploy error, so
it never gets far enough to tell you anything useful about Capacitor itself.

The recorded resolution is the one upstream documents anyway: install from the plain manifests via a
Flux `Kustomization`. That is exactly what is checked in, and the folder shows the workings:

| File | State |
|---|---|
| `helm/ocirepository.yaml` | `OCIRepository` → `oci://ghcr.io/gimlet-io/capacitor-manifests`, tag `v0.4.8` — **active** |
| `kustomization.yaml` | `Kustomization` over that source, into `flux-system`, `prune: true`, `wait: true` — **active** |
| `helm/helmrelease.yaml` | the `HelmRelease` that failed — **commented out in full, kept as evidence** |

Leaving the broken `HelmRelease` commented out rather than deleting it is the right call: without it,
the next person re-derives the same failure from scratch.

Note that the OCI artefact is pinned to `v0.4.8` while the source of the problem is the chart, not
the manifests — so the working path and the broken path come from different packaging of the same
release.

### Reaching it

```sh
kubectl -n flux-system port-forward svc/capacitor 9000:9000
```

### The verdict

> **"I can easily see everything the dashboard has via the CLI — fairly useless."**

This is the reason nothing further was done with it, and it is worth taking at face value rather
than treating as a criticism of Capacitor specifically. Capacitor renders Flux CRD status. `flux get
all` prints Flux CRD status. For someone who already has the CLI, the dashboard adds a page load.

The judgement is conditional on the audience, which is the point made in
[`flux-ui/`](../README.md): a Flux dashboard earns its place only when the people using it do not
have cluster access — and reaching this one requires a port-forward, which requires exactly that
access. The tool was evaluated in the configuration where it cannot win.

If Capacitor were placed behind an ingress with an identity provider, and developers were the users,
the same evaluation could come out differently. Nothing in the note contradicts that; it simply was
not the situation.

---

[← Flux UIs](../README.md)
