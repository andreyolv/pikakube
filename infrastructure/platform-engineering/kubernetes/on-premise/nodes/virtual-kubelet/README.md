[← Nodes](../README.md)

# virtual-kubelet

<https://github.com/virtual-kubelet/virtual-kubelet>
<https://github.com/virtual-kubelet/azure-aci>

---

## The problem it solves

virtual-kubelet implements the kubelet's API without a machine behind it. It registers as a node,
Kubernetes treats it as one, and pods scheduled onto it are handed to a **provider** — a cloud
container service, another cluster, an edge platform — which runs them somewhere else entirely.

The elegance is that nothing else has to change. The scheduler, Deployments, Services, affinity rules
and `kubectl` all work as normal, because from the API's point of view there is simply another node.

It is a CNCF project, and the pattern matters more than the project: it is the mechanism underneath
several tools mapped elsewhere in this repository.

## When to use it

- Bursting to a serverless container service — Azure Container Instances, AWS Fargate — when the
  cluster is full
- Edge locations that should appear as capacity in a central cluster
- Presenting a non-Kubernetes execution environment through the Kubernetes API
- As a library, when building something that needs to look like a node

## When not to use it

- Workloads needing DaemonSets, host networking, host paths or privileged access — none of that exists
  on a node that is not a machine
- Where per-pod cost on the backing service exceeds running a real node
- Stateful workloads, where volume semantics differ from what pods expect
- Without accounting for how different the failure modes are

## Notes

**Installed from a `GitRepository`** with a namespace manifest — the project does not publish a
packaged chart, so Flux builds it from the repository tree. Same pattern as
[KubeView](../../../managed/dashboards/kubeview/README.md) and
[HNC](../../../managed/multi-tenancy/hierarchical-namespaces/README.md) in this repository.

**Two links, and the second is the important one.**
`virtual-kubelet/virtual-kubelet` is the **framework** — it does nothing on its own. A **provider**
implements the actual "run a pod" behaviour, and `virtual-kubelet/azure-aci` is the concrete example:
pods scheduled onto the virtual node become Azure Container Instances.

Recording both is the right instinct, because installing the framework alone and expecting pods to
run somewhere is the first confusion available. There is no default provider.

**What the abstraction hides**, and these are the things that break:

- **DaemonSets do not run there.** No log collector, no monitoring agent, no CNI, no service mesh
  sidecar injector operating as a DaemonSet. Anything relying on a per-node agent is absent for those
  pods.
- **`kubectl logs` and `exec` are proxied** by the provider, with the provider's latency and the
  provider's failure modes. When the far side is unreachable, the symptoms resemble nothing a real
  node produces.
- **Pod-to-pod networking depends entirely on the provider.** Whether a pod on the virtual node can
  reach a Service in the cluster is a provider question, not a Kubernetes one.
- **Node-level resources are simulated.** The capacity a virtual node advertises is a number someone
  chose, and the scheduler believes it.

**Where the pattern shows up elsewhere here:**
[Admiralty](../../../managed/multi-cluster/admiralty/README.md) and
[Liqo](../../../managed/multi-cluster/liqo/README.md) both present remote *clusters* as virtual nodes,
so the ordinary scheduler places work across cluster boundaries without any new scheduling concepts.
Understanding this project is understanding how those work.

---

[← Nodes](../README.md)
