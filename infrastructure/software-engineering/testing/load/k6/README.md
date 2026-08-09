[← Load testing](../README.md)

# k6

<https://github.com/grafana/k6>
<https://github.com/grafana/k6-operator>
<https://github.com/grafana/xk6-python>

---

## The problem it solves

**A load test that is a pass or a fail, and a Kubernetes resource rather than a machine someone
maintains.**

k6 is a single Go binary that runs test scripts written in JavaScript. Two properties make it the
default choice for a platform:

**Thresholds.** A k6 script declares its own pass condition — `p(95)<300`, `http_req_failed<0.01` —
and the binary exits non-zero when it is not met. That is what turns a load test from a report
somebody interprets into a pipeline stage that fails the build. It is the direct answer to the
problem in [`load/`](../README.md) section 1: a number with no target means nothing.

**The k6-operator.** Distributed load generation normally means provisioning machines, distributing
the script and aggregating the results. The operator makes it a CRD: apply a `TestRun`, and the
operator creates runner pods, splits the load across them, and collects the output. The test becomes
a file in git like everything else here.

The engine is Go, so per-virtual-user cost is low — one modest pod holds a lot of concurrent users —
and the binary has no runtime to install.

## When to use it

- **HTTP load tests in CI**, with a threshold derived from an SLO
- **distributed runs on Kubernetes**, via the operator
- a Grafana-based platform — output goes where the dashboards already are
- soak, stress and spike runs driven by staged ramps in the script
- anywhere a low-footprint, single-binary generator matters

## When not to use it

- **the scenario needs real libraries** — k6 scripts are JavaScript on a Go engine, not Node; there
  is no `npm install`, and anything beyond the k6 APIs needs an xk6 extension compiled in. Use
  [Locust](../locust/README.md) when the load generation itself needs an SDK or a client library.
- a **live web UI during the run** — k6 reports to the terminal or to a backend; Locust has one
  built in
- **browser-level testing** — k6 has a browser module, but end-to-end journeys belong in
  [`web-scraping/`](../../../web-scraping/README.md) tools
- functional API testing — that is [`api/`](../../api/README.md)
- as a substitute for defining the SLO first —
  [`service-level/`](../../../../site-reliability-engineering/service-level/README.md)

## Notes

Three links were recorded, and each is a separate point:

**<https://github.com/grafana/k6>** — the tool itself. Originally Load Impact's k6, now Grafana's,
which is why its output integrates with the rest of the Grafana stack:
[metrics](../../../../observability/metrics/README.md) and
[dashboards](../../../../observability/dashboards/grafana/README.md).

**<https://github.com/grafana/k6-operator>** — the Kubernetes operator, and the reason k6 is the tool
deployed in this repository rather than merely documented. It introduces the `TestRun` custom
resource, splits a run across `parallelism` runner pods, and takes the script from a `ConfigMap`.
Without it, distributed load generation is infrastructure somebody has to own.

**<https://github.com/grafana/xk6-python>** — an **xk6 extension that allows k6 scripts to be written
in Python**. xk6 is k6's extension mechanism: extensions are compiled into a custom k6 binary, so
using one means building and distributing that binary rather than using the released one. This
extension is worth knowing about precisely because the JavaScript-only scripting model is k6's main
limitation against [Locust](../locust/README.md) — it narrows the gap, at the cost of a custom
build.

**What is deployed here:**

| Manifest | Detail |
|---|---|
| `namespace.yaml` | namespace `k6` |
| `helm/helmrepository.yaml` | Flux `HelmRepository` for `grafana`, in `flux-system` |
| `helm/helmrelease.yaml` | chart `k6-operator`, **version 3.10.1**, 5m reconcile interval |
| `example/testrun.yaml` | a sample `TestRun` |

The sample `TestRun` is the useful documentation of the model: `parallelism: 4` spreads the run over
four runner pods, `separate: false` keeps them schedulable together, the script comes from a
`ConfigMap` named `k6-test` (file `test.js`), and both the **runner** and the **starter** carry their
own `securityContext` (`runAsNonRoot`, explicit UID/GID) and CPU/memory requests and limits. The
image fields are placeholders — `<custom-image>` — so it is a template rather than a working run.

Two things to be deliberate about when using it:

- **`parallelism` splits the load, it does not multiply it.** The script's total virtual users are
  divided across the runners.
- **Watch the runners' own CPU.** The most common invalid load test is one where the generator
  saturates before the target does; the resource limits in the sample are small, and a real run
  needs them sized against the load.

---

[← Load testing](../README.md)
