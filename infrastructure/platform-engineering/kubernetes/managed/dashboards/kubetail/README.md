[← Dashboards](../README.md)

# Kubetail

<https://github.com/kubetail-org/kubetail>

---

## The problem it solves

`kubectl logs` handles one pod. `kubectl logs -l` handles a few, badly — it will not follow more than
five by default, output from different pods is indistinguishable, and a pod restarting mid-stream
ends the follow.

Kubetail is a web interface for tailing logs across many pods at once: select by workload, namespace
or label, see which pod each line came from, filter live, and keep following as pods come and go
during a rollout.

Notably it is **not a log store**. There is no ingestion pipeline and no retention — it reads from
the Kubernetes API in real time, exactly as `kubectl logs` does. That makes it trivial to run and
useless for anything historical.

## When to use it

- Watching a rollout across many replicas, live
- Following one logical service whose pods are being replaced underneath you
- A cluster with no log aggregation, where this is the pragmatic stopgap
- Developers who want log access without cluster CLI access

## When not to use it

- Anything historical — logs are gone when the pod is; use [`observability/`](../../../../../observability/README.md)
- Search across time or aggregation; it filters a live stream, nothing more
- Compliance or audit retention
- As a reason to postpone real log aggregation

## Notes

**Chart** `kubetail` version `0.13.4` from `https://kubetail-org.github.io/helm-charts`, with a
namespace manifest. No notes were recorded — a wired-up chart.

Two points worth adding, because they decide whether it is the right tool:

- **The value is the multi-pod follow.** `kubectl logs -l app=x --max-log-requests 8 -f` — the idiom
  recorded in [`core/`](../../core/README.md) — is the CLI equivalent, and hitting the
  `--max-log-requests` limit is precisely the moment Kubetail starts to look worthwhile.
- **It needs pod log read access cluster-wide** to be useful, which is a meaningful grant: pod logs
  routinely contain tokens, connection strings and personal data. A UI that makes every log in the
  cluster browsable is a data-access decision, not a convenience.

The clean way to think about the boundary: Kubetail replaces `kubectl logs`, not Loki. If the
question is "what is happening right now", it is the right tool; if it is "what happened", nothing
in this folder can answer it.

---

[← Dashboards](../README.md)
