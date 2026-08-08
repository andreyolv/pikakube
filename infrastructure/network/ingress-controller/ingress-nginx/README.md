[← Ingress controller](../README.md)

# ingress-nginx

<https://github.com/kubernetes/ingress-nginx>
<https://kubernetes.github.io/ingress-nginx/>

Context and comparison: [../README.md](../README.md)

---

> **Not the same as [nginx-ingress](../nginx-ingress/).** This is the **Kubernetes community**
> controller (`kubernetes/ingress-nginx`). The other is F5/NGINX Inc's
> (`nginx/kubernetes-ingress`). Different codebases, different annotations — manifests do not
> transfer.

## The problem it solves

`Ingress` objects do nothing on their own. This controller reads them, configures NGINX, and
becomes the actual data path: TLS termination, host and path routing, and the wide set of
behaviours exposed through annotations.

It is **the default choice** — the most deployed and most documented controller, which means
almost every problem you hit already has an answer written down.

## When to use it

- you want the safest, best-documented option
- the team knows NGINX
- annotations cover the requirement — rate limiting, auth, rewrites, CORS

## When not to use it

- you need per-consumer quotas and API keys — that is [`api-gateway/`](../../api-gateway/README.md)
- you are adopting the [Gateway API](../../gateway-api/README.md) and want a native implementation

---

## Notes

### Kind

```
https://github.com/kubernetes/ingress-nginx/blob/main/hack/manifest-templates/provider/kind/values.yaml
https://github.com/kubernetes/ingress-nginx/blob/main/deploy/static/provider/kind/deploy.yaml
```

Port-forward and browse:

```bash
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80
```

<http://foo.127.0.0.1.nip.io:8080/>

### Generating certificates

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt

openssl req -x509 -newkey rsa:4096 -sha256 -nodes -keyout tls.key -out tls.crt -subj "/CN=seudominio.com" -days 365
```

### Converting from PFX

```bash
openssl pkcs12 -in [yourfile.pfx] -chain -clcerts -nokeys -out tls.crt
openssl pkcs12 -in [yourfile.pfx] -nocerts -out encrypted-key.key
openssl rsa -in encrypted-key.key -out tls.key

kubectl create secret tls [secret-name] --cert=tls.crt --key=tls.key --dry-run=client -o yaml > secret-name.yaml
```

For anything beyond a one-off, [cert-manager](../../../security/2-cluster/certificates/cert-manager/)
issues and renews these automatically.

### Fixing `certificate signed by unknown authority`

```bash
kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission
```

### Guides

- [OAuth external auth](https://kubernetes.github.io/ingress-nginx/examples/auth/oauth-external-auth/)
- [Rate limiting annotations](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#rate-limiting) — see also [`rate-llimit/`](rate-llimit/)
- [Local cluster with ingress](https://blog.lepape.me/local-kubernetes-cluster-with-ingress/)

---

[← Ingress controller](../README.md)
