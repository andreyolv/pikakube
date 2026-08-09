[← Local](../README.md)

# Distributions

<https://github.com/kubernetes-sigs/kind>
<https://github.com/k3d-io/k3d>
<https://github.com/k3s-io/k3s>
<https://github.com/kubernetes/minikube>
<https://github.com/k0sproject/k0s>
<https://github.com/canonical/microk8s>
<https://github.com/derailed/k9s>
<https://github.com/kubernetes-sigs/cloud-provider-kind>

---

## The problem it solves

You need a Kubernetes API server that starts in seconds, can be deleted without ceremony, and
behaves enough like the real thing that manifests, CRDs, admission webhooks and controllers can be
tested against it.

Each of these solves that differently: **kind** runs upstream Kubernetes with each node as a Docker
container. **k3d** does the same for k3s, which is a smaller distribution with substituted
components. **minikube** predates both and supports a wide range of drivers, including real VMs.
**k0s** and **MicroK8s** are single-binary and snap-packaged installs aimed at clusters that live
longer than a test run.

## When to use it

- kind — you want upstream Kubernetes, unmodified, with multi-node topology and good CI support
- k3d — you want the fastest start and the smallest memory footprint, and k3s's substitutions are acceptable
- minikube — you need a hypervisor driver the others do not offer, or an addon it bundles
- k0s / MicroK8s — a single-node cluster on a real machine that is meant to persist
- k9s — always; it is a terminal UI, orthogonal to which cluster you are on

## When not to use it

- Anything involving node capacity, resource pressure or eviction — see the note below
- Performance testing; the nodes share one kernel and one machine
- Multi-zone or topology-spread behaviour, which has no meaning here
- Load-balancer semantics, unless `cloud-provider-kind` is added on purpose
- Scale testing — [`kwok`](../../on-premise/nodes/kwok/README.md) fakes thousands of nodes cheaply and is the right tool

## Notes

**kind cannot set node names or node capacity.** This is the recorded finding and it is a real
limitation, not a missing flag:

- <https://github.com/kubernetes-sigs/kind/issues/877>
- <https://github.com/kubernetes/kubernetes/issues/120832>

The consequence is concrete: any test that depends on a node being called something specific, or
on a node advertising a particular amount of CPU or memory, cannot be written against kind. That
rules out most scheduler, autoscaler and bin-packing experiments — which is why
[`managed/scheduler/`](../../managed/scheduler/README.md) work needs either a real cluster or a
simulator.

**Load balancers on kind** need <https://github.com/kubernetes-sigs/cloud-provider-kind>. Without
it, a `Service` of type `LoadBalancer` stays `<pending>` forever, which looks like a broken
manifest and is not.

**Upgrading kind** is manual, because kind is installed as a release binary rather than through a
package manager. The recorded procedure:

```sh
which kind
sudo rm -f /usr/local/bin/kind
# then reinstall from
# https://kind.sigs.k8s.io/docs/user/quick-start/#installing-from-release-binaries
```

Worth writing down precisely because there is no `kind upgrade` — people look for one, do not find
it, and end up running an old version for a year.

**k3s appears here twice on purpose.** k3d is a wrapper that runs k3s in Docker; k3s itself is the
distribution and runs fine directly on a machine. Choosing k3d means choosing k3s's opinions —
Traefik as the ingress controller, its own service load balancer, SQLite instead of etcd unless
configured otherwise — and those opinions are the reason it is fast.

---

[← Local](../README.md)
