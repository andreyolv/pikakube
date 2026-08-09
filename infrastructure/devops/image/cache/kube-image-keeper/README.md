[← Image caching](../README.md)

# kube-image-keeper

<https://github.com/enix/kube-image-keeper>

---

## The problem it solves

**An image that ran once can always run again.** kube-image-keeper — `kuik`, pronounced "quick" —
copies every image a pod uses into a registry inside the cluster, and serves it from there
afterwards.

The mechanism has three parts:

| Component | Role |
|---|---|
| A **mutating webhook** | rewrites pod image references to point at the local proxy |
| A **cached image controller** | a `CachedImage` custom resource per image in use; a controller pulls and stores it |
| A **per-node proxy** | intercepts the pull, serves from the in-cluster registry, falls back upstream |

What that buys, concretely:

| Risk | Without | With |
|---|---|---|
| Docker Hub rate limits | anonymous pulls shared across the cluster's egress IP, and `toomanyrequests` at the worst moment | pulled once, then local |
| An upstream tag deleted or repushed | the workload cannot be restarted, or restarts as different code | the cached copy is authoritative |
| Upstream registry outage | new pods and scale-out fail | unaffected |
| Slow pulls on new nodes | full pull from the internet | from inside the cluster |

The property that makes it different from a plain pull-through cache is **intent**: a cache holds
what it happens to have; kuik holds what the cluster is actually running, tracked as Kubernetes
resources you can list and reason about.

## When to use it

- **anywhere production workloads pull from public registries** — the rate-limit and
  disappearance risks are real and arrive without warning
- clusters that scale out often, where every new node otherwise re-pulls from the internet
- where an audit needs an answer to "which external images are we running, and do we hold a copy"
- as insurance against an upstream image being deleted, which happens more often than anyone plans
  for

## When not to use it

- where everything already comes from a registry you control — the problem is solved upstream
- where the extra components are not wanted: it adds a registry, a controller, a webhook and a
  per-node proxy, all in the pod-creation and image-pull paths
- if cert-manager is not available or wanted; the webhook depends on it
- for pure **start-latency** problems on a known set of images, where
  [kube-fledged](../kube-fledged/README.md) is the smaller answer
- at very large scale, where the fan-out problem is distribution rather than availability —
  [`../../p2p-mirror/`](../../p2p-mirror/README.md)

## Notes

Recorded link:

- <https://github.com/enix/kube-image-keeper> — the project, by Enix. Apache-licensed, actively
  developed, and reasonably well documented for a tool of its size.

What is configured here: a Flux `HelmRelease` at chart version **1.5.0**, in its own namespace,
with two details worth reading:

```yaml
dependsOn:
- name: cert-manager
  namespace: cert-manager
```

**The cert-manager dependency is not optional.** kuik installs a mutating admission webhook, and
Kubernetes requires webhooks to be served over TLS with a CA bundle the API server trusts.
cert-manager issues and rotates that certificate. Expressing it as a Flux `dependsOn` is exactly
right — without it, Flux may install kuik before cert-manager is ready, the webhook certificate
never appears, and the failure looks like an unrelated admission error.

```yaml
docker-registry-ui:
  enabled: true
```

The bundled registry UI, so the cached images can be browsed. Useful for confirming that caching
is actually happening, and a thing to keep off any public Ingress.

**The operational risk to know before deploying it**, and it applies to any admission-webhook
tool: the webhook sits in the pod-creation path. If it is unavailable and its failure policy is
`Fail`, **no pods are created anywhere the webhook's scope covers**. Check the chart's
`failurePolicy` and replica count and choose deliberately, rather than discovering the default
during an incident. The second thing to plan is retention — the in-cluster registry grows with
every distinct image the cluster has ever run.

## Where it fits here

The most complete of the three tools in [`cache/`](../README.md), and the one that addresses a
risk rather than a latency. [kube-fledged](../kube-fledged/README.md) makes known images start
faster; [k8s-image-swapper](../k8s-image-swapper/README.md) redirects references to a registry you
control; kuik guarantees that whatever ran once can run again.

The cheaper first step remains the one in
[§3 of the parent](../README.md#3-the-cheap-fixes-first): a pull-through cache in front of Docker
Hub. kuik is what you add when "we hold a copy of everything we run" needs to be true and
verifiable.

---

[← Image caching](../README.md)
