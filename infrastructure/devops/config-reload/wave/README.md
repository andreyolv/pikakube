[← Config reload](../README.md)

# Wave

<https://github.com/wave-k8s/wave>

---

## The problem it solves

The same problem as [Reloader](../reloader/README.md) — a ConfigMap or Secret changes and the Pods
consuming it carry on with the old values — solved from the opposite direction.

Reloader **reacts**: it notices a change and then patches the workload to force a rollout. Wave
**encodes**: it computes a hash of every ConfigMap and Secret the pod template references and writes
that hash into the pod template as an annotation:

```
wave.pusher.com/config-hash: <sha256 of the referenced configuration>
```

The consequence is that the workload's own spec now depends on its configuration. When the
configuration changes, the hash changes, the pod template changes, and the Deployment controller
rolls out — for exactly the same reason it rolls out when you change the image tag. There is no
special case and no out-of-band restart.

Wave is opt-in per workload, with:

```
wave.pusher.com/update-on-config-change: "true"
```

It supports `Deployment`, `StatefulSet` and `DaemonSet`, and it discovers the referenced resources
from the pod spec itself — `envFrom`, `valueFrom`, and volume mounts — so nothing has to be listed
twice.

It also sets an `OwnerReference` from the workload onto the ConfigMaps and Secrets it watches. That
is how it knows to re-evaluate when they change, and it has a side effect worth knowing: the
relationship becomes visible in `kubectl describe` on the configuration resource.

## When to use it

- when the **desired state should be self-describing** — someone reading the live Deployment can
  see, from the hash, whether it is running the current configuration or a stale one
- in a GitOps setup, where "the cluster matches the repository" is the property being asserted.
  A workload whose spec does not change when its configuration does is a hole in that property
- when reproducibility matters more than convenience: the same manifests plus the same ConfigMaps
  always produce the same pod template

## When not to use it

- **if broad coverage or per-resource control is the requirement.** Reloader handles more workload
  kinds and offers selective annotations; Wave is deliberately narrower
- for the same reasons as Reloader: applications that hot-reload their own configuration, and
  high-churn configuration that would produce a restart loop
- if the extra `OwnerReference` on shared ConfigMaps is unwelcome — on a resource consumed by many
  workloads it accumulates owners, which is harmless but noisy

## Notes

The only recorded reference is the repository: <https://github.com/wave-k8s/wave>.

The project began at Pusher, which is why the annotation prefix is still `wave.pusher.com` while
the repository now lives under the `wave-k8s` organisation. The chart is named `wave-k8s` for the
same reason — a detail that costs ten minutes if you go looking for a chart called `wave`.

**Deployed here**, via a Flux `HelmRelease` against the `wave` Helm repository, chart version
`4.5.0`, with default values. There is no `namespace.yaml` alongside it, unlike the other tools in
this discipline.

The reason both this and Reloader are mapped: they are not really competitors, they are two
positions on the same question. **Is a workload's configuration part of its desired state, or an
input it reads?** Wave answers "part of its desired state" and makes the hash prove it. Reloader
answers "an input", and reacts when the input moves. Running both is not useful; choosing between
them is a real decision, made in [`../README.md`](../README.md).

---

[← Config reload](../README.md)
