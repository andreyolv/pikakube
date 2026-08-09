[← Dashboards](../README.md)

# Grafana

<https://github.com/grafana/grafana>
<https://grafana.com/docs/grafana/latest/>

Deployment: [`grafana-operator/`](grafana-operator/README.md) — the declarative, GitOps-friendly way
to run it.

---

## The problem it solves

Signals live in different systems — metrics in Prometheus, logs in Loki, traces in Tempo,
profiles in Pyroscope. Grafana is the layer that queries all of them and puts the results on
one page.

That datasource-agnosticism is the actual product, and the reason it won: you are not
choosing a UI for one backend, you are choosing the one place people look regardless of what
is underneath.

Practical consequences:

- **correlation across signals** — a latency spike on a graph links straight to the traces behind it
- **an enormous community dashboard library**, so most components come with one already written
- alerting exists in Grafana too, though [Alertmanager](../../alerting/alertmanager/README.md) remains the standard when Prometheus is the source

## When to use it

- effectively always, when there is more than one datasource
- the team expects to find dashboards where everyone else's are

## When not to use it

- you want dashboards to be **entirely** declarative and lightweight, with no UI-first path at all — [Perses](../perses/README.md) is designed for that
- the only requirement is one panel for one metric, where Grafana is more than the job needs

## Related in this repo

Grafana's storage components are filed by signal rather than by vendor:
[Loki](../../logs/storage/loki/README.md) · [Tempo](../../tracing/storage/tempo/README.md) ·
[Mimir](../../metrics/long-term-storage/mimir/README.md) · [Pyroscope](../../profiling/pyroscope/README.md) ·
[Alloy](../../tracing/collector/alloy/README.md) · [Beyla](../../tracing/instrumentation/auto-ebpf/beyla/README.md) ·
[Faro](../../frontend/faro/README.md)

---

[← Dashboards](../README.md)
