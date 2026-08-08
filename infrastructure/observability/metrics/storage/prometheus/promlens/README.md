[← Prometheus](../README.md)

# PromLens

<https://github.com/prometheus/promlens>

---

## The problem it solves

PromQL is easy to start with and hard to debug. A query returns nothing, or returns the wrong
shape, and the expression bar gives no clue which part is at fault.

PromLens breaks a query into a **tree** and shows the intermediate result at every node. You
can see exactly where the series disappeared — a label match with a typo, a `rate()` window
shorter than the scrape interval, a join that dropped everything.

## When to use it

- writing or debugging non-trivial PromQL
- **teaching** — the tree view makes the structure of a query legible in a way the expression bar does not
- understanding an inherited alert rule nobody can explain any more

## When not to use it

- simple queries, where Grafana's explore view is enough
- as a permanent exposed service; it is a development tool, not part of the monitoring path

## The two failures it explains fastest

**Label mismatch in a join.** Two metrics with almost-matching labels produce an empty result
and no error. The tree shows both sides, and the difference becomes obvious.

**`rate()` window too short.** A window smaller than two scrape intervals silently yields
nothing. The tree shows the raw selector returning data and the `rate()` returning nothing —
which points straight at the cause.

Both are common, both look like "the metric does not exist", and both are hard to see any
other way.

---

[← Prometheus](../README.md)
