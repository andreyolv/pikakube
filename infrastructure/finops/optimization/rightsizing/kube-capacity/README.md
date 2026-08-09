[← Right-sizing](../README.md)

# kube-capacity

<https://github.com/robscott/kube-capacity>

---

## The problem it solves

[`../README.md`](../README.md#1-why-this-is-the-biggest-lever) makes the case that over-requesting
is invisible: no throttling, no eviction, no alert, no failing probe. It surfaces **only if somebody
deliberately compares requests against usage.**

kube-capacity is that comparison, as one command.

`kubectl top` shows usage. `kubectl describe node` shows requests and limits. Neither shows them
together, and the gap between them is the entire subject of this folder.

```
kube-capacity --util --pods

NODE           NAMESPACE   POD          CPU REQUESTS   CPU LIMITS   CPU UTIL   MEMORY REQUESTS   MEMORY LIMITS   MEMORY UTIL
node-1         *           *            1200m (60%)    2000m (100%) 85m (4%)   3Gi (48%)         5Gi (80%)       1Gi (16%)
node-1         kafka       kafka-0      500m (25%)     1000m (50%)  22m (1%)   2Gi (32%)         2Gi (32%)       600Mi (9%)
```

The `CPU REQUESTS 60%` against `CPU UTIL 4%` on the first line is the finding. That node is 60%
reserved and 4% busy, and nothing in Kubernetes was ever going to mention it.

## Why it belongs in this folder rather than in observability

Every other tool here **recommends** or **enforces**. This one only **shows**, and that is its
argument:

| Tool | What it does | Needs |
|---|---|---|
| **kube-capacity** | shows the current gap | metrics-server |
| [krr](../krr/README.md) | recommends values from **history** | Prometheus |
| [goldilocks](../goldilocks/README.md) | recommends, via VPA, with a dashboard | VPA installed |
| [vpa](../vpa/README.md) | **changes** requests | a controller, and a decision about mode |
| [stormforge](../stormforge/README.md), [perfectscale](../perfectscale/README.md) | recommend and act, as a product | a commercial relationship |

That makes it **the zero-commitment entry point**. Before installing a controller or wiring up
Prometheus history, one binary answers whether there is a problem worth solving — and how large it
is.

If requests and usage are already close, the rest of this folder is not needed. That is a genuinely
useful answer to get in ten seconds.

## When to use it

- **first**, before adopting anything else here — establish whether the gap exists
- during an incident, to answer "why will nothing schedule on this node" with `--available`
- reviewing a namespace before setting a `ResourceQuota` or a `LimitRange`
- checking a specific workload after changing its requests, without waiting for a dashboard
- explaining the problem to someone — the output is a table, not a graph to interpret

## When not to use it

- **as the basis for setting requests.** It is a point-in-time snapshot; a value chosen from one
  observation will be wrong at the next traffic peak. Requests come from **history** —
  [krr](../krr/README.md) or [goldilocks](../goldilocks/README.md)
- for tracking over time or alerting — that is
  [`observability/metrics/`](../../../../observability/metrics/README.md)
- as an enforcement mechanism; it changes nothing
- without metrics-server, in which case the utilisation columns are simply absent

## The flags that matter

| Flag | What it gives you |
|---|---|
| **`--util`** / `-u` | the utilisation columns — **without this it shows only requests and limits**, which is half the point |
| `--pods` / `-p` | break down by pod, not just node |
| `--containers` / `-c` | further, to the container |
| **`--available`** / `-a` | what is left schedulable — the answer to "why is nothing scheduling" |
| `--sort` | order by the column that matters; sorting by CPU or memory request finds the offenders |
| `--output` | `table`, `json`, `yaml` — the non-table formats are what make it scriptable |
| `--namespace` | scope it |
| `--pod-labels`, `--node-labels`, `--namespace-labels` | filter by label, which is how you scope it to a team |
| `--node-taints`, `--no-taint` | see or exclude tainted nodes |
| `--hide-limits`, `--hide-requests` | narrow the table when it is too wide to read |

**`--util` is the one to remember.** The default output shows requests and limits only, which is
information `kubectl describe node` already had. The utilisation column is what turns it into a
right-sizing tool.

The `--output json` path is worth knowing separately: it makes this scriptable, so "report the ten
worst requests-to-usage ratios" is a pipeline rather than an eyeball exercise.

## Installing it

```bash
# Homebrew
brew tap robscott/tap && brew install robscott/tap/kube-capacity

# krew
kubectl krew install resource-capacity
```

**The krew plugin is named differently from the binary.** Installed through krew it is invoked as
`kubectl resource-capacity`, not `kube-capacity` — which is a small thing that wastes ten minutes
the first time. Binaries are also published on the releases page.

## Notes

Added to the catalogue from <https://github.com/robscott/kube-capacity>. Apache 2.0, from Rob Scott,
around 2.7k stars.

Worth checking release activity before relying on it for anything scripted: the author's main work
is elsewhere in the Kubernetes ecosystem, and the project has the shape of a stable, complete tool
rather than an actively developed one — which for a read-only CLI is closer to a feature than a
risk, but is the kind of thing to confirm rather than assume.

**Where this lands for pikakube.** It is the tool to reach for **first** in this folder, and it costs
nothing: no controller, no Prometheus, no commitment. The only dependency is
[metrics-server](../../../../observability/metrics/collector/metrics-server/README.md), which is
already mapped in this repository.

It also serves a purpose the rest of the folder does not, and one that matters on a
[Kind](../../../../platform-engineering/kubernetes/local/README.md) cluster specifically: on a
single-node local cluster, "nothing will schedule" is a routine occurrence, and `--available`
answers why in one command instead of by reading events.

The sequence this folder implies:

1. **kube-capacity** — is there a gap, and how big
2. [krr](../krr/README.md) or [goldilocks](../goldilocks/README.md) — what should the values be,
   from history
3. [vpa](../vpa/README.md) — should anything apply them automatically, and in which mode

Skipping step 1 is how teams install a recommender to discover their requests were already
reasonable.

---

[← Right-sizing](../README.md)
