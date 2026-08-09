[← Progressive delivery](../README.md)

# Flagger

<https://github.com/fluxcd/flagger>
<https://docs.flagger.app/>

---

## The problem it solves

Automated canary releases driven by **metrics**, without changing how workloads are defined.

Flagger watches a normal `Deployment`. When the image changes it creates a canary, shifts
traffic to it in steps, queries Prometheus at each step, and either promotes or rolls back —
with no human watching a dashboard.

That non-invasiveness is its main distinction from [Argo Rollouts](../argo-rollouts/README.md): your
manifests stay ordinary `Deployment` resources, and a `Canary` object describes the release
policy alongside them.

```yaml
# roughly: step size, interval, and what must hold
analysis:
  interval: 1m
  threshold: 5
  stepWeight: 10
  metrics:
    - name: request-success-rate
      thresholdRange: {min: 99}
    - name: request-duration
      thresholdRange: {max: 500}
```

## When to use it

- **Flux** is the GitOps tool — same project, and the integration is direct
- you do not want to replace `Deployment` with a different resource type
- automated promotion and rollback, with no manual gate

## When not to use it

- you want a **UI** and manual approval steps — [Argo Rollouts](../argo-rollouts/README.md)
- traffic is too low for percentages to be statistically meaningful
- there is no traffic-splitting layer yet, which is the actual prerequisite

## Traffic providers

Flagger does not split traffic itself. It drives something that does:

- service meshes — Istio, Linkerd, Kuma, Open Service Mesh
- ingress controllers — NGINX, Traefik, Contour, Gloo
- Gateway API

The provider decides which strategies are available: mirroring and header-based routing need L7
capability that a basic ingress controller may not have.

## References

- <https://docs.flagger.app/usage/how-it-works>
- <https://docs.flagger.app/tutorials/nginx-progressive-delivery>
- [GitOps with Linkerd, a full worked example](https://github.com/stefanprodan/gitops-linkerd/tree/main)
- [Progressive delivery on DigitalOcean Kubernetes](https://www.digitalocean.com/community/tutorials/how-to-progressively-deliver-releases-using-flagger-on-digitalocean-kubernetes)

---

[← Progressive delivery](../README.md)
