[← Kubernetes RBAC](../README.md)

# audit2rbac

<https://github.com/liggitt/audit2rbac>

---

## The problem it solves

**"Nobody knows the minimum permissions."**

This is the reason `cluster-admin` gets granted. A workload needs *some* set of API permissions,
and the only way to discover that set is empirically: deploy it, watch it fail with `Forbidden`,
add a rule, repeat. That loop is slow, it is done under time pressure, and it terminates the
moment someone grants `cluster-admin` "temporarily".

audit2rbac inverts it. Instead of guessing forward, it reads the **API server audit log** and
generates the exact `Role`, `ClusterRole` and bindings that would have permitted every request a
subject actually made:

```bash
# capture what the workload did, then:
audit2rbac -f audit.log --serviceaccount=namespace:my-sa > rbac.yaml
audit2rbac -f audit.log --user=alice@example.com > rbac.yaml
```

The output is real, applyable YAML — named, annotated with the generating command, and scoped to
exactly the verbs and resources that appeared. Nothing is inferred, nothing is padded, and no
wildcard is introduced.

Why this is the right shape of answer:

| | Guessing forward | audit2rbac |
|---|---|---|
| Source of truth | someone's mental model of the workload | **what the workload actually did** |
| Failure mode | too broad, because narrowing means another outage | too narrow, which fails loudly and is fixable |
| Effort | one `Forbidden` at a time | one command |
| Result | wildcards, because they end the loop | enumerated verbs and resources |

Its authorship is worth knowing: Jordan Liggitt, a Kubernetes maintainer deeply involved in the
API server's authentication and authorization. It is a small, focused tool by someone who knows
exactly what the audit log contains.

## When to use it

- **Replacing `cluster-admin` on an existing workload.** The single best use, and the reason the
  tool exists.
- **Writing RBAC for a new controller or operator you are building.** Run it against a
  permissive Role in a development cluster, exercise every code path, then generate the real
  one.
- **Auditing a third-party chart's claims.** Charts routinely request more than they use.
  Comparing the chart's ClusterRole against what audit2rbac generates from observed traffic
  shows the gap concretely.
- **Producing evidence for a review.** "Here is the minimal Role, derived from observed
  behaviour" is a much stronger position than "here is what I think it needs".
- **Understanding what something does.** The generated Role is a readable summary of a workload's
  entire API surface.

## When not to use it

- **API audit logging is not enabled.** There is no input, and nothing works. This is the hard
  prerequisite — see the Notes.
- **The workload has not exercised its rare paths.** This is the critical limitation:
  audit2rbac generates permissions for what happened, and **if a code path never ran, its
  permission is missing.** A failover routine, an upgrade migration, a cleanup that runs monthly,
  an error handler that deletes a resource — all invisible until they run and fail.
- **You need continuous enforcement.** It is a one-shot generator, not a controller. It does not
  watch, reconcile or alert.
- **You want to find risky permissions.** That is the opposite direction —
  [kubiscan](../kubiscan/README.md) analyses what is granted; audit2rbac synthesises what is
  needed.
- **The subject is a human.** People do unpredictable things, and a Role derived from one week of
  someone's activity will block them in week two. It works for workloads because workloads are
  deterministic.

The mitigation for the rare-path problem is procedural, not technical: run the workload long
enough to cover its real behaviour, deliberately exercise failure and upgrade paths, review the
generated Role against the workload's documentation, and treat the result as a strong starting
point rather than a final answer. Then keep audit logging on, so the next `Forbidden` is
diagnosable in seconds.

## Notes

**`https://github.com/liggitt/audit2rbac`** — the project, and the only note recorded for this
folder. Go, and distributed as a single binary; there is nothing to install into the cluster.

**No manifests are staged here**, and correctly so — audit2rbac is a CLI that runs against a log
file on your machine. It has no cluster-side component at all, which also means it is
**completely safe to try**: it reads a file and writes YAML to stdout.

### The prerequisite: API audit logging

Nothing here works without it, so it is worth stating what is involved.

The API server writes audit events only when started with `--audit-policy-file` and an audit
backend (`--audit-log-path` for a file). The policy file decides what is recorded, and the level
matters:

| Level | Records |
|---|---|
| `None` | nothing |
| `Metadata` | who, what, when, which resource — **this is what audit2rbac needs** |
| `Request` | the above plus the request body |
| `RequestResponse` | the above plus the response body |

`Metadata` is sufficient and is the right default: it is far smaller than the others and does not
capture Secret contents. This repository already has an audit policy under
`security/2-cluster/audit/`, which is where that configuration belongs.

On a Kind cluster, enabling it means patching the control-plane node's API server manifest
through the Kind cluster configuration — a cluster-creation concern rather than something a
manifest in this folder can do.

Worth connecting: this is the **accounting** half of AAA described in
[`identity-access/README.md`](../../../README.md). Turning it on for audit2rbac also turns on the
only detective control the cluster has, which is a better argument for it than RBAC generation
alone.

### The workflow in practice

1. Enable audit logging at `Metadata` level.
2. Deploy the workload with a deliberately permissive Role in a non-production cluster.
3. **Exercise it thoroughly** — normal operation, failure handling, upgrade, cleanup. This step
   is the whole quality of the result.
4. `audit2rbac -f audit.log --serviceaccount=ns:sa > rbac.yaml`
5. Read the output. Anything surprising in it is a finding about the workload, not about the
   tool.
6. Apply it, remove the permissive Role, and keep audit logging on so the next gap is obvious.

---

[← Kubernetes RBAC](../README.md)
