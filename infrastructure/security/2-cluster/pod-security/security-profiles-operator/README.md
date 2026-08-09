[← Pod security](../README.md)

# security-profiles-operator

<https://github.com/kubernetes-sigs/security-profiles-operator>
<https://github.com/kubernetes-sigs/security-profiles-operator/tree/main/examples>

Context and comparison against the other tools: [../README.md](../README.md)

---

## The problem it solves

Both [seccomp](../seccomp/README.md) and [AppArmor](../apparmor/README.md) run into the same
wall: a tight profile is enormously valuable, and **nobody can write one by hand.** You do
not know which of 350 syscalls your app makes, or every file path it touches, and guessing
means either a crash you cannot debug or a profile so loose it is pointless. On top of that,
getting a profile onto every node — and keeping it there — is manual, node-level work that
does not belong in a GitOps model.

The Security Profiles Operator (SPO), a Kubernetes SIG project, fixes both problems:

**1. It manages profiles as Kubernetes resources.** Instead of dropping JSON files onto
nodes by hand, you create a `SeccompProfile` or `AppArmorProfile` custom resource, and the
operator distributes it to the nodes and makes it available to pods. Profiles become
first-class cluster objects — versioned, reviewed and reconciled like everything else.

**2. It *records* profiles from a running workload.** This is the feature that matters. You
put a workload into recording mode (via a `ProfileRecording` resource, backed by eBPF or the
audit log), exercise it under real traffic, and SPO writes out the exact seccomp or AppArmor
profile of what it actually did. The answer to "nobody can write a seccomp profile by hand"
is: **you do not write it, you record it** — then review the recording, tighten it, and
promote it to an enforced profile.

Its resources, roughly:

| Resource | What it does |
|---|---|
| `SeccompProfile` | a seccomp profile as a cluster object, distributed to nodes |
| `AppArmorProfile` | the same for AppArmor |
| `ProfileRecording` | record what a selected workload actually does, and emit a profile from it |
| `ProfileBinding` | bind a profile to workloads by image, so it is applied automatically |

## When to use it

- You want tight seccomp/AppArmor profiles but have no realistic way to author them — record from the running workload instead
- You are managing profiles across more than a handful of nodes and want them reconciled declaratively rather than copied by hand
- GitOps-managed clusters where "a file on a node" is an anti-pattern and everything should be a reconciled resource
- You want profiles bound to workloads automatically by image reference, rather than annotated pod by pod

## When not to use it

- If `RuntimeDefault` seccomp is enough for your threat model — and for many workloads it is. SPO is for when you want the *tight* profiles, and that is extra machinery to run
- On a cluster too small to justify the operator. One or two workloads needing a custom profile can be handled with a `Localhost` profile and a node-provisioning step; SPO earns its place at scale
- Expecting it to replace `securityContext` or Pod Security Standards. It produces and distributes seccomp/AppArmor profiles; it does not set `runAsNonRoot` or enforce the standards. Different layer
- Recording in production without care. Recording mode observes real syscalls/file access; scope the `ProfileRecording` tightly and treat the output as a draft to review, not a profile to trust blindly

## Notes

The original `doc.md` held two links:

- <https://github.com/kubernetes-sigs/security-profiles-operator> — the upstream operator,
  a Kubernetes SIG project.
- <https://github.com/kubernetes-sigs/security-profiles-operator/tree/main/examples> — the
  upstream examples directory, the reference for `SeccompProfile`, `ProfileRecording` and
  `ProfileBinding` manifests.

This folder installs SPO through Flux (GitOps), which is itself the point — profiles managed
as reconciled resources rather than node files:

- [`namespace.yaml`](namespace.yaml) — the `security-profiles-operator` namespace.
- [`helm/gitrepository.yaml`](helm/gitrepository.yaml) — a Flux `GitRepository` pointing at
  the upstream repo, pinned to tag **`v0.8.4`**, with an `ignore` rule that includes only
  the `deploy/helm` directory. Pin the version deliberately; do not float it.
- [`helm/helmrelease.yaml`](helm/helmrelease.yaml) — a Flux `HelmRelease` installing the
  chart from `deploy/helm/` in that GitRepository, with `replicaCount: 1`. The values
  comment points at the upstream
  [`values.yaml`](https://github.com/kubernetes-sigs/security-profiles-operator/blob/main/deploy/helm/values.yaml)
  as the reference for what else can be configured.

The recording workflow ties this folder together: the profiles hand-written in
[seccomp](../seccomp/README.md) show what a profile *is*; SPO is how you generate one without
writing it, then manage it across the cluster. That is the intended reading order —
understand the format first, then let the operator produce it.

Do not modify these files; they are the reference installation manifests.

---

[← Pod security](../README.md)
