[← API gateway](../README.md)

# Easegress

<https://github.com/easegress-io/easegress>
<https://megaease.com/docs/easegress/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

A traffic orchestrator written in Go, positioned as a **lighter and more programmable**
alternative to the larger gateways in this folder.

Its model is a pipeline of filters composed per route, which makes behaviour explicit rather
than implied by a plugin's defaults. It also covers things the others treat as separate
products — a degree of service discovery, resilience patterns such as circuit breaking and
retries, and canary routing.

## When to use it

- you want an API gateway without the operational weight of Kong, Tyk or an Envoy control plane
- the pipeline model fits how you think about request handling
- resilience patterns are wanted at the edge without adding a service mesh

## When not to use it

- you need an ecosystem — plugins, integrations, documented answers and people who have used it. That is [Kong](../kong/) or [APISIX](../apisix/)
- API management proper — consumers, plans, portal — is the requirement

## The honest framing

The smallest and least widely deployed option here. That is a genuine advantage when the
requirement is modest and the team wants something they can reason about completely, and a
genuine risk when a problem arises and there is little written about it.

---

[← API gateway](../README.md)
