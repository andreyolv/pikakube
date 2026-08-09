[← Pod security](../README.md)

# AppArmor

<https://kubernetes.io/docs/tutorials/security/apparmor/>
<https://apparmor.net/>

Context and comparison against the other tools: [../README.md](../README.md)

---

## The problem it solves

seccomp filters *syscalls*. AppArmor confines a different axis: **which files, paths,
capabilities and network operations a process may touch.** It is a Linux Mandatory Access
Control (MAC) system — the kernel enforces the profile regardless of file ownership or the
process's own privileges, so even a root process is boxed in by the profile.

Where a discretionary permission model asks "does this user own the file", MAC asks "does
the policy permit *this program* to open *this path* at all", and the policy wins. That is
the property that makes it useful for containment: a compromised process cannot read
`/etc/shadow` or write outside its allowed paths if the profile does not grant it, even if
Unix permissions would.

An AppArmor profile lists rules like "may read `/usr/**`", "may not write `/**`", "deny
`capability net_raw`". A container is put into a profile, and from then on any operation
outside the profile is denied by the kernel.

The relationship to the other tools in this folder:

| Layer | Controls | Tool |
|---|---|---|
| Identity & capabilities | who the process is, what capabilities it holds | [securityContext](../security-context/README.md) |
| Syscalls | which kernel calls are allowed | [seccomp](../seccomp/README.md) |
| **File/path/capability access (MAC)** | **which files and resources the process may touch** | **AppArmor** |

They are complementary layers, not alternatives. AppArmor is the file-access dimension the
other two do not cover.

## When to use it

- Confining a workload's filesystem access beyond `readOnlyRootFilesystem` — for example denying all writes, or all access to a sensitive path, at the kernel level
- On Debian/Ubuntu and SUSE nodes, where AppArmor is the native MAC system (Red Hat / Fedora use SELinux instead — the equivalent axis, different implementation)
- High-value workloads where you want a positive allow-list of the files the process may touch, enforced by the kernel
- As one layer in a stack that also sets `securityContext` and a seccomp profile

## When not to use it

- On nodes without AppArmor. It is kernel- and distro-specific: no AppArmor loaded on the node means the profile cannot be enforced. On SELinux distros you use SELinux instead
- As the only confinement. Like seccomp, it defends one axis; combine it with the others
- Hand-authoring complex profiles from scratch. Writing an AppArmor profile by hand has the same problem as writing a seccomp profile by hand — you do not know every path the app touches. [security-profiles-operator](../security-profiles-operator/README.md) can **record** AppArmor profiles from a running workload, which is the sane way to produce them
- Assuming the profile is loaded. The profile must already exist on the node; Kubernetes references it by name, it does not distribute it. Getting the profile onto every node is the actual operational work (again, what security-profiles-operator handles)

## Notes

This folder had no `doc.md` — only one example manifest.

- [`hello-apparmor.yaml`](hello-apparmor.yaml) — a pod that applies the profile
  `k8s-apparmor-example-deny-write` to its container. The mechanism is the annotation
  `container.apparmor.security.beta.kubernetes.io/hello: localhost/k8s-apparmor-example-deny-write`,
  where `hello` is the container name and `localhost/<name>` means "a profile already loaded
  on the node under that name". The container just runs `echo` and sleeps; the point is that
  with that profile any **write** would be denied by the kernel.

Two things worth recording from that example:

- **The profile must be loaded on the node first.** The annotation only *references* a
  profile named `k8s-apparmor-example-deny-write`; it does not create it. If that profile is
  not present on the node, the pod will not run as intended. This is the operational catch
  with AppArmor, and the reason the security-profiles-operator exists.
- **The annotation syntax is the old, beta one.** Kubernetes 1.30+ promoted AppArmor to a
  proper field, `securityContext.appArmorProfile`, and the
  `container.apparmor.security.beta.kubernetes.io/*` annotation is deprecated (still honoured
  for backward compatibility). New workloads should use the field; this example predates it.

Do not modify this file; it is a reference example.

---

[← Pod security](../README.md)
