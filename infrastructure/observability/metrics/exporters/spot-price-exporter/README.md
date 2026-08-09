[← Exporters](../README.md)

# Spot Price Exporter

<https://github.com/banzaicloud/spot-price-exporter>
<https://github.com/banzaicloud/banzai-charts/tree/master/spot-price-exporter>

---

## The problem it solves

Spot instance prices move by region, availability zone and instance type. That variation is
the difference between a good spot strategy and a bad one, and it is invisible from inside the
cluster.

This exports current spot prices as Prometheus metrics, so the pricing landscape can be
graphed, compared and alerted on alongside everything else.

## When to use it

- a spot strategy exists and instance type or zone selection should be informed by data
- validating that [Karpenter](../../../../finops/README.md) or an autoscaler is choosing what you expect
- watching for price spikes that make the current selection uneconomical

## When not to use it

- no spot instances in use
- the interest is interruptions rather than price — that is [spot-termination-exporter](../spot-termination-exporter/README.md)
- Karpenter already handles selection well and nobody will act on the data

## Note on the project

Banzai Cloud is no longer active in the form it was. Check current maintenance status before
depending on it — cloud pricing APIs change, and a stale exporter reports stale prices, which
is worse than none.

## Related

[`finops/`](../../../../finops/README.md) covers the spot strategy itself, including Karpenter and the
consolidation behaviour that makes spot viable in the first place.

---

[← Exporters](../README.md)
