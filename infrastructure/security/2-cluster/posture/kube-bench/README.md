[← Posture assessment](../README.md)

# kube-bench

<https://github.com/aquasecurity/kube-bench>

Runs the CIS Kubernetes Benchmark against a cluster and prints a pass/fail/warn report. One binary,
one Job, no operator.

---

## The problem it solves

The CIS Kubernetes Benchmark is a few hundred pages of prose describing how a hardened cluster
should be configured: which flags the API server should carry, which permissions the files under
`/etc/kubernetes` should have, how the kubelet should be configured, whether etcd is encrypted.
Checking it by hand is a day of work and it is out of date the following week.

kube-bench turns that document into an executable check. It inspects the node it runs on — process
arguments, config files, file permissions — and reports each control as `[PASS]`, `[FAIL]`, `[WARN]`
or `[INFO]`, with the remediation text from the benchmark attached.

Two design decisions define how it behaves:

**It runs on the node, not against the API.** The controls are about processes and files, so the
tool has to see them. `job.yaml` here mounts `/var/lib/etcd`, `/var/lib/kubelet`,
`/var/lib/kube-scheduler`, `/var/lib/kube-controller-manager`, `/etc/systemd`, `/lib/systemd`,
`/srv/kubernetes`, `/etc/kubernetes`, `/etc/cni/net.d`, `/opt/cni/bin` and `/usr/bin` from the host,
all read-only, with `hostPID: true` so it can inspect running processes. That is a lot of authority,
and it is why this should be a Job rather than a permanent DaemonSet.

**It auto-detects what to check.** It works out the Kubernetes version and which components are
present on the node, then selects the matching benchmark. That detection is why `/usr/bin` is
mounted at `/usr/local/mount-from-host/bin` — it needs `kubectl`/`kubelet` to determine the version.
Passing `--version` or `--benchmark` explicitly removes the need for that mount.

The `[WARN]` category is the one to understand: those are the benchmark's *unscored* controls, which
have no automatable test. They are not failures — they are a list of things a human has to judge.

## When to use it

- **You run the control plane yourself.** On kubeadm, kubespray, RKE or bare-metal clusters, every
  control is both checkable and fixable. This is where kube-bench is at its best.
- **An auditor asked for CIS Benchmark evidence.** This is the tool that produces exactly that
  artefact, mapped control by control, with the official numbering.
- **After a cluster upgrade.** Component defaults change between Kubernetes versions, and an upgrade
  is the event most likely to move a control from pass to fail. Running it as a Job after each
  upgrade catches essentially everything a scheduled scan would.
- **On a new node image.** The node-level controls (kubelet flags, file permissions, systemd units)
  are properties of the image and the bootstrap process, so checking them once per image is
  proportionate.
- **To bootstrap a hardening backlog.** The first run on a cluster nobody hardened produces a real
  list of concrete, remediable items with instructions attached.

Selecting the right benchmark matters: `--benchmark` and `--targets` pick between the generic
Kubernetes benchmark and the provider-specific ones (EKS, AKS, GKE, RKE, OpenShift). The default
detection is usually right on self-managed clusters and usually not what you want on a managed one.

## When not to use it

- **As the security programme.** It checks configuration against one document. It says nothing about
  RBAC bindings anyone actually holds, application vulnerabilities, secrets in Git, or a workload
  currently mining cryptocurrency. See [`../README.md`](../README.md#4-why-the-score-is-a-starting-point-not-a-programme).
- **On a managed control plane, expecting a clean run.** On AKS, EKS or GKE the API server, scheduler,
  controller manager and etcd are not yours. Those checks come back as failures or `[INFO]` and there
  is no action available. Use the provider benchmark and read only the sections you control — kubelet,
  node files, and the policy recommendations.
- **As a continuous monitor.** It is a point-in-time snapshot with no history, no diffing, no
  alerting. If you want drift detection, either wrap it in a scheduled Job and store the JSON output,
  or use something built for it — [kubescape](../kubescape/README.md) is the neighbour that does.
- **For workload security.** It covers Pod-level recommendations only lightly and does not evaluate
  your actual Deployments. That is [`../../policies/`](../../policies/README.md) for enforcement and
  kubescape for assessment.
- **As a permanently running privileged workload.** A pod with `hostPID` and ten host mounts is a
  meaningful attack surface. Run it, read it, delete it.

## Notes

The original `doc.md` contained only the repository link, which is at the top of this file. What
follows is the state of this folder.

### How it is deployed here

Two files: `namespace.yaml` and `job.yaml`. No Helm chart, no HelmRelease, no schedule, no
kustomization. That is a deliberate and correct shape for this tool — it means running the benchmark
is an explicit act.

Details of `job.yaml` worth knowing:

| Element | Why |
|---|---|
| `image: docker.io/aquasec/kube-bench:v0.6.17` | pinned, but old enough to be worth checking against current Kubernetes versions — benchmark content ships in the image |
| `hostPID: true` | required to inspect the arguments of running control-plane and kubelet processes |
| ten read-only host mounts | the controls are about files and directories on the node |
| `restartPolicy: Never` | a benchmark that failed should not silently re-run |

There is no `nodeSelector` and no toleration for control-plane taints, so on a cluster where the
control plane is tainted the Job lands on a worker node and only the node-level controls are
evaluated. On a managed cluster that is all you get anyway; on a self-managed one, scheduling it
onto a control-plane node is the difference between a partial report and a complete one.

Results go to the pod's stdout: `kubectl logs job/kube-bench -n kube-bench`. `--json` produces
machine-readable output if the results are to be stored or diffed over time.

### Practical reading of the output

The failures worth acting on first, in order:

1. **Anonymous auth and insecure ports.** Anything that grants access without authentication.
2. **Kubelet configuration.** `--anonymous-auth=false`, `--authorization-mode=Webhook`,
   `--read-only-port=0`. These are yours even on managed node pools, and they are the most commonly
   wrong.
3. **etcd encryption and access.** Only relevant if you run etcd.
4. **File permissions.** Real, cheap to fix, and rarely the way anyone gets in.

Everything under `[WARN]` needs a person to decide, and "we accepted this, because X" written next to
it is worth more than a re-run.

### Where it fits with the neighbours

kube-bench answers "is the cluster configured the way CIS says". [kubescape](../kubescape/README.md)
answers a broader question across more frameworks and keeps history;
[kubeeye](../kubeeye/README.md) answers an operational-health question. They overlap, and only
kube-bench is the authoritative CIS answer.

Findings that recur — a missing setting that keeps coming back after every cluster rebuild — should
stop being scan findings and become configuration or admission policy. Scanning finds a problem
once; [`../../policies/`](../../policies/README.md) prevents it.

---

[← Posture assessment](../README.md)
