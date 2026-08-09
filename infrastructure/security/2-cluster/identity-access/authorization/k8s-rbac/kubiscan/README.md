[← Kubernetes RBAC](../README.md)

# KubiScan

<https://github.com/cyberark/KubiScan>

---

## The problem it solves

**"Nobody can see the risk."**

RBAC risk is not visible in any single manifest. It is a property of the **union** of everything
granted, and it accumulates: every operator installed by Helm brings ClusterRoles nobody read,
every "temporary" binding stays, and every wildcard silently expands when a new CRD appears.

KubiScan scans a live cluster and reports what that union actually permits, focusing on the
escalation primitives enumerated in [`../README.md`](../README.md) §2:

| It finds | Why it matters |
|---|---|
| **Risky roles, RoleBindings and ClusterRoleBindings** | roles granting `escalate`, `bind`, `impersonate`, wildcard verbs, Secret access, `pods/exec`, and the rest of the list |
| **Risky subjects** | which users, groups and ServiceAccounts hold them, via the full binding graph |
| **Risky pods and containers** | pods running with a ServiceAccount whose token would be valuable if the pod were compromised |
| **ServiceAccount tokens inside pods** | it can extract and decode them, showing exactly what a compromised container would hold |
| **Privileged containers** | the ones that make a node escape possible, which then makes every Secret on that node readable |
| **Subjects that can escalate to cluster-admin** | the traversal that connects a small permission to a full compromise |

The last row is the one that distinguishes it from a linter. Reading manifests tells you what
each grants. KubiScan follows the graph: this ServiceAccount can create pods, so it can mount
this other ServiceAccount's token, which has `bind`, which reaches `cluster-admin`. **That path
is invisible in every individual object on it.**

It comes from CyberArk's research team, and the risk model it encodes is essentially the
attacker's view — "given a foothold here, what can I reach?" — rather than a compliance
checklist. That is the more useful framing for RBAC specifically.

## When to use it

- **Auditing a cluster you did not build.** The highest-value case. It answers "what does this
  cluster currently permit?" in one run.
- **After installing operators.** Charts routinely request cluster-wide Secret access and wildcard
  verbs. Scan after every significant addition.
- **Periodically, as hygiene.** Permissions only ever accumulate; a scheduled scan is how the
  accumulation stays visible.
- **Incident response.** "This ServiceAccount was compromised — what could it reach?" is exactly
  the question KubiScan traverses.
- **Before a security review**, so you find what the reviewer would find.
- **Learning.** Running it against a real cluster is the fastest way to understand why the
  escalation primitives matter — you see them in bindings you installed yourself.

## When not to use it

- **As enforcement.** It is a scanner. It reports, it does not block, and it does not reconcile.
  Preventing risky RBAC from being created is an admission policy engine's job.
- **As the only check.** Its risk model is a set of rules; it will not know that your specific
  Role over your specific CRD is dangerous in your specific context.
- **To generate correct permissions.** Opposite direction — that is
  [audit2rbac](../audit2rbac/README.md). The two pair naturally: KubiScan finds the over-grant,
  audit2rbac produces the replacement.
- **Expecting zero findings on a real cluster.** Kubernetes' own built-in ClusterRoles and every
  serious operator will appear. The output needs triage, not blind remediation — removing a
  legitimately required permission breaks the cluster.
- **In an environment where you cannot grant it read access.** It needs broad read permissions to
  see all roles and bindings, which is itself a privileged position. Run it with a dedicated,
  read-only, short-lived identity rather than a permanent one.

## Notes

**`https://github.com/cyberark/KubiScan`** — the project, and the only note recorded for this
folder. Python, from CyberArk Labs.

**No manifests are staged here**, and that is correct — KubiScan is a **read-only CLI**. It can
run from a container, or locally against a kubeconfig, and it installs nothing into the cluster.
That makes it one of the two things in this entire `identity-access/` tree that can be tried
immediately at zero risk, the other being [audit2rbac](../audit2rbac/README.md).

The subcommands worth knowing, since the tool's value is in knowing what to ask:

| Command | Question it answers |
|---|---|
| `kubiscan -rr` | which **risky roles** exist |
| `kubiscan -rs` | which **subjects** hold them |
| `kubiscan -rp` | which **pods** run with risky ServiceAccounts |
| `kubiscan -aa` | **all** of the above |
| `kubiscan -ptp` | which **pods can escalate to cluster-admin** — the traversal, and the most alarming output |
| `kubiscan -dsat` | **dump ServiceAccount tokens** from pods, showing what a compromised container holds |

Two operational notes:

- **The permissions it needs are themselves privileged.** Reading every Role, ClusterRole and
  binding cluster-wide is a meaningful grant. Use a dedicated read-only identity, and remove it
  afterwards — an audit tool that leaves behind a permanent broad-read ServiceAccount has made
  the problem slightly worse.
- **Triage the output against intent.** Kubernetes ships `cluster-admin`, and controllers
  legitimately need broad access. The finding that matters is a *workload* holding a permission
  its function does not require — an application ServiceAccount that can read Secrets
  cluster-wide, not the kube-controller-manager doing so.

For this platform, the recommendation in [`../README.md`](../README.md) applies directly: this is
the first thing to run. Every operator installed by Flux in this repository brought ClusterRoles
that nobody has read, and a single read-only run will say what they collectively permit.

---

[← Kubernetes RBAC](../README.md)
