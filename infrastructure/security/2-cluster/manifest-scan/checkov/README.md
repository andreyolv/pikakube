[← Manifest scan](../README.md)

# checkov

<https://github.com/bridgecrewio/checkov>
<https://github.com/bridgecrewio/checkov-action>
<https://www.checkov.io/5.Policy%20Index/kubernetes.html>

Context and comparison against the other tools: [../README.md](../README.md)

---

## The problem it solves

checkov is the broad one. kubesec scores a pod; kube-linter checks Kubernetes manifests;
checkov scans **infrastructure-as-code across the board** — Kubernetes, Terraform,
CloudFormation, Helm, Dockerfiles, ARM, Serverless — against a large library of built-in
policies. On a real platform, security misconfigurations do not live only in Kubernetes
YAML; they live in the Terraform that created the VPC and the Dockerfile that built the
image. checkov is the single scanner that sees all of it.

For the Kubernetes subset specifically, its checks (the `CKV_K8S_*` family, indexed at the
policy link above) overlap heavily with kube-linter: root user, privileged containers,
missing resource limits, writable root filesystem, dropped capabilities, seccomp profile
set, ServiceAccount token automounting. The difference is not the Kubernetes checks — it is
that the *same tool* also tells you the S3 bucket is public and the security group is open
to `0.0.0.0/0`.

Findings carry a stable ID (`CKV_K8S_23`, etc.), which is what makes exceptions manageable:
you skip a specific check on a specific resource by ID, in an annotation, with a reason
recorded next to it — rather than lowering the bar globally.

## When to use it

- **One scanner across a polyglot IaC repo** — the platform's Terraform, Helm charts, Dockerfiles and Kubernetes manifests all checked by one tool in one CI step
- Cloud misconfiguration checks that Kubernetes-only tools structurally cannot see (IAM, storage, network in Terraform/CloudFormation)
- CI gating with the official [`checkov-action`](https://github.com/bridgecrewio/checkov-action) for GitHub Actions
- Where a stable, referenceable finding ID and a documented policy index matter for audit and for managing exceptions

## When not to use it

- **As admission control.** Same ceiling as the whole folder: it runs in CI on files, and anything reaching the cluster outside CI bypasses it entirely. Enforcement is `policies/`
- As a focused pod-security score — that is kubesec, and it is more opinionated on `securityContext`
- As the reliability net — kube-linter's probe/limit/replica checks are sharper for Kubernetes operational readiness; checkov's strength is breadth, not Kubernetes depth
- Expecting runtime or image-CVE findings from the base tool. It is a configuration scanner. Vulnerability scanning of images is `3-container/`; runtime behaviour is `runtime-security/`

## Notes

The original notes in this folder were three links:

- <https://github.com/bridgecrewio/checkov> — the upstream tool, from Bridgecrew (now
  Prisma Cloud / Palo Alto Networks).
- <https://github.com/bridgecrewio/checkov-action> — the official GitHub Action, the
  intended way to run checkov as a CI gate.
- <https://www.checkov.io/5.Policy%20Index/kubernetes.html> — the Kubernetes policy index:
  the full list of `CKV_K8S_*` checks with their IDs and descriptions. This is the reference
  you use when deciding which check a finding is and whether to skip it.

This folder also ships a working example of running checkov **inside the cluster** as a Job
that scans the *live* cluster's resources (not just files in a repo):

- [`namespace.yaml`](namespace.yaml) — creates the `checkov` namespace.
- [`rbac.yaml`](rbac.yaml) — a `ServiceAccount`, a `checkov-view` `ClusterRole` and a
  binding. The ClusterRole grants `get`/`list`/`watch` on workloads, networking, RBAC and
  metrics resources but **deliberately excludes Secrets** (the comment says so): a scanner
  needs to read configuration, not credentials. This is a good, small example of
  least-privilege RBAC — worth reading for that alone.
- [`job.yaml`](job.yaml) — a one-shot `Job` (`image: bridgecrew/checkov-k8s:latest`) that
  runs under that ServiceAccount, `runAsNonRoot`, `runAsUser: 12000`,
  `allowPrivilegeEscalation: false`, dropping `ALL` capabilities. It is itself an example of
  the pod hardening checkov checks for.
- The `checkov.io/skip*` annotations on the Job are the exception mechanism in action:
  `CKV_K8S_22` (read-only root filesystem) is skipped because checkov needs to write dumped
  resource definitions; `CKV_K8S_38` (no ServiceAccount token) is skipped because this Job
  needs the token to read the API; `CKV_K8S_14`/`CKV_K8S_43` (pinned image digest / no
  `latest`) are skipped with the recorded reason of always wanting the latest rules on each
  run. Each skip carries its justification inline — which is exactly how exceptions should
  be recorded.

Two points about that example worth stating plainly. First, scanning the live cluster is a
different activity from scanning the repo — it catches drift and hand-applied resources that
CI never saw, which is genuinely useful. Second, it is still *reporting*, not enforcement:
the Job finds problems after they are already running. Do not mistake it for admission
control.

---

[← Manifest scan](../README.md)
