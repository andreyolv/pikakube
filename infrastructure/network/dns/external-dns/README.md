[← DNS](../README.md)

# external-dns

<https://github.com/kubernetes-sigs/external-dns>
<https://kubernetes-sigs.github.io/external-dns/latest/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

Nothing in Kubernetes publishes anything to real DNS. You create an Ingress with a hostname,
and the outside world has no idea that name exists — someone still has to create the record
by hand, or open a ticket.

external-dns closes that gap. It watches `Ingress`, `Service` and `HTTPRoute` objects and
**writes records into your authoritative provider** — Route 53, Azure DNS, Cloud DNS,
Cloudflare, PowerDNS and others.

```yaml
metadata:
  annotations:
    external-dns.alpha.kubernetes.io/hostname: airflow.k8s.example.com
```

A new hostname stops being a ticket and becomes an annotation.

## When to use it

- you control a DNS zone, or have a **delegated subzone** — that delegation is what makes this worth deploying
- hostnames change often enough that manual records drift
- you want cert-manager to complete DNS-01 automatically, which needs records written without a human

## When not to use it

- there is no zone you control — on a local cluster, [nip.io](../nip.io/) answers by construction
- records are owned by another team and must stay under their change process

## The gotcha: TXT ownership records

external-dns writes a **TXT record alongside every entry it creates**, marking it as owned.
It will only ever modify records carrying that marker.

Delete those TXT records and it loses ownership — it then refuses to manage entries it
actually created, and they go stale silently. Leave them alone.

## Related

- getting a delegated subzone in a company: [../README.md](../README.md#7-in-a-corporate-environment)
- issuing certificates for the names it publishes: [cert-manager](../../../security/2-cluster/certificates/cert-manager/README.md)

---

[← DNS](../README.md)
