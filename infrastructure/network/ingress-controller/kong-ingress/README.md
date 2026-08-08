[← Ingress controller](../README.md)

# Kong Ingress Controller

<https://github.com/Kong/kubernetes-ingress-controller>
<https://github.com/Kong/charts>
<https://docs.konghq.com/kubernetes-ingress-controller/>

Context and comparison: [../README.md](../README.md)

---

## What it is

The controller that lets [Kong](../../api-gateway/kong/) act on Kubernetes objects: it reads
`Ingress`, and Kong CRDs such as `KongPlugin` and `KongConsumer`, and configures the Kong
data path accordingly.

Kong and this controller are **two artifacts**: Kong is the gateway, this is what drives it
from the cluster API.

## When to use it

- **Kong is already the gateway**, and you want Kubernetes-native configuration for it
- you want Ingress routing today and API management later, without changing the data path — plugins attach to the same routes

## When not to use it

- there is no API management requirement. Running Kong purely as an ingress controller means operating a gateway to do a job [ingress-nginx](../ingress-nginx/) or [Traefik](../traefik/) does with far less
- you have not chosen Kong yet — decide that first, in [`api-gateway/`](../../api-gateway/README.md)

## Related

Gateway and API-management context: [`api-gateway/kong/`](../../api-gateway/kong/)

---

[← Ingress controller](../README.md)
