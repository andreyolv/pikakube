[← Scheduler](../README.md)

# Custom scheduler

<https://kubernetes.io/docs/concepts/scheduling-eviction/resource-bin-packing/>
<https://kubernetes.io/docs/tasks/extend-kubernetes/configure-multiple-schedulers/#define-a-kubernetes-deployment-for-the-scheduler>
<https://stackoverflow.com/questions/74638464/configuring-mostallocated-on-an-eks-cluster>

---

## The problem it solves

The default scheduler spreads pods across nodes (`LeastAllocated`). That is good for resilience and
expensive, because a node cannot be removed until it is empty and spreading ensures none ever is.
Switching the scoring strategy to `MostAllocated` produces **bin packing**: pods concentrate on nodes
that already have work, other nodes empty out, and the cluster autoscaler can remove them.

On a self-managed cluster that is a `KubeSchedulerConfiguration` change. **On AKS and EKS it is
impossible** — the control plane is the provider's, and the scheduler's configuration is not exposed.

The workaround implemented here is the generic one: run a **second scheduler** with the desired
configuration, alongside the default, and direct pods to it.

## When to use it

- Bin packing on a managed cluster, where the default scheduler cannot be reconfigured
- Any scheduling policy that must apply to some workloads and not others
- Trying a scheduling change without touching the scheduler everyone else depends on
- Cloud-portable — the mechanism is upstream Kubernetes, not a provider feature

## When not to use it

- Self-managed clusters, where configuring the real scheduler is simpler and has no extra component
- When affinity or topology spread constraints would express the requirement
- Without PodDisruptionBudgets; packed pods mean a lost node takes more with it
- If nobody will own it — this is a scheduler you now operate

## Notes

### Why it exists

**You cannot configure the default scheduler on the managed clouds.** The recorded issues:

- AKS — <https://github.com/Azure/AKS/issues/4203>
- EKS — <https://github.com/aws/containers-roadmap/issues/1468>

And the AWS-provided sample, assessed bluntly in the original note as *"bad, AWS-specific and
unmaintained"*:

- <https://github.com/aws-samples/custom-scheduler>

The generic, cloud-independent route taken instead:

- <https://kubernetes.io/docs/tasks/extend-kubernetes/configure-multiple-schedulers/#define-a-kubernetes-deployment-for-the-scheduler>
- <https://stackoverflow.com/questions/74638464/configuring-mostallocated-on-an-eks-cluster>

### The scheduler configuration

`configmap.yaml` holds a `KubeSchedulerConfiguration` for a scheduler named
**`most-allocated-scheduler`**:

```yaml
scoringStrategy:
  resources:
    - name: cpu
      weight: 1
    - name: memory
      weight: 1
  type: MostAllocated
```

with the scoring plugins reduced to one:

```yaml
plugins:
  score:
    disabled:
      - name: '*'
    enabled:
      - name: NodeResourcesFit
        weight: 1
```

Two deliberate decisions are encoded there:

- **`type: MostAllocated`** with equal CPU and memory weight — prefer the node that is already
  fullest, considering both resources equally. This is the bin packing.
- **Every other scoring plugin disabled.** Normally a dozen plugins vote — image locality, pod
  spreading, node affinity, taint toleration. Disabling them makes packing the *only* consideration,
  which is decisive and blunt. It also discards spreading behaviour that other workloads may have
  been relying on, which is the trade-off to be aware of.

`leaderElect: false` means a single replica. Fine for a secondary scheduler; it also means no
scheduling for pods assigned to it while that pod is restarting.

Note the API version: `kubescheduler.config.k8s.io/v1beta2`. That is an **old** version and it has
been removed in current Kubernetes releases. Before this is deployed anywhere modern, the config
needs migrating to `v1` — otherwise the scheduler will refuse to start on the API version alone.

### Directing pods to it, without editing manifests

The elegant part. `assign-scheduler.yaml` is a **Gatekeeper mutation** that sets
`spec.schedulerName` on every Pod at admission:

```yaml
location: "spec.schedulerName"
parameters:
  assign:
    value: most-allocated-scheduler
match:
  excludedNamespaces: ["kube-system"]
```

So no workload manifest changes and no developer has to know the scheduler exists. Excluding
`kube-system` is essential: control-plane and system components must keep using the default
scheduler, and pointing them at a single-replica secondary one is a good way to make a cluster
unrecoverable.

`assign-metadata.yaml` is a second, unrelated Gatekeeper mutation — it sets an `owner` annotation on
pods in the `purview-catalog` namespace. Kept here as an example of `AssignMetadata` alongside
`Assign`; the two together are the mutation vocabulary.

### The risks, plainly

- **A pod assigned to a scheduler that is not running stays `Pending` forever.** No error, no event
  from the default scheduler — it simply is not its pod. If the mutation is applied cluster-wide and
  the scheduler is down, nothing new schedules anywhere.
- **`kube-system` must be excluded**, as above.
- **Packing raises blast radius.** Pair it with PodDisruptionBudgets and topology spread constraints
  for workloads that genuinely need spreading.
- **Gatekeeper is now in the scheduling path.** A mutation webhook failure has cluster-wide effect —
  the same class of risk described in [`multi-tenancy/`](../../multi-tenancy/README.md).

The upstream reference for the theory:
<https://kubernetes.io/docs/concepts/scheduling-eviction/resource-bin-packing/>.

---

[← Scheduler](../README.md)
