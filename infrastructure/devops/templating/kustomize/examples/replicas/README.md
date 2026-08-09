[← Kustomize examples](../README.md)

# replicas

Sets the replica count of a named workload.

```yaml
resources:
  - ../../base
replicas:
- name: ubuntu
  count: 5
```

A dedicated transformer for one field, because it is the field that differs between environments
more often than any other and writing a patch for it every time is noise.

**The caveat that matters:** if a `HorizontalPodAutoscaler` manages the same workload, this field
is a starting value and nothing more. The HPA writes `spec.replicas` continuously, so the
declared count and the running count diverge immediately, and the diff between Git and the
cluster is permanent. With an autoscaler in play, set `minReplicas` on the HPA and leave
`replicas` out of the manifest entirely, or the GitOps controller and the HPA will take turns
overwriting each other.

Rendered result in [`output.yaml`](output.yaml):

```bash
kustomize build overlays/dev -o output.yaml
```

---

[← Kustomize examples](../README.md)
