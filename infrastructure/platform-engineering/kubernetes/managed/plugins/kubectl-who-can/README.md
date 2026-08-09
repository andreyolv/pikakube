[← Plugins](../README.md)

# kubectl-who-can

<https://github.com/aquasecurity/kubectl-who-can>

---

## The problem it solves

RBAC answers the question "may **this** subject do **this** thing" — that is what
`kubectl auth can-i` asks. The reverse question is the one you actually have during a review or an
incident: **who can do this thing?**

Kubernetes has no API for that. Answering it by hand means enumerating every Role, ClusterRole,
RoleBinding and ClusterRoleBinding and working out which combinations grant the verb on the resource.
`kubectl who-can delete pods -n production` does the enumeration for you.

## When to use it

- Security review: who can read Secrets, delete namespaces, create ClusterRoleBindings
- Incident investigation: who could have done this
- Verifying that a permissions change had the effect intended, and only that effect
- Auditing a cluster you have inherited

## When not to use it

- As a complete authorisation model — it reads RBAC and nothing else
- Where authorisation is partly enforced by admission webhooks or an external policy engine
- As a substitute for audit logs; it tells you who **can**, not who **did**
- Without checking the project's current maintenance status before depending on it

## Notes

Recorded as a link only.

**Its limits are the thing to be precise about**, because a security tool that is trusted beyond its
scope is worse than none:

- **It reads RBAC.** Admission webhooks — [Capsule](../../multi-tenancy/capsule/README.md), Kyverno,
  Gatekeeper — can reject requests RBAC would allow. `who-can` does not model them, so its answer is
  an upper bound on who is permitted, not the effective set.
- **Impersonation is a separate path.** A subject with the `impersonate` verb can act as anyone else.
  That is itself a permission worth running `who-can impersonate users` against, and it is the first
  query to run on an unfamiliar cluster.
- **Group membership comes from outside the cluster.** Bindings reference groups; who is in a group is
  decided by the identity provider. `who-can` reports the binding; it cannot expand the group.

**The queries worth running on any cluster you are responsible for:**

```sh
kubectl who-can get secrets --all-namespaces
kubectl who-can create clusterrolebindings
kubectl who-can impersonate users
kubectl who-can '*' '*'
```

The last one is the "who is effectively cluster-admin" question, and the answer is usually longer
than expected — because ServiceAccounts belonging to installed operators appear in it, and every one
of those is a controller whose compromise is a cluster compromise. That connects directly to the RBAC
discipline argued for in [`core/python-client/`](../../core/python-client/README.md).

Aqua Security maintain it; check the repository's activity before making it part of a routine.

---

[← Plugins](../README.md)
