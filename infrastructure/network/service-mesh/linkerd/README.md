[← Service mesh](../README.md)

# Linkerd

<https://github.com/linkerd/linkerd2>
<https://linkerd.io/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

The same core problem as any mesh — mTLS, retries, timeouts and golden metrics between
services — with a deliberate bias toward **being small**.

Its proxy is purpose-built in Rust rather than being Envoy, which keeps memory and latency
overhead low and reduces the number of knobs. Less to configure, less to get wrong.

## When to use it

- you want **mTLS, retries and per-service golden metrics** with the smallest operational burden available
- the team is adopting a mesh for the first time and complexity is the main risk
- Istio's feature surface is larger than the actual requirement

## When not to use it

- you need fine-grained traffic manipulation, an extension ecosystem, or complex multi-cluster topologies — that is [Istio](../istio/)
- workloads run outside Kubernetes too — see [Kuma](../kuma/) or [Consul](../consul/)

---

## Notes

### Does not work with Airflow using KubernetesExecutor

The sidecar keeps running after the task container exits, so the pod never completes.

<https://github.com/apache/airflow/discussions/16033>

**Jobs and CronJobs need the injection annotation set to `false`.** This is the general form
of the same problem — any batch workload with a sidecar mesh needs explicit exclusion, or it
hangs forever in `NotReady` after finishing its work.

### Grafana

<https://raw.githubusercontent.com/linkerd/linkerd2/main/grafana/values.yaml>

### Examples

- <https://linkerd.io/2-edge/tasks/books/>
- <https://linkerd.io/2-edge/tasks/configuring-per-route-policy/>
- <https://linkerd.io/2-edge/tasks/configuring-rate-limiting/>

### Certificates

The mesh CA can be bootstrapped with cert-manager using a `selfSigned` ClusterIssuer — see
[cert-manager](../../../security/2-cluster/certificates/cert-manager/README.md).

---

[← Service mesh](../README.md)
