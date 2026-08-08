[← Static IP](../README.md)

# kubeip

<https://github.com/doitintl/kubeip>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

Nodes get whatever public IP the cloud hands out, and it changes whenever a node is
replaced, scaled or recycled. That breaks any integration where the other side has
allow-listed your addresses.

kubeip watches nodes as they join and **assigns reserved static IPs** from a pool you
control, so the set of addresses the cluster can appear from stays known and finite — and
therefore allow-listable.

## When to use it

- a partner, bank, legacy system or managed database allow-lists your egress addresses
- nodes are recycled often — spot instances, autoscaling, frequent upgrades — and the address churn is the actual problem
- you need traffic to come from a **specific** address rather than merely a stable one

## When not to use it

- a **NAT gateway with a reserved address** is available and sufficient — that is simpler, managed, and solves the same problem for all egress at once
- nothing outside the cluster cares where traffic comes from, which is the common case

## Worth checking first

```bash
# from inside a pod: what does the outside world currently see?
curl ifconfig.me
```

If that already returns a stable NAT gateway address, the problem is solved and this tool
adds nothing.

---

[← Static IP](../README.md)
