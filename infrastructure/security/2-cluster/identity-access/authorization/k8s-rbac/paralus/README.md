[← Kubernetes RBAC](../README.md)

# Paralus

<https://github.com/paralus/paralus>
<https://github.com/paralus/helm-charts>

---

## The problem it solves

**"Nobody manages who gets in."**

RBAC decides what a subject may do. It says nothing about how a human *becomes* a subject —
because, as established in [`identity-access/README.md`](../../../README.md), **Kubernetes has no
users**. In practice that gap is filled by someone hand-editing kubeconfigs, mailing certificates,
and hoping the spreadsheet of who has access to which cluster is current.

Paralus is a **zero-trust access-management platform** for that gap. It sits between people and
clusters and provides:

| Capability | Detail |
|---|---|
| **SSO login** | OIDC against an existing identity provider, or local users |
| **Kubeconfig distribution** | users obtain a kubeconfig themselves, from a UI or CLI, with a **short-lived, per-user credential** |
| **A UI and a CLI (`pctl`)** | self-service access, and administration without editing YAML |
| **Cross-cluster access control** | one policy plane for many clusters, which is where RBAC alone stops helping |
| **Audit** | who accessed which cluster, when, and what they did — attributable to a person |
| **Groups and project scoping** | permissions expressed against groups and projects, then projected into cluster RBAC |

The property that makes it a security improvement rather than a convenience is the credential
model. Instead of a permanent kubeconfig with a client certificate — which, per
[`privileged-access/`](../../../authentication/privileged-access/README.md), **Kubernetes cannot
revoke** — each user gets a short-lived credential tied to their identity. Offboarding is
removing them in Paralus, not a hunt across clusters.

The chart is named `ztka` — Zero Trust Kubectl Access — which describes the product more
precisely than the project name does.

## When to use it

- **Several clusters and many users.** This is the case it is built for. One cluster with three
  engineers does not need a platform; ten clusters with fifty engineers has no good manual answer.
- **Self-service access is a requirement.** Users obtaining their own kubeconfig, scoped and
  expiring, removes a recurring administrative task and a recurring source of over-granting.
- **Attribution is required.** Every kubectl session tied to a named person, with an audit trail,
  rather than a shared certificate.
- **You want a UI.** Some organisations genuinely need a non-YAML interface for access
  management, and refusing to provide one means access is managed in tickets instead.
- **Open-source, self-hosted, and no per-seat cost.** This is Paralus's clearest advantage over
  the commercial platforms in the same space.

## When not to use it

- **One cluster, few users.** [Dex](../../../authentication/federation/dex/README.md) plus
  RoleBindings on groups is the whole answer, and it is two orders of magnitude less to operate.
- **You already run Teleport.** Overlapping scope, and
  [Teleport](../../../authentication/privileged-access/teleport/README.md) goes considerably
  deeper — session recording, per-session Kubernetes audit, and coverage of SSH and databases as
  well. Running both means two access planes.
- **You want RBAC analysis.** Paralus manages *access*, not permission hygiene. For risk use
  [kubiscan](../kubiscan/README.md); for minimality [audit2rbac](../audit2rbac/README.md).
- **You cannot make it highly available.** It becomes the front door to every cluster; when it is
  down, nobody gets a kubeconfig. It needs its own availability plan and a break-glass path —
  the same warning as every broker in
  [`privileged-access/`](../../../authentication/privileged-access/README.md).
- **Project activity matters to you.** Paralus is a CNCF sandbox project with a smaller community
  than the alternatives. Check its current state before making it the only path to production
  clusters.

## Notes

**`https://github.com/paralus/paralus`** — the project. Go, Apache-2.0, CNCF sandbox, originally
from Rafay Systems.

**`https://github.com/paralus/helm-charts`** — the chart repository. The chart is named **`ztka`**,
not `paralus`, which is worth knowing because searching for a `paralus` chart finds nothing.

The recorded notes were the first-login procedure, preserved and explained:

**`login`** / **`admin@paralus.local`** — the default administrative account created during
bootstrap. Note that it is a **local** account, not an SSO identity: Paralus bootstraps with one
local admin so that the OIDC integration can be configured from inside. It should be disabled or
tightly restricted once SSO works, since it is a standing credential that bypasses the identity
provider.

**The password-retrieval command:**

```bash
kubectl logs -f --namespace paralus \
  $(kubectl get pods --namespace paralus -l app.kubernetes.io/name='paralus' \
    -o jsonpath='{ .items[0].metadata.name }') initialize \
  | grep 'Org Admin default password:'
```

What it does, piece by piece:

- the inner `kubectl get pods` finds the Paralus pod by its `app.kubernetes.io/name` label and
  extracts the first result's name with a JSONPath expression
- `initialize` is the **init container** name — the logs are read from that container
  specifically, not from the main one
- `grep` pulls out the generated organisation-admin password, which Paralus prints exactly once
  during bootstrap

Two consequences of that design worth recording. The password **only exists in a log line**, so
it must be captured at first boot and stored properly; and it is *in a log*, which means anyone
with read access to pod logs in that namespace can read the platform's admin password until the
logs rotate. Change it immediately after first login, and do not treat the log as storage.

What is staged: a `HelmRepository`, a `Namespace` `paralus`, and a `HelmRelease` for the `ztka`
chart at version `0.2.7`:

| Setting | What it means |
|---|---|
| `deploy.postgresql.enable: true` | the bundled Postgres subchart. Paralus needs a database; the commented-out `address`, `username`, `password` and `database` fields directly beneath show the alternative — pointing at an external one, which is what the platform's CloudNativePG would provide |
| `deploy.fluentbit.enable: false` | audit-log shipping via Fluent Bit is **disabled**. Worth flagging: Paralus's audit trail is a large part of its value, and turning off the shipping component means those records stay local. For a lab that is fine; for the use case that justifies deploying Paralus at all, it is not |
| `deploy.kratos.kratos.development: true` | Ory **Kratos** is Paralus's identity component — the same Kratos referenced in [Hydra](../../../authentication/oauth-oidc-server/hydra/README.md)'s notes as the user-management half of the Ory stack. `development: true` relaxes security settings and is not a production configuration |

The Kratos dependency is a nice illustration of the pattern in
[`oauth-oidc-server/`](../../../authentication/oauth-oidc-server/README.md): Paralus did not build
its own identity system, it embedded the specialist one.

For this platform, the conclusion in [`../README.md`](../README.md) applies: one cluster, one
operator, and no access-management problem to solve. Paralus is catalogued for a multi-cluster,
multi-user future, and deploying it now would add a front door to a house with one occupant.

---

[← Kubernetes RBAC](../README.md)
