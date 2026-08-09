[← Core](../README.md)

# Python client

<https://github.com/kubernetes-client/python>

---

## The problem it solves

Sometimes a script needs to ask the cluster something — which namespaces exist, which pods are
failing, what an annotation says — and shelling out to `kubectl` and parsing the output is the wrong
shape. The official Python client wraps the API properly: typed objects, watches, pagination,
authentication handled.

This folder is a complete worked example of doing that **from inside the cluster**: a Deployment
running a Python process that authenticates as a ServiceAccount, lists namespaces on a loop, and
caches the result on disk.

## When to use it

- Automation that needs to read or react to cluster state, running as a workload
- A prototype of a controller, before committing to a real one — see [`operators/`](../../operators/README.md)
- Exporters, reporting jobs, anything that must call the API on a schedule
- Learning how in-cluster authentication actually works, because this is the smallest complete example

## When not to use it

- Reconciliation loops with real semantics — that is [Kopf](../../operators/kopf/README.md) or a
  proper controller framework, both of which handle retries, watches and finalizers for you
- Anything a `kubectl` one-liner covers
- Where cluster-admin would be needed; a script with broad permissions running unattended is a standing risk
- High-frequency polling; watches exist, and the API server has other users

## Notes

**The example does three things worth extracting.**

`config.load_incluster_config()` — reads the ServiceAccount token and CA bundle that Kubernetes mounts
into every pod at `/var/run/secrets/kubernetes.io/serviceaccount/`. No kubeconfig, no credentials in
the image. The code keeps `config.load_kube_config()` beside it as a comment, which is the
out-of-cluster equivalent that reads `~/.kube/config` — the two-line difference between running
locally and running as a pod, and the thing people get stuck on first.

**A file-based cache with a 600-second expiry**, pickled to disk, refreshed on a loop with a
60-second sleep. It demonstrates a real pattern — do not hammer the API server for data that changes
slowly — though the specific implementation has a flaw worth naming: the cache file lives in the
container's writable layer, so it does not survive a restart. For a genuine cache that needs to
outlive the pod, that is a volume; for reducing API load within one pod's lifetime, it is fine as
written.

**RBAC scoped to exactly what the code calls.** The `rbac.yaml` creates a `kubernetes-client`
ServiceAccount in the `teste` namespace and a `ClusterRole` granting precisely:

```yaml
rules:
- apiGroups: [""]
  resources: ["namespaces"]
  verbs: ["get", "list"]
```

That is the model to copy. The application lists namespaces, so it may list namespaces, and nothing
else. Compare it with the broad developer role in
[`cluster-permissions/`](../cluster-permissions/README.md) — the contrast between human access and
machine access is the whole point.

One detail: a `ClusterRole` is required rather than a `Role` because namespaces are cluster-scoped
objects. The `namespace: teste` field on the `ClusterRole` in the file is ignored by the API server —
harmless, and a common copy-paste artifact.

**Build script:**

```sh
docker image build . -t kubernetes-client:latest
docker tag kubernetes-client:latest andreyolv/kubernetes-client:latest
docker push andreyolv/kubernetes-client:latest
```

`set -e` at the top, so a failed build does not silently push a stale image. The `latest` tag is
convenient here and is exactly what not to do in a cluster that has to redeploy predictably.

---

[← Core](../README.md)
