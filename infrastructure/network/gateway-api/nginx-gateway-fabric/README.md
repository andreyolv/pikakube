[← Gateway API](../README.md)

# NGINX Gateway Fabric

<https://github.com/nginx/nginx-gateway-fabric>
<https://docs.nginx.com/nginx-gateway-fabric/>

Context and comparison: [../README.md](../README.md)

---

## What it is

NGINX's implementation of the [Gateway API](../README.md) — the same data path teams already
know, driven by the new resource model instead of `Ingress` annotations.

It is a **third, separate** NGINX project in this repository:

| Project | Folder | API |
|---|---|---|
| `kubernetes/ingress-nginx` | [`ingress-controller/ingress-nginx/`](../../ingress-controller/ingress-nginx/) | `Ingress` |
| `nginx/kubernetes-ingress` | [`ingress-controller/nginx-ingress/`](../../ingress-controller/nginx-ingress/) | `Ingress` + own CRDs |
| **`nginx/nginx-gateway-fabric`** | here | **Gateway API** |

Different codebases with different behaviour. Only the proxy is shared.

## When to use it

- adopting the Gateway API and wanting **NGINX** rather than Envoy as the data path
- the team's operational knowledge is NGINX and should carry over

## When not to use it

- Envoy is acceptable — [Envoy Gateway](../envoy-gateway/) is closer to the reference implementation and moves faster
- you are staying on `Ingress`

---

[← Gateway API](../README.md)
