[← OpenTelemetry platforms](../README.md)

# OpenObserve

<https://github.com/openobserve/openobserve>
<https://github.com/openobserve/openobserve-helm-chart>

---

## The problem it solves

An OTLP-native platform built around **storage efficiency**. Its pitch is a very large
reduction in storage cost compared to Elasticsearch for the same log volume, achieved by
writing Parquet to object storage instead of maintaining inverted indexes.

That trade is the whole design: cheaper storage and much lower operational weight, in exchange
for a query model that is scan-oriented rather than index-oriented.

It also runs as a **single binary**, which is a genuine difference from platforms that need
several components before ingesting anything.

## When to use it

- **log volume is the cost problem** and Elasticsearch has become expensive to run and store
- you want object storage as the backend rather than local disks to manage
- a small footprint matters — one binary, no cluster to operate

## What is not open source

**SSO (OIDC/SAML) and RBAC live in the Enterprise edition.** The open source edition gives you
local users and nothing else, so every operator gets a separate password in a system that holds
production logs. Putting authentication behind the paywall is ridiculous: it is not a premium
feature, it is the baseline for anything that runs in a company, and it turns an otherwise
cheap platform into a licensing conversation the moment more than one person needs access.

Worth knowing before adopting it — the storage economics are real, the access model is not.
[SigNoz](../signoz/README.md) plays the same game, slightly less aggressively: local users and
basic roles are included there, only SSO is paid.

## When not to use it

- **SSO is a hard requirement** and you are not paying for the Enterprise edition
- complex full-text search across huge datasets is the primary workload; index-based engines still win there
- you want the broadest feature surface — [SigNoz](../signoz/README.md) covers more
- you need Grafana's ecosystem as the front end

## Related

Compare against [Loki](../../../logs/storage/loki/README.md), which makes a similar bet — index only
labels, store the rest cheaply. The difference is scope: Loki is a log store, this is a
platform for all three signals.

---

[← OpenTelemetry platforms](../README.md)
