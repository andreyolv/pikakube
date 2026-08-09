[← Pod security](../README.md)

# securityContext

<https://kubernetes.io/docs/tasks/configure-pod-container/security-context/>

Context and comparison against the other tools: [../README.md](../README.md)

---

## The problem it solves

`securityContext` is the block on a pod and on each container that decides **who the process
runs as and what it is allowed to do**. It is the most basic confinement in Kubernetes, it
is built in, it needs no operator and no CRD, and it is the thing the scanners in
`manifest-scan/` and the standards in `pod-security/` are all ultimately checking for.

By default a container runs as **root inside its namespace** with a broad set of Linux
capabilities and a writable filesystem. `securityContext` is where you take that away. The
fields that actually matter:

| Field | Set it to | Why |
|---|---|---|
| `runAsNonRoot: true` | `true` | refuses to start a container whose image runs as UID 0 — the single highest-value line |
| `runAsUser` / `runAsGroup` | a high, non-zero UID/GID | run as an unprivileged identity |
| `allowPrivilegeEscalation: false` | `false` | blocks `setuid`/`setgid` binaries from gaining more than the process started with |
| `readOnlyRootFilesystem: true` | `true` | the container cannot write to its own image; forces writable state into explicit volumes |
| `capabilities.drop: ["ALL"]` | drop `ALL` | start from zero Linux capabilities and add back only what is genuinely needed |
| `privileged` | never `true` | `privileged: true` is a full escape hatch — it is effectively root on the node |
| `seccompProfile` | `RuntimeDefault` | see [seccomp](../seccomp/README.md) |

Two levels exist and their interaction is the usual source of confusion: a **pod-level**
`securityContext` sets defaults (and `fsGroup`, which is pod-only), and a **container-level**
`securityContext` overrides it for that container. The container level wins.

## When to use it

- **Always.** Every workload should set at minimum `runAsNonRoot`, `allowPrivilegeEscalation: false`, drop `ALL` capabilities, and a seccomp profile. This is the baseline, not the hardened tier
- As the concrete target that Pod Security Standards `restricted` and your admission policies (`policies/`) enforce — the standards are, in effect, "these fields, set correctly"
- When a container genuinely needs one capability (say `NET_BIND_SERVICE` to bind port 80), add exactly that one back after dropping `ALL`

## When not to use it

- There is no "not to use it" — the question is only how strict. The escape hatches (`privileged`, `hostPID`, added `SYS_ADMIN`) are what to avoid, not the block itself
- Do not rely on `runAsUser` alone. Setting a non-zero UID without `runAsNonRoot: true` still lets an image that hardcodes `USER 0` win. Set both
- Do not treat it as a boundary against a determined attacker on its own. It is one layer; seccomp, AppArmor and NetworkPolicy are the others. A kernel bug can defeat any single one

## Notes

This folder had no `doc.md` — only example pods. They form a deliberate teaching sequence,
straight from the Kubernetes documentation, and each one demonstrates a specific behaviour:

- [`pod1.yaml`](pod1.yaml) (`security-context-demo`) — a **pod-level** context with
  `runAsUser: 1000`, `runAsGroup: 3000`, `fsGroup: 2000`, plus a container that sets
  `allowPrivilegeEscalation: false`. `fsGroup` is the interesting field: it makes the
  mounted `emptyDir` volume group-owned by GID 2000, so a non-root process can write to it.
  This is how you give an unprivileged container a writable volume.
- [`pod2.yaml`](pod2.yaml) (`security-context-demo-2`) — pod sets `runAsUser: 1000`, the
  container **overrides** it with `runAsUser: 2000`. Demonstrates the precedence rule: the
  container-level value wins, and the process runs as 2000.
- [`pod3.yaml`](pod3.yaml) (`security-context-demo-3`) — no `securityContext` at all. The
  "before" case: this is what an unhardened workload looks like, and what every scanner in
  `manifest-scan/` flags.
- [`pod4.yaml`](pod4.yaml) (`security-context-demo-4`) — **adds** capabilities
  (`NET_ADMIN`, `SYS_TIME`). The counter-example: it shows the mechanism for granting a
  capability, and `SYS_TIME` (setting the system clock) is exactly the kind of broad grant
  you should be suspicious of in review. Instructive as the thing *not* to do casually.

Read them in that order — unconfigured (pod3), then identity (pod1/pod2), then the
capability escape hatch (pod4) — and the whole field set makes sense.

Do not modify these files; they are reference examples.

---

[← Pod security](../README.md)
