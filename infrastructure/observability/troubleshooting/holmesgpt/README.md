[← Troubleshooting](../README.md)

# HolmesGPT

<https://github.com/robusta-dev/holmesgpt>

---

## The problem it solves

An alert fires and triage begins: pull the logs, read the events, check what deployed, look
at the relevant metrics, form a hypothesis. Fifteen minutes of mechanical work before anyone
starts thinking.

HolmesGPT does that gathering automatically. It connects to the sources — Prometheus, logs,
Kubernetes, and more — collects what is relevant to the specific alert, and proposes a root
cause with the evidence attached.

Its differentiator over a plain scanner is **investigating a specific alert** rather than
reporting everything that looks wrong.

## When to use it

- alert volume is high enough that initial triage is the bottleneck
- responders repeatedly gather the same context by hand
- you already run [Robusta](../../alerting/robusta/) — same project, and they compose

## When not to use it

- cluster data cannot go to an external model without review. It reads logs, and logs carry credentials and personal data more often than expected — check whether a local model is viable
- the answer is expected to be authoritative. Treat the output as a hypothesis with evidence, never as a conclusion

## The realistic value

It is very good at the recurring, boring causes, which are most incidents by count. It is
confidently unreliable on anything novel — and a plausible wrong hypothesis costs more than
none, because people follow it.

Used as "here is where to look first", it saves real time. Used as "here is the answer", it
eventually causes an outage extension.

---

[← Troubleshooting](../README.md)
