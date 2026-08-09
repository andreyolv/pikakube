[← Config reload](../README.md)

# Reloader

<https://github.com/stakater/Reloader>

Recorded issue: <https://github.com/stakater/Reloader/issues/853>

---

## The problem it solves

A `ConfigMap` mounted as environment variables is read exactly once, when the container starts.
Update the ConfigMap and the running Pod keeps the old values, indefinitely, with no error and no
event. The cluster reports everything as healthy because by its own definition everything is.

Mounted as a volume the situation is only slightly better: the kubelet does eventually refresh the
file on disk, but nothing tells the application, so unless it watches the file itself the outcome
is the same.

Reloader watches ConfigMaps and Secrets and, when one changes, triggers a **rolling update** of the
workloads that consume it. It supports `Deployment`, `StatefulSet`, `DaemonSet`, `Rollout` and
`CronJob`.

The mechanism is the important part: it does not restart Pods directly. It patches an annotation
on the workload's **pod template**, which changes the template hash, which makes the Deployment
controller do what it always does — roll out new Pods and retire the old ones. Surge, maxUnavailable,
readiness gates and `PodDisruptionBudget` all apply, because from the cluster's point of view this
is an ordinary rollout.

### The annotations

| Annotation | Behaviour |
|---|---|
| `reloader.stakater.com/auto: "true"` | reload on a change to **any** ConfigMap or Secret this workload references |
| `configmap.reloader.stakater.com/reload: "name1,name2"` | reload only for the named ConfigMaps |
| `secret.reloader.stakater.com/reload: "name1,name2"` | reload only for the named Secrets |
| `reloader.stakater.com/search: "true"` on the workload, with `reloader.stakater.com/match: "true"` on the resource | opt-in from **both** sides — the resource declares itself reloadable and the workload declares itself searchable |

`auto` is the one to reach for by default. The `search`/`match` pair matters when a ConfigMap is
shared: it lets the owner of the ConfigMap decide whether changing it should be allowed to restart
other people's workloads.

## When to use it

- **the default answer in this folder.** Broad workload-kind coverage, one annotation, and the
  behaviour is easy to explain to someone reading the manifest
- applications that read configuration at startup and never again — which is most of them
- Secrets rotated by an external system (a certificate renewal, a rotated database credential)
  where the consuming Pods need to pick up the new value without a human running `kubectl rollout
  restart`
- when per-workload control over *which* ConfigMaps trigger a reload is needed

## When not to use it

- **if the application already watches its own configuration.** Many do — reverse proxies,
  collectors, most Go controllers. Restarting them on change is strictly worse than the hot reload
  they already implement
- for high-churn ConfigMaps. A resource updated every few minutes plus `auto` is a restart loop, and
  the workload will never be stable long enough to serve anything
- if what is really wanted is a `Deployment` whose spec changes when its configuration does —
  see [Wave](../wave/README.md), which encodes the configuration hash into the workload rather than
  reacting after the fact
- as a substitute for a rollout strategy. If restarting a workload is disruptive, Reloader will
  faithfully make it disruptive on every ConfigMap edit

## Notes

Two recorded references. The project, <https://github.com/stakater/Reloader>, and issue **#853**,
<https://github.com/stakater/Reloader/issues/853> — *"[ENHANCE] Dashboard"*, an open request for a
UI showing which workloads are being watched, recent reload events, counts of monitored ConfigMaps
and Secrets, and reload metrics. It is still open and unimplemented.

Why it is recorded here: it names the real operational gap. Reloader restarts things silently and
correctly, and there is no first-class way to see *what it is watching* or *why that Pod restarted
at 03:14*. Today the answers come from the controller's logs and its Prometheus metrics. If a
mysterious restart ever needs explaining, that is where to look, and the absence of anything better
is a known limitation rather than a misconfiguration.

**Deployed here**, via a Flux `HelmRelease` against the Stakater Helm repository.

**The with/without demonstration** is the most useful thing in this folder. Two identical Flask
Deployments sit side by side under `with/` and `without/`, both consuming a `ConfigMap`
(`database_url`) and a `Secret` (`db_password`) as environment variables. The only difference is
one annotation:

```
reloader.stakater.com/auto: "true"
```

Edit the ConfigMap and `flask-with` rolls; `flask-without` does not, and serves the old value until
someone notices. Both use `strategy: Recreate`, which makes the difference visible immediately
rather than blended into a rolling update. It is worth running once, because the failure this tool
prevents is otherwise invisible — the whole point is that nothing goes wrong loudly.

---

[← Config reload](../README.md)
