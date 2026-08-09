[← Ingress controller](../README.md)

# NGINX Ingress Controller (F5 / NGINX Inc)

<https://github.com/nginx/kubernetes-ingress>
<https://docs.nginx.com/nginx-ingress-controller/>

Context and comparison: [../README.md](../README.md)

---

> **Not the same as [ingress-nginx](../ingress-nginx/README.md).** That one is the Kubernetes
> community controller. This is F5/NGINX Inc's, with a different codebase and a different
> annotation set. Manifests written for one do not work on the other.

## The problem it solves

The same job — reading `Ingress` objects and configuring NGINX — from the vendor that makes
NGINX. What it adds over the community controller:

- **commercial support**, and a path to NGINX Plus features
- **its own CRDs** (`VirtualServer`, `VirtualServerRoute`) as an alternative to annotation soup
- **App Protect** WAF integration on the Plus tier

## When to use it

- there is an **NGINX Plus or F5 support contract**, or one is wanted
- you prefer typed CRDs over annotations and are not yet moving to the [Gateway API](../../gateway-api/README.md)

## When not to use it

- no commercial requirement — [ingress-nginx](../ingress-nginx/README.md) has far more community material, and most answers you find online assume it

---

## Notes

Extracting the CRDs, if you want them split per file:

```bash
kubectl create -f "https://raw.githubusercontent.com/nginx/kubernetes-ingress/v4.0.0/deploy/crds.yaml" --dry-run=client -o yaml | kubectl-slice -f - -o ./crds --template '{{.spec.names.plural}}.yaml'
```

> The CRDs do **not** need to be applied beforehand — the Helm chart handles them.

---

[← Ingress controller](../README.md)
