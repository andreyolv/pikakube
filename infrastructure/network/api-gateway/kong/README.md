[← API gateway](../README.md)

# Kong

<https://github.com/Kong/kong>
<https://github.com/Kong/charts>
<https://docs.konghq.com/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

The most widely adopted open-source API gateway. Built on NGINX/OpenResty, with the largest
plugin ecosystem of anything in this folder — authentication, rate limiting, transformation,
logging, tracing — configurable per route and **per consumer**.

The consumer model is the point: `KongConsumer` and `KongPlugin` let a limit or a credential
apply to a specific caller, which is exactly what an ingress controller cannot express.

## When to use it

- you need API management and want the option with the most examples, plugins and hiring pool
- per-consumer credentials and quotas are a real requirement
- you want to extend behaviour with plugins rather than modify backends

## When not to use it

- there are no external API consumers — an [ingress controller](../../ingress-controller/README.md) does the routing with far less to operate
- you want a developer portal and per-plan analytics out of the box; [Tyk](../tyk/README.md) includes more of that in its open-source tier

## Kubernetes

Configuration from cluster objects comes from the separate Kong Ingress Controller:
[`ingress-controller/kong-ingress/`](../../ingress-controller/kong-ingress/README.md)

---

## Notes

- Kind setup: <https://github.com/arthurbdiniz/kind-kong>
- [Using the KongPlugin resource](https://docs.konghq.com/kubernetes-ingress-controller/2.11.x/guides/using-kongplugin-resource/)

```bash
curl -I "http://httpbin.local.172.18.0.2.nip.io/headers"
```

UI: [`konga/`](konga/README.md) — archived, see its README before using it.

---

[← API gateway](../README.md)
