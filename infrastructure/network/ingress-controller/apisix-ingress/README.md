[← Ingress controller](../README.md)

# APISIX Ingress Controller

<https://github.com/apache/apisix-ingress-controller>
<https://github.com/apache/apisix-helm-chart>
<https://apisix.apache.org/docs/ingress-controller/getting-started/>

Context and comparison: [../README.md](../README.md)

---

## What it is

The controller that drives [Apache APISIX](../../api-gateway/apisix/README.md) from Kubernetes
objects — `Ingress`, plus APISIX CRDs such as `ApisixRoute` and `ApisixPluginConfig`.

APISIX is the gateway; this is what configures it from the cluster API. Two artifacts, one
data path.

## When to use it

- **APISIX is already the gateway**, and you want it configured declaratively from Kubernetes
- you want APISIX's dynamic configuration — plugin and route changes apply without reloading the proxy

## When not to use it

- there is no API management requirement; a plain ingress controller is less to operate
- APISIX has not been chosen yet — make that decision in [`api-gateway/`](../../api-gateway/README.md) first

## Related

Gateway and API-management context: [`api-gateway/apisix/`](../../api-gateway/apisix/README.md)

---

[← Ingress controller](../README.md)
