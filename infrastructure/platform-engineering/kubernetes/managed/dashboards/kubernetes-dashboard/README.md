[← Dashboards](../README.md)

# Kubernetes Dashboard

<https://github.com/kubernetes/dashboard>
<https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md>

---

## The problem it solves

The official web UI. Browse workloads, services, config and storage; view logs; exec into
containers; edit YAML in place. It is the reference implementation, it lives under the `kubernetes`
organisation, and it will not be abandoned.

Since version 7 it is distributed as a multi-component Helm chart — API, web, metrics scraper and a
gateway — rather than the single deployment it used to be. That change is worth knowing about,
because most tutorials still describe the old shape.

## When to use it

- You want the official, guaranteed-maintained option and nothing more
- A familiar interface that new team members have probably seen before
- Token-based access is acceptable, or you have OIDC in front of it

## When not to use it

- **Local clusters over plain HTTP** — see the recorded issue below
- CRD-heavy work; [Headlamp](../headlamp/README.md) handles custom resources far better
- When you want a lightweight single container — version 7 is several components
- Anywhere it would be exposed without real authentication; this dashboard's history of being left
  open is the reason it has a reputation

## Notes

**Chart** `kubernetes-dashboard` version `7.7.0` from `https://kubernetes.github.io/dashboard/`.
Deployed with `namespace.yaml`, `rbac.yaml` and `secret.yaml` alongside — the sample admin user,
created manually.

**Getting the token**, following the upstream sample-user documentation
(<https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md>):

```sh
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d
```

The `secret.yaml` in this folder exists because of a change in Kubernetes 1.24: ServiceAccounts no
longer get a permanent token Secret automatically. To keep a long-lived token you must create the
Secret explicitly with the `kubernetes.io/service-account-token` type. That is a deliberate
long-lived credential, and the modern alternative is `kubectl create token admin-user`, which expires.

**The recorded verdict:** *"rubbish for localhost"* —
<https://github.com/kubernetes/dashboard/issues/8829>.

The substance behind it: version 7 puts a gateway in front of the components and the login flow
depends on secure-context and cookie behaviour that assumes HTTPS. Accessed over plain HTTP on
`localhost` — the normal way anyone tries it first, via `kubectl port-forward` — the login does not
work properly. The fix is TLS, which for a local cluster means generating a certificate to look at a
dashboard, and the irritation in the note is proportionate.

It is a good illustration of why this folder ended up with eleven tools: the official one is the
hardest to run casually, and every alternative here starts by being easier.

---

[← Dashboards](../README.md)
