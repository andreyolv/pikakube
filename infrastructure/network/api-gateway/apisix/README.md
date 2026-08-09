[← API gateway](../README.md)

# Apache APISIX

<https://github.com/apache/apisix>
<https://github.com/apache/apisix-helm-chart>
<https://apisix.apache.org/docs/apisix/getting-started/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

An Apache Software Foundation API gateway built on NGINX/OpenResty, whose distinguishing
trait is **fully dynamic configuration**: routes, plugins, upstreams and consumers change at
runtime with **no reload** of the proxy.

That matters more than it sounds. A gateway that reloads to apply a route change has a
window where connections are disrupted, which puts a ceiling on how often anyone is willing
to change it. APISIX removes the window, so configuration stops being a deployment event.

Alongside that: a large plugin set, consumer and credential handling, and an admin API.

## When to use it

- configuration changes frequently, and reload behaviour is a real constraint
- you want an ASF-governed project rather than a vendor-led one
- the plugin set covers the requirement and you value dynamic reconfiguration over ecosystem size

## When not to use it

- ecosystem size and available examples matter most — [Kong](../kong/README.md) is ahead there
- you need a portal and per-plan analytics out of the box — [Tyk](../tyk/README.md) includes more
- there are no external consumers at all, in which case an [ingress controller](../../ingress-controller/README.md) is the right layer

## Kubernetes

Configuration from cluster objects comes from the separate controller:
[`ingress-controller/apisix-ingress/`](../../ingress-controller/apisix-ingress/README.md)

---

[← API gateway](../README.md)
