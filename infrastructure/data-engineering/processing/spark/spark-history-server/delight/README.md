[← History server](../README.md)

# Delight

<https://github.com/datamechanics/delight>

---

## What it adds

A free hosted alternative to the Spark UI, with the thing the standard one lacks: **CPU and
memory metrics overlaid on the job timeline**.

The standard [history server](../spark-history-server/README.md) shows what Spark did — stages, tasks,
shuffle. It does not show how much of the requested resources were actually used, which is the
information needed to right-size executors.

Delight puts both on the same timeline, which makes over-provisioning visible rather than
theoretical.

## When it is useful

- **right-sizing executors** — seeing that a job requested 8 GB and used 2 GB
- correlating a slow stage with resource saturation rather than guessing
- a nicer UI than the standard history server, at no cost

## When not to use it

- **event data leaves your environment.** It is hosted, and the agent uploads job telemetry. That includes the plan and configuration, which can be sensitive
- self-hosted only is a requirement — use the [history server](../spark-history-server/README.md)
- see the note below

---

## Notes

> The authentication is very poor.

Worth evaluating before adopting it for anything beyond experimentation — for a hosted service
receiving job telemetry, the access model is the first thing that should be solid.

## The alternative

For resource metrics without sending data anywhere:
[spark-dashboard](../../spark-performance/spark-dashboard/README.md) collects Spark metrics into
Prometheus and Grafana, which puts the same information next to the rest of the platform's
[observability](../../../../../observability/README.md) — self-hosted, and correlated with
everything else.

---

[← History server](../README.md)
