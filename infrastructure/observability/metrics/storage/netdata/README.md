[← Metrics storage](../README.md)

# Netdata

<https://github.com/netdata/netdata>
<https://learn.netdata.cloud/>

---

> **A different shape from the others in this folder.** Netdata is per-node, real-time
> monitoring with its own UI — not a cluster-wide time-series database. It is not an
> alternative to [Prometheus](../prometheus/README.md).

## The problem it solves

Install an agent and get **per-second** metrics with dashboards already built, from
auto-detected sources — the OS, containers, databases, web servers — with no configuration and
no dashboard authoring.

Two things it does that a Prometheus stack genuinely does not:

- **one-second resolution.** Prometheus typically scrapes every 15–30 seconds, which averages away short spikes entirely. Netdata sees them.
- **zero setup to useful.** Detection, collection and dashboards arrive together. There is no gap between installing it and having something to look at.

## When to use it

- looking closely at **one machine, right now** — a node behaving strangely, and 30-second averages are hiding the cause
- a quick view on a system with no monitoring at all
- short-lived spikes that scrape-interval monitoring cannot resolve

## When not to use it

- as the cluster's metrics system. There is no PromQL, no cross-cluster query, and the
  ecosystem of alert rules and dashboards assumes Prometheus
- long retention or historical analysis — it is oriented to the recent window at high
  resolution, which is the opposite trade
- as an alerting foundation; that belongs with [Prometheus](../prometheus/README.md) and
  [Alertmanager](../../../alerting/alertmanager/README.md)

## The honest framing

Best understood as a **diagnostic tool that happens to be always on**, rather than a
monitoring platform. It can export to Prometheus, which is the sensible arrangement if both
are wanted: Netdata for high-resolution local inspection, Prometheus for the cluster-wide,
long-lived, alertable view.

---

[← Metrics storage](../README.md)
