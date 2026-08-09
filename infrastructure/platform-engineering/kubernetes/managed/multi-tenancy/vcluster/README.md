[← Multi-tenancy](../README.md)

# vcluster

<https://github.com/loft-sh/vcluster>

---

## The problem it solves

A virtual cluster is a **real Kubernetes API server** running as a pod inside a namespace of a host
cluster, with its own data store. Tenants connect to it and are cluster-admin: they install CRDs,
run operators, create ClusterRoles, use a different Kubernetes version.

Their pods are then **synced down** to the host cluster's namespace and scheduled onto the host's
nodes. So the tenant gets the illusion of a private cluster, and the platform pays for one control
plane pod instead of one cluster.

This is the answer to the single problem namespaces cannot solve: shared CRDs. Two teams needing two
versions of the same operator is unsolvable with RBAC and trivial with two virtual clusters.

## When to use it

- Tenants who need their own CRDs, operators, or Kubernetes version
- Realistic per-developer or per-PR environments without provisioning real clusters
- Giving someone cluster-admin safely — it is admin of *their* API server, not yours
- Testing operators and CRDs, where installation is destructive to a shared cluster

## When not to use it

- Hard multi-tenancy against a hostile tenant; **pods still run on shared nodes and share a kernel**
- Where namespaces plus quota already work — this is more moving parts for no gain
- Workloads needing node-level access, privileged pods or host networking
- If nobody will manage the virtual clusters' lifecycle; orphaned vclusters are quietly expensive

## Notes

**Chart** `vcluster` from the Loft Helm repository, with a namespace manifest. But the useful content
here is the **CLI**, which is how vcluster is actually driven.

**Install**, pinned to `v0.24.1`:

```sh
curl -L -o vcluster "https://github.com/loft-sh/vcluster/releases/download/v0.24.1/vcluster-linux-amd64" \
  && sudo install -c -m 0755 vcluster /usr/local/bin && rm -f vcluster

vcluster --version
```

**The lifecycle:**

```sh
vcluster create my-vcluster --namespace team-x
kubectl get namespaces        # the virtual cluster's namespaces, not the host's
vcluster disconnect
vcluster delete my-vcluster --namespace team-x
```

The `kubectl get namespaces` in the middle is the demonstration, and it is worth pausing on: after
`vcluster create`, your kubeconfig context points at the virtual cluster's API server. The namespaces
listed are the ones inside it — `default`, `kube-system`, and whatever you create — not the host's.
`vcluster disconnect` puts the context back.

That context switch is also the main operational hazard. It is easy to forget which side you are on,
and `kubectl delete` behaves very differently depending on the answer. Pair it with
[kubectx](../../plugins/kubectx/README.md) or a prompt that shows the current context.

**What is real and what is illusion**, since this is where expectations go wrong:

| Real | Illusion |
|---|---|
| Its own API server and data store | it is not a cluster |
| Its own CRDs, at its own versions | nodes are the host's |
| Its own RBAC and ClusterRoles | the kernel is the host's |
| Its own Kubernetes version | node-level resources are synced, not owned |

So it isolates the **control plane** completely and the **data plane** not at all. For tenants who
are colleagues, that is the right split and an excellent deal. For a genuinely untrusted tenant, the
shared kernel means the answer is still
[sandboxed runtimes](../../../on-premise/container-runtime-sandbox/README.md) or a separate cluster.

**Loft Software** maintain it, with a commercial platform product above the open-source CLI. The
open-source part is fully functional; the fleet-management layer is the paid one.

---

[← Multi-tenancy](../README.md)
