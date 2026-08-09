[← Troubleshooting](../README.md)

# stern

<https://github.com/stern/stern>

---

## The problem it solves

`kubectl logs` reads **one pod, one container**. A Deployment with five replicas means five
terminals, and the request you are chasing hit exactly one of them — you find out which by
opening all five and reading.

stern tails **many pods and containers at once**, into a single stream:

| What it adds | Why it matters during an incident |
|---|---|
| **Regex pod matching** — `stern api-` matches every pod whose name matches | you rarely know the pod hash, and you should not have to |
| **Label selection** — `-l app=checkout` | the same set the Service targets |
| **Colour per pod and container** | interleaved output from ten sources is unreadable without it |
| **Follows pods that appear later** | a rollout replaces every pod; the tail survives it |
| **Follows across restarts** | a CrashLoopBackOff keeps producing new containers to read |
| **`--since`, `--tail`** | start from the last ten minutes instead of the beginning |
| **Container selection** — `-c`, `--exclude-container` | drop the sidecar that drowns out the application |

`kubectl logs -l` exists and covers part of this, but it selects pods **once, at invocation**:
new pods and restarted containers are not picked up, there is no regex, and the output is
undifferentiated text. That gap is the whole reason stern is still installed.

## When to use it

- watching a rollout live — old pods draining, new pods starting, all in one stream
- a CrashLoopBackOff, where the interesting output is in a container that keeps being replaced
- reproducing a request against a multi-replica service without knowing which replica serves it
- correlating a few related workloads at once — `stern -A -l 'app in (api,worker)'`
- local and development clusters, where there is no log pipeline at all

## When not to use it

- **as a substitute for log storage.** stern reads through the kubelet, so it only sees what is
  still on the node. Logs vanish when the pod is deleted and when the container log rotates —
  a post-mortem the next morning has nothing to read. Storage and search live in
  [`observability/logs/`](../../logs/README.md), and the backends in
  [`logs/storage/`](../../logs/storage/README.md) — Loki, OpenSearch, Quickwit
- **for querying history.** There is no query language and no retention. Filtering happens on a
  live stream, once
- **for alerting.** Nothing here is evaluated or persisted; alerting needs
  [`observability/alerting/`](../../alerting/README.md) on top of stored data
- on a very large selection — every matched container is an open log request against the API
  server, and the useful signal drowns anyway

## Notes

```bash
stern api-                              # regex over pod names
stern -l app=checkout                    # label selector
stern . -n payments                      # everything in a namespace
stern -A -l app=api                      # across all namespaces
stern api- -c app --exclude-container istio-proxy
stern api- --since 10m --tail 100
stern api- -t                            # timestamps
```

Deployed **nowhere** — it is a CLI on the operator's machine and holds no state in the
cluster. It needs the same log-read permission `kubectl logs` needs, so anyone who can read
logs can already run it.

Two things worth internalising before relying on it:

> **The kubelet is the source, not a database.** Rotation is governed by the kubelet's
> `containerLogMaxSize` / `containerLogMaxFiles`, and deletion of a pod deletes its logs with
> it. "It was in stern an hour ago" is not a retrieval path.

> **It is a tail, not a search.** The right mental model is `tail -f` across a fleet. When the
> question is "what happened yesterday", the answer is in the logging pipeline or it does not
> exist.

Complements rather than replaces the rest of this folder: stern shows you the output,
[k8sgpt](../k8sgpt/README.md) tells you which objects are broken, and
[Inspektor Gadget](../inspektor-gadget/README.md) is for when the application never logged
the problem at all.

---

[← Troubleshooting](../README.md)
