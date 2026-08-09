[← Container runtime sandbox](../README.md)

# gVisor

<https://github.com/google/gvisor>

---

## The problem it solves

gVisor puts a **kernel written in Go between the container and the host kernel**. Its `runsc` runtime
intercepts the container's system calls and implements most of them in userspace, forwarding only a
small, deliberately restricted set to the real kernel.

The effect on the threat model is significant: a container exploiting a Linux kernel vulnerability
reaches gVisor's implementation of that call rather than the kernel's. The host's syscall surface —
the several hundred calls that are the usual attack surface — is largely unreachable.

Google run it in production for App Engine, Cloud Run and Cloud Functions, which is the strongest
evidence available that the approach works at scale.

## When to use it

- Running untrusted code: customer-supplied builds, CI jobs from external pull requests, sandboxes
- Multi-tenant nodes where a kernel exploit must not become a node compromise
- Workloads that are not syscall- or I/O-heavy, where the overhead is acceptable
- Where a VM per pod ([Kata](../kata-containers/README.md)) is more memory than you can spend

## When not to use it

- Trusted first-party workloads — the cost buys nothing
- I/O-heavy or syscall-heavy applications; the overhead lands hardest exactly there
- Anything needing unusual syscalls, direct device access or host networking
- Without testing the actual workload — unimplemented syscalls fail at **runtime**

## Notes

**The manifests here are a good minimal experiment**, and worth describing because the design is
deliberate.

`runtimeclass.yaml`:

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
```

`handler: runsc` refers to a runtime **configured in containerd on the node**. The `RuntimeClass`
does not install anything; it is a cluster-level name for something that must already exist on the
machine.

Then two nearly identical pods:

- `pod.yaml` — nginx, ordinary runtime
- `pod-gvisor.yaml` — nginx, `runtimeClassName: gvisor`

Same image, one difference. That is the right way to evaluate a sandbox: run both, then compare
`dmesg` visibility, `/proc` contents, syscall behaviour and performance. The comparison is the
experiment, and having the control pod committed alongside is what makes it one.

**The prerequisite that is not in this folder:** `runsc` must be installed on the node and registered
in `/etc/containerd/config.toml` as a runtime handler. Without that, the gVisor pod fails to start
with an error about an unknown runtime — which reads like a manifest problem and is a node problem.
On managed clusters this is generally impossible unless the provider offers gVisor natively (GKE
Sandbox does).

**How to verify it is actually working**, once running: inside the gVisor pod, `dmesg` shows gVisor's
own boot output rather than the host's, and `/proc/version` reports a gVisor kernel string. If it
looks like the host, the `RuntimeClass` was not applied.

**The compatibility caveat, restated because it is the reason gVisor is rejected in practice:**
gVisor implements most of the Linux syscall interface, not all of it. An application using an
unimplemented call gets an error at the moment it makes the call — possibly under a rare code path,
in production, weeks later. Test the real workload, not a placeholder.

---

[← Container runtime sandbox](../README.md)
