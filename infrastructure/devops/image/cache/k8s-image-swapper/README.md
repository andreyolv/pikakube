[← Image caching](../README.md)

# k8s-image-swapper

<https://github.com/estahn/k8s-image-swapper>
<https://github.com/estahn/charts>

---

## The problem it solves

**Nothing pulls from a public registry any more, and no manifest had to change.**
k8s-image-swapper is a mutating admission webhook: when a pod is created, it rewrites the image
reference to a registry you control, and copies the image there on first use if it is not already
present.

```
image: nginx:1.25                     →  image: 123456.dkr.ecr.eu-west-1.amazonaws.com/nginx:1.25
```

The application manifests, the Helm charts and the upstream charts you did not write all keep
saying `nginx:1.25`. The rewrite happens at admission time.

| Problem | How the swap addresses it |
|---|---|
| Docker Hub rate limits | pulls go to your registry, not to a shared anonymous quota |
| Upstream outage | your registry has the copy |
| Egress cost and latency | the registry is next to the cluster |
| "Which external images are we running" | they are all in one registry, listable |
| Third-party charts hard-coding registries | rewritten anyway, with no fork and no values override |

That last row is the underrated one. Overriding the image registry in someone else's Helm chart
means finding the right values key in every chart, and some charts do not expose one. An admission
webhook does not care.

## When to use it

- **a policy that all images come from a registry you control**, applied without editing manifests
- heavy use of third-party Helm charts whose image references are awkward to override
- rate limiting or egress cost from public registries is an actual problem
- **on AWS**, where the ECR integration is the best-supported path by some distance

## When not to use it

- **on Azure** — see the recorded limitation below
- where images already come from a registry you control
- where an admission webhook in the pod-creation path is not acceptable risk
- when the requirement is really "keep a copy of everything we run" with per-image visibility —
  [kube-image-keeper](../kube-image-keeper/README.md) models that explicitly
- when the requirement is start latency on a few known images —
  [kube-fledged](../kube-fledged/README.md)

## Notes

Recorded links and findings, in full:

- <https://github.com/estahn/k8s-image-swapper> — the project.
- <https://github.com/estahn/charts> — the maintainer's chart repository, which is where the Helm
  chart used here comes from. Worth noting that it is a personal chart repository rather than an
  organisation's, which is a small supply-chain consideration in itself.

> **Does not support Azure Container Registry** —
> [estahn/k8s-image-swapper#572](https://github.com/estahn/k8s-image-swapper/issues/572)

This is the finding that decides the evaluation on Azure, and it is worth understanding rather
than filing away. k8s-image-swapper does not merely rewrite references; it must also **create
repositories and copy images** into the target registry, and that part is registry-specific. The
tool was built around **AWS ECR** — including ECR's repository creation API, its authentication
flow and its lifecycle policies — and other backends have followed unevenly. On ACR the
integration is not there, so the tool cannot do the copy half of its job.

The practical consequence: on AWS this is a strong option; on Azure it is not an option at all,
and the alternatives are a pull-through cache configured on the registry side, or
[kube-image-keeper](../kube-image-keeper/README.md), which runs its own in-cluster registry and
therefore has no cloud-registry integration to be missing.

What is configured here: a Flux `HelmRelease` at chart version **1.11.0** from the `estahn` chart
repository, in its own namespace, with the values left as comments pointing at the chart's
`values.yaml` — so this is mapped rather than tuned.

**The webhook risk applies here too**, and it is the same one as for
[kube-image-keeper](../kube-image-keeper/README.md): the webhook is in the pod-creation path. With
`failurePolicy: Fail` and a single replica, an unavailable webhook stops pod creation across its
scope. Check the failure policy, the namespace selectors and the replica count before deploying,
and make sure the webhook's own namespace is excluded — a webhook that must be running to create
the pod that runs the webhook is a bootstrap that cannot start.

## Where it fits here

The third model in [`cache/`](../README.md): not a cache and not a pre-puller, but a **redirection
policy**. It is the right tool when the requirement is stated as "everything must come from our
registry" and manifests cannot all be edited.

Since this repository is not AWS-based, the recorded ACR limitation is the reason it stays mapped
rather than deployed. The equivalent outcome here comes from a pull-through cache on whichever
registry from [`../../oci-registry/`](../../oci-registry/README.md) is chosen, configured as a
runtime mirror on the nodes.

---

[← Image caching](../README.md)
