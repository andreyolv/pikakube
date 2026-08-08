[← eBPF platforms](../README.md)

# Coroot

<https://github.com/coroot/coroot>
<https://github.com/coroot/helm-charts>

---

## The problem it solves

Deploy an agent and get a **working service map with golden signals**, for applications
nobody instrumented. Coroot derives the dependency graph, latency, error rates and resource
attribution from eBPF alone.

What sets it apart from the others here is that it goes past the map into **interpretation**:
it flags likely causes, tracks SLO-style objectives per service, and attributes cloud cost to
workloads.

## When to use it

- an existing system with no instrumentation and no realistic path to adding it soon
- you want the dependency graph as it actually is, not as the diagram claims
- a small team that wants coverage without an instrumentation project

## When not to use it

- you need business context inside requests — eBPF stops at the process boundary
- Prometheus and Grafana are entrenched and working
- kernel versions across the fleet are old or inconsistent

## The honest positioning

The most complete open-source option in this folder, and the best answer to "we have no
observability and cannot instrument right now". It is a strong starting point, and it does not
remove the eventual need to instrument what matters.

---

[← eBPF platforms](../README.md)
