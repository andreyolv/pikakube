[← Pod security](../README.md)

# seccomp

<https://kubernetes.io/docs/tutorials/security/seccomp/>

Context and comparison against the other tools: [../README.md](../README.md)

---

## The problem it solves

`securityContext` controls *who* the process is and *what capabilities* it holds. seccomp
controls something lower down: **which of the ~350 Linux syscalls the process is even
allowed to make.** A container almost never needs all of them. seccomp (secure computing
mode) installs a filter in the kernel so that a syscall the workload does not use — and that
an exploit *would* use to escalate — is refused before it runs.

This is defence against the class of attack that `securityContext` cannot see: a compromised
process making a syscall like `keyctl`, `ptrace` or a raw mount to break out. If the filter
does not permit that syscall, the escape fails at the kernel boundary.

A seccomp profile is a JSON document with a default action and a list of exceptions:

| `defaultAction` | Meaning |
|---|---|
| `SCMP_ACT_ERRNO` | deny by default — every syscall fails unless explicitly allowed. The secure posture |
| `SCMP_ACT_ALLOW` | allow by default — used inside an `allow`-list block for the permitted syscalls |
| `SCMP_ACT_LOG` | allow everything but **log** each syscall — the way you discover what a workload actually needs |

In Kubernetes you attach one via `securityContext.seccompProfile`:

| `type` | Meaning |
|---|---|
| `RuntimeDefault` | use the container runtime's built-in profile — a sane blocklist that stops dangerous syscalls with near-zero effort. **This is what almost everything should set** |
| `Localhost` | use a custom profile file from the node's seccomp directory (`localhostProfile: <path>`) — for when you want a tight allow-list |
| `Unconfined` | no filtering — the insecure default that `RuntimeDefault` should replace |

The honest problem with the tight end of this: **nobody writes a syscall allow-list by
hand.** You do not know which of 350 syscalls your app needs. That is exactly what
[security-profiles-operator](../security-profiles-operator/README.md) exists to solve — it
records the profile from a running workload.

## When to use it

- **`RuntimeDefault` on every workload, always.** It is one line, it costs effectively nothing, and it closes off the dangerous syscalls. There is no good reason not to
- A `Localhost` custom profile for high-value or exposed workloads where you want to allow only the syscalls the app genuinely makes
- The `SCMP_ACT_LOG` profile as a discovery step: run the workload against it, watch which syscalls it makes, then build the tight profile from that data

## When not to use it

- Do not leave workloads `Unconfined` — that is the absence of the control, not a choice
- Do not hand-author a tight allow-list from guesswork. You will either block a syscall the app needs (it crashes in a way that is miserable to debug) or allow too much (pointless). Record it instead — see security-profiles-operator
- Do not treat it as a substitute for `securityContext`. They operate at different layers: capabilities and identity above, syscalls below. You want both
- A tight profile is version-fragile: a library update can start making a new syscall and the pod breaks. Budget for maintaining custom profiles, or stick to `RuntimeDefault`

## Notes

The original `doc.md` held a single link:

- <https://kubernetes.io/docs/tutorials/security/seccomp/> — the official seccomp tutorial,
  which is exactly the tutorial the files in this folder implement.

This folder ships the tutorial's full worked set. The **profiles** (in `profiles/`) are the
three `defaultAction` modes made concrete:

- [`profiles/violation.json`](profiles/violation.json) — `defaultAction: SCMP_ACT_ERRNO`
  and **no exceptions**: every syscall is denied, so a container using it cannot even start
  properly. The deliberate "too strict, breaks everything" case.
- [`profiles/audit.json`](profiles/audit.json) — `defaultAction: SCMP_ACT_LOG`: allow
  everything but log it. This is the **discovery** profile — run a workload under it and the
  node's audit log tells you every syscall the workload made.
- [`profiles/fine-grained.json`](profiles/fine-grained.json) — `defaultAction:
  SCMP_ACT_ERRNO` with an explicit `SCMP_ACT_ALLOW` list of ~50 syscalls: deny by default,
  permit exactly what this specific `http-echo` workload needs. The "correct" end state,
  and a good illustration of how long even a minimal allow-list is — which is the argument
  for recording profiles rather than writing them.

The **example pods** (in `examples/`) each attach one of the above:

- [`examples/default-pod.yaml`](examples/default-pod.yaml) — `type: RuntimeDefault`. The
  one-line, do-this-everywhere case.
- [`examples/audito-pod.yaml`](examples/audito-pod.yaml) — `type: Localhost`,
  `localhostProfile: profiles/audit.json`. (Filename is misspelled upstream; left as-is.)
- [`examples/fine-pod.yaml`](examples/fine-pod.yaml) — `type: Localhost`, the fine-grained
  allow-list.
- [`examples/violation-pod.yaml`](examples/violation-pod.yaml) — `type: Localhost`, the
  deny-all profile; the pod fails, on purpose, to show what an over-tight profile does.

All of them also set `allowPrivilegeEscalation: false`, tying back to
[security-context](../security-context/README.md).

Do not modify these files; they are the reference examples for the tutorial.

---

[← Pod security](../README.md)
