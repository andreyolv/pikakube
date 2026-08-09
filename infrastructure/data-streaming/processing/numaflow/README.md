[← Stream processing](../README.md)

# Numaflow

<https://github.com/numaproj/numaflow>
<https://github.com/numaproj/helm-charts>
<https://numaflow.numaproj.io/>

---

## What it is

Stream processing as **Kubernetes resources**. A pipeline is a CRD; each vertex is a container;
the platform handles buffering, scaling and delivery between them.

```yaml
apiVersion: numaflow.numaproj.io/v1alpha1
kind: Pipeline
spec:
  vertices:
    - name: in
      source: { kafka: {...} }
    - name: transform
      udf: { container: { image: my-transform } }
    - name: out
      sink: { kafka: {...} }
```

From the Numaproj family — the same project as Argo Workflows, Argo Rollouts and Argo Events —
and it shares their instinct: everything is a Kubernetes object.

| Property | Consequence |
|---|---|
| **Language-agnostic** | a vertex is a container, so any language works |
| Kubernetes-native | pipelines are objects, reconciled from Git |
| Auto-scaling per vertex | including to zero |
| Built-in buffering | between vertices, so slow stages apply back pressure |

## When to use it

- pipelines should be **Kubernetes resources**, reconciled by Flux like everything else
- the processing logic is in several languages, or in an existing container
- the Argo ecosystem is already in use
- per-vertex autoscaling matters, including scale to zero

## When not to use it

- complex **stateful** semantics — event time, watermarks, large keyed state. That is [Flink](../flink/README.md)
- SQL is the interface — [RisingWave](../risingwave/README.md) or [ksqlDB](../ksqldb/README.md)
- stateless plumbing, where [Benthos](../benthos/README.md) is one binary and no CRDs

## The trade

Excellent operational fit, limited processing semantics.

If pipelines belonging in Git as manifests is the priority — and for a GitOps repository that is
a real argument — this is the most natural shape here. If the processing needs windowing and
watermarks handled correctly, it is not the tool.

The honest split: **Numaflow for pipelines that move and transform, Flink for pipelines that
compute over time.**

---

[← Stream processing](../README.md)
