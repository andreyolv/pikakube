[← Certifications](../README.md)

# CKS

<https://github.com/ramanagali/Interview_Guide/blob/main/CKS_Preparation_Guide.md>
<https://github.com/zealvora/certified-kubernetes-security-specialist>
<https://github.com/bmuschko/cks-crash-course>
<https://github.com/killer-sh/cks-course-environment>
<https://github.com/moabukar/CKS-Exercises-Certified-Kubernetes-Security-Specialist>
<https://github.com/ViktorUJ/cks/tree/master/tasks/cks/mock/01>
<https://github.com/snigdhasambitak/cks>

---

## The problem it solves

Certified Kubernetes Security Specialist is the security exam, and it has a hard prerequisite: **CKA
must be passed first**. Where CKA asks whether you can run a cluster, CKS asks what an attacker would
do with it and whether you would notice.

The domains it covers map directly onto folders elsewhere in this repository — admission control,
runtime sandboxing, image scanning and supply chain, network policy, audit logging, and minimising
the host and the container.

## When to use it

- You already hold CKA and secure clusters as part of the job
- Admission control and runtime security are decisions you make rather than inherit
- You want a structured reason to actually read the audit-logging and seccomp documentation

## When not to use it

- Without CKA — it is a formal prerequisite
- As a substitute for a security programme; a certification is one person's knowledge, not a control
- If your clusters are managed and hardened by someone else, and will stay that way

## Notes

The recorded material is a **collection of preparation resources with no commentary** — seven
repositories and five videos. That shape is worth reading honestly: this is a gathered reading list,
not notes from work done. Compare it with [`cka/`](../cka/README.md), which is eight files of worked
commands.

The repositories, and what each kind is for:

- **`ramanagali/Interview_Guide` (CKS preparation guide)** — a written syllabus walkthrough; the
  orientation document
- **`zealvora/...`, `snigdhasambitak/cks`** — course companion material
- **`bmuschko/cks-crash-course`** — Benjamin Muschko's crash course, the companion to a well-known
  book on the exam
- **`killer-sh/cks-course-environment`** — the environment from killer.sh, which is also the vendor
  behind the exam simulator candidates get with the registration. The closest thing to the real
  interface
- **`moabukar/CKS-Exercises-...`, `ViktorUJ/cks` mock tasks** — exercise sets and mock tasks; the
  practice half

Video material recorded alongside them:

- <https://www.youtube.com/watch?v=GgWUkw-q9sw&list=PLpbwBK0ptssx38770vYNwZEuCeGNw54CH&index=8> — part of a playlist
- <https://www.youtube.com/watch?v=KF72ZoyVN-0&t=983s>
- <https://www.youtube.com/watch?v=MC9BizUnIs8&t=1152s>
- <https://www.youtube.com/watch?v=e7TIMDdzmY8>
- <https://www.youtube.com/watch?v=7eH7vfT0axA>

**Where the exam's subject matter already lives in this repository**, which is the practical way to
prepare without a course:

| CKS domain | Here |
|---|---|
| Runtime sandboxing — gVisor, Kata | [`on-premise/container-runtime-sandbox/`](../../../../on-premise/container-runtime-sandbox/README.md) |
| Container runtimes and `RuntimeClass` | [`on-premise/container-runtime-interface/`](../../../../on-premise/container-runtime-interface/README.md) |
| RBAC and least privilege | [`core/cluster-permissions/`](../../cluster-permissions/README.md) |
| Pod Security Admission | referenced in [`core/`](../../README.md) |
| Multi-tenancy boundaries | [`multi-tenancy/`](../../../multi-tenancy/README.md) |

The one thing the exam covers that this discipline does not is admission-control policy engines and
image scanning, which belong to the security discipline rather than to platform engineering.

---

[← Certifications](../README.md)
