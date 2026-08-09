[← Network monitoring](../README.md)

# Zabbix

<https://github.com/zabbix-community/helm-zabbix>
<https://www.zabbix.com/documentation/current/en>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

A general-purpose infrastructure monitoring platform — servers, network devices, databases,
applications — with its own agents, templates, alerting and UI.

In a Kubernetes context it answers an **organisational** question rather than a technical
one: *how does this cluster appear inside the monitoring system the company already
operates?* Many infrastructure and network teams have run Zabbix for years across switches,
firewalls and VMs, and a new cluster is expected to report into it like everything else.

## When to use it

- Zabbix is **already** the organisation's monitoring standard, and the cluster must not be an exception
- the same team watches network hardware and the cluster, and wants one console
- there are non-Kubernetes systems in scope that Prometheus does not cover well

## When not to use it

- Prometheus is already the standard in the cluster — running both means two stacks, two alert definitions and two on-call surfaces
- what you want is **cluster-internal path probing**; that is [kubenurse](../kubenurse/README.md), and it is not what Zabbix is for

## The honest framing

This is rarely a technical decision. If the company runs Zabbix, integrating is cheaper than
arguing. If it does not, adopting it alongside Prometheus is a cost with no matching benefit.

---

[← Network monitoring](../README.md)
