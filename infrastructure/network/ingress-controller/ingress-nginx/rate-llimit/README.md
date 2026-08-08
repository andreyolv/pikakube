[← ingress-nginx](../README.md)

# Rate limiting with ingress-nginx

Controller: [../README.md](../README.md)

---

## What it does, and what it does not

ingress-nginx rate-limits **per route**, through annotations — requests per second, per
minute, connections, and a burst multiplier.

That covers protecting a backend from overload. What it does **not** do is vary the limit by
caller: there is no notion of a consumer, a plan or a quota. "The free tier gets 100 and the
partner gets 10,000" is not expressible here — that is
[`api-gateway/`](../../../api-gateway/README.md).

Use this when the goal is **protection**. Use an API gateway when the goal is **entitlement**.

## Watching it work

```bash
kubectl logs -l app.kubernetes.io/component=controller -c controller -f --tail 100 | grep backstage
```

Rejected requests appear as `503` in the controller logs, which is how you confirm the limit
is firing rather than the backend failing on its own.

## References

- [Rate limit on specific APIs via ingress-nginx](https://milaan.hashnode.dev/rate-limit-in-specific-apis-via-nginx-ingress-controller)
- [Rate limiting in NGINX](https://blog.nginx.org/blog/rate-limiting-nginx)
- [`ngx_http_limit_req_module`](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)
- [Rate limiting by decoded JWT values](https://stackoverflow.com/questions/64263895/nginx-rate-limitting-by-decoded-values-from-jwt-token)

---

[← ingress-nginx](../README.md)
