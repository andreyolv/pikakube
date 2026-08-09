[← Dashboards](../README.md)

# Headlamp

<https://github.com/headlamp-k8s/headlamp>
<https://github.com/headlamp-k8s/plugins>
<https://github.com/kubernetes-sigs/headlamp>

---

## The problem it solves

A general-purpose cluster UI that is actually maintained: browse and edit every resource type
including CRDs, read logs, exec into containers, and extend it with plugins. It runs either as a
desktop application against your kubeconfig or in-cluster behind an Ingress, and it supports OIDC so
users can sign in as themselves.

It has moved under `kubernetes-sigs`, which is the strongest availability signal of any tool in this
folder — a CNCF-sandbox dashboard with SIG ownership rather than a single maintainer.

## When to use it

- The default choice for a general cluster UI, especially where OIDC is available
- CRD-heavy clusters — it renders custom resources properly instead of hiding them
- A desktop client for engineers who want a UI without exposing anything in-cluster
- Where a plugin can add the one view your platform actually needs

## When not to use it

- **Per-namespace access for teams** — see the note below; this does not work the way you expect
- A read-only status page for non-engineers; it is an editor, and the object model is on display
- When port-forwarding is enough; running it in-cluster adds an auth surface for no gain
- Logs across many pods at once — [Kubetail](../kubetail/README.md) is built for that

## Notes

**Chart** `headlamp` version `0.32.1` from `https://kubernetes-sigs.github.io/headlamp/`.

**Getting the admin token:**

```sh
kubectl -n headlamp get secret headlamp-admin-token -o jsonpath='{.data.token}' | base64 -d
```

This is the static-token login path — one Secret, one identity, no expiry. Fine for a local cluster;
on anything shared it means every user is the same user and the audit log says so.

### The recorded verdict

Translated from the original note: *"nice, but look at this rubbish — restricting by namespace is
awful, it only works with `ClusterRole` and `ClusterRoleBinding`."*

- <https://github.com/headlamp-k8s/headlamp/issues/2385>

This is the most useful finding in the folder, and it generalises. The natural requirement is "team A
sees namespace A". Headlamp needs cluster-scoped read to build its navigation — the namespace list,
the resource types, the CRDs — so granting it anything less produces a UI that cannot render. The
practical outcome is that a working setup requires `ClusterRole` and `ClusterRoleBinding`, which is
precisely the cluster-wide grant you were trying to avoid.

Test this before promising namespace scoping to anyone. It is not a Headlamp-specific flaw so much as
a consequence of how cluster UIs are built, but Headlamp is where it was hit and written down.

**OIDC on AKS** — <https://github.com/kubernetes-sigs/headlamp/issues/2480>. Recorded separately, and
the issue number being under `kubernetes-sigs` while the first is under `headlamp-k8s` is itself the
marker of the project's move between organisations. Both links resolve; both are worth reading before
wiring Headlamp to Entra ID.

**Plugins** live in a separate repository, <https://github.com/headlamp-k8s/plugins>. They are the
route to making it useful for a specific platform — a Flux view, a cost view — and they are also a
build step you now own.

---

[← Dashboards](../README.md)
