[← Metrics collectors](../README.md)

# prometheus-adapter

<https://github.com/kubernetes-sigs/prometheus-adapter>

---

## The problem it solves

The HPA reads from **Kubernetes metrics APIs**, not from Prometheus. So a metric already in
Prometheus — queue depth, requests per second, lag — cannot drive autoscaling, even though the
number exists.

prometheus-adapter bridges that: it runs PromQL and serves the results through the
`custom.metrics.k8s.io` and `external.metrics.k8s.io` APIs, so an HPA can scale on anything
Prometheus knows.

It can also replace [metrics-server](../metrics-server/) for the resource metrics API, serving
CPU and memory from Prometheus instead — which removes one component when Prometheus is
already scraping cAdvisor.

## When to use it

- autoscaling on a metric that is **not** CPU or memory, and Prometheus already has it
- you want one source of truth for metrics, including for autoscaling decisions
- HPA specifically is the mechanism you are using

## When not to use it

- **event-driven scaling** — [KEDA](../../../../devops/event-driven/keda/) covers the same
  ground with prebuilt scalers for Kafka, RabbitMQ, SQS, cron and dozens more, plus
  scale-to-zero, which the HPA cannot do
- only CPU-based autoscaling is needed — metrics-server is simpler

## KEDA or prometheus-adapter

| | prometheus-adapter | KEDA |
|---|---|---|
| Source | Prometheus only | Prometheus, Kafka, RabbitMQ, SQS, cron, and many more |
| Scale to zero | no | yes |
| Configuration | query rules mapping PromQL to metric names | a `ScaledObject` per workload |
| Fits | one metrics source, HPA-centric | event-driven workloads |

For a data platform, KEDA is usually the better fit — scaling consumers on queue depth and to
zero between batches is exactly its shape. prometheus-adapter is the right answer when
Prometheus is genuinely the only source and the HPA is the mechanism.

---

[← Metrics collectors](../README.md)
