[← DNS](../README.md)

# nip.io

<https://github.com/exentriquesolutions/nip.io>
<https://nip.io/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

A local cluster needs hostnames — for Ingress rules, for browsing to a service — and you do
not want to buy a domain, run a zone, or edit `/etc/hosts` on every machine.

nip.io is a public wildcard DNS service: **`<anything>.<ip>.nip.io` resolves to `<ip>`**,
with no registration and no configuration.

| Hostname | Resolves to |
|---|---|
| `airflow.127.0.0.1.nip.io` | `127.0.0.1` |
| `grafana.127.0.0.1.nip.io` | `127.0.0.1` |
| `anything.192.168.1.50.nip.io` | `192.168.1.50` |

Every subdomain works automatically, so adding a service needs no DNS step at all — and one
wildcard certificate for `*.127.0.0.1.nip.io` covers the whole cluster.

## When to use it

- local, ephemeral or demo clusters
- CI environments that need hostnames and are torn down afterwards
- you want zero setup and zero cost, and control is not the point

## When not to use it

Anything real. The limits are structural, not incidental:

| Limit | Consequence |
|---|---|
| You do not own the zone | **DNS-01 is impossible** — no public CA can ever issue for these names |
| It is a free third-party service | outages and rate limiting are outside your control, and it sits in your resolution path |
| Some resolvers reject it | DNS rebinding protection drops answers pointing at private IPs — the classic "works at home, fails on the office VPN" |

The first line is why a local cluster is **always** a private-CA scenario. See
[certificates](../../../security/2-cluster/certificates/README.md#3-public-ca-vs-private-ca).

## Alternatives

- **sslip.io** — same mechanism, different operator
- **`.test` names** with manual `/etc/hosts` entries — no third party, more setup
- **localtest.me** — resolves to `127.0.0.1` only

---

[← DNS](../README.md)
