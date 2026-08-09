[← Manifest scan](../README.md)

# kubesec

<https://github.com/controlplaneio/kubesec>

Context and comparison against the other tools: [../README.md](../README.md)

---

## The problem it solves

kubesec takes a single Kubernetes manifest and returns a **security score** — a number,
plus a list of what raised it and what lowered it. It is the narrowest and most opinionated
tool in this folder, and that is the point: it does one thing, scoring the `securityContext`
and a handful of adjacent fields, and it needs no configuration to be useful.

Its opinions map almost exactly onto the fields that matter in
[`../../pod-security/security-context/README.md`](../../pod-security/security-context/README.md):

| Raises the score (good) | Lowers the score (bad) |
|---|---|
| `runAsNonRoot: true` | `privileged: true` |
| `readOnlyRootFilesystem: true` | `hostNetwork`, `hostPID`, `hostIPC` |
| `runAsUser > 10000` | `allowPrivilegeEscalation: true` |
| dropping capabilities | adding capabilities like `SYS_ADMIN` |
| a seccomp profile set | mounting sensitive host paths |
| resource limits set | `capabilities.add` with dangerous entries |

The output is a scalar, which makes it the easy one to gate on in CI: fail the build below
a threshold. That simplicity is also its ceiling — see below.

## When to use it

- A **fast, zero-config gate** in CI on a workload manifest: "is this pod configured like something that belongs in production?"
- Teaching or reviewing `securityContext` — the score makes the effect of each field legible
- A quick score of a manifest before it ever reaches the cluster, via the CLI or the hosted API
- Alongside kube-linter and checkov, not instead of them — it scores the pod's own hardening; they check different things

## When not to use it

- **As your only manifest check.** It scores pod security posture and little else. It will not catch a missing liveness probe, a `latest` tag, or a broken label selector — that is [kube-linter](../kube-linter/README.md)'s job
- As a substitute for admission control. A high kubesec score in CI means nothing to anything that bypasses CI. Enforcement in the cluster is `policies/` (Kyverno, Gatekeeper). See the parent README on why this distinction is load-bearing
- On non-workload resources. A score on a `ConfigMap` or a `Service` is meaningless — it is built around the pod spec
- Trusting the hosted API with sensitive manifests. `kubesec.io` offers a public scanning endpoint; for anything real, run the container or binary locally so manifests never leave your control

## Notes

The original note in this folder was the project link and nothing else:

- <https://github.com/controlplaneio/kubesec> — the upstream repository, from ControlPlane.

Points worth recording alongside it:

- **It runs three ways:** a CLI/container (`kubesec scan pod.yaml`), a self-hostable HTTP
  server, and the public API at `kubesec.io`. For CI, the container is the sane default —
  no network dependency and nothing leaves the build.
- **The score is relative, not absolute.** A positive score is not a certificate of safety;
  it means "more of the good fields are set than the bad ones". Treat the threshold as a
  floor to clear, not a finish line.
- **Scope is deliberately small.** kubesec is the specialist. Where kube-linter is breadth
  across production-readiness and checkov is breadth across all of IaC, kubesec is depth on
  exactly one axis: how hardened is this pod. That is why it earns a place next to the
  other two rather than being replaced by them.

---

[← Manifest scan](../README.md)
