[← Lifecycle](../README.md)

# MLflow 2 (rebuild)

<https://github.com/mlflow/mlflow>
<https://github.com/cloudnative-pg/cloudnative-pg>
<https://github.com/external-secrets/external-secrets>

---

## The problem it solves

Same tool as [`../mlflow/`](../mlflow/README.md) — MLflow tracking and the Model Registry. What
this folder solves is different: it is the **second attempt at deploying it**, and it exists
because MLflow ships no official Helm chart, so improving a deployment means rewriting the
manifests rather than bumping a chart version.

The problems this rebuild fixes, each of which was a real weakness of the first deployment:

| Problem in `mlflow/` | Fix here |
|---|---|
| Third-party image on a floating `:latest` tag | official `ghcr.io/mlflow/mlflow:v3.3.2`, pinned |
| Postgres as a hand-written Deployment + PVC — no backups, no failover, no metrics | a CloudNativePG `Cluster` with a `PodMonitor` |
| Credentials in a committed `Secret` template, injected by hand | a generated 42-character password through `external-secrets` |
| Static MinIO access keys in a Secret | a ServiceAccount annotated with an IAM role — no long-lived keys |
| No metrics from the server | `--expose-prometheus=/metrics` |

### What is deployed here

| File | What it contains |
|---|---|
| `namespace.yaml` | the `mlflow` namespace, labelled `agentpool: spot` |
| `deployment.yaml` | the MLflow server, `ghcr.io/mlflow/mlflow:v3.3.2`, port 5000, `Recreate` strategy, running as the `mlflow-server` ServiceAccount |
| `service.yaml` | ClusterIP service on 5000 |
| `serviceaccount.yaml` | `mlflow-server`, annotated `eks.amazonaws.com/role-arn` — AWS IRSA, so S3 access comes from a role rather than keys |
| `postgres/cluster.yaml` | a CloudNativePG `Cluster`: 1 instance, PostgreSQL 17.5, 2 Gi storage, database and owner both `mlflow`, `enablePodMonitor: true` |
| `postgres/password.yaml` | an external-secrets `Password` generator — 42 characters, 5 digits, no symbols |
| `postgres/externalsecret.yaml` | an `ExternalSecret` that draws from that generator and templates both `password` and a full `connection` string into the `postgres-app` Secret |

The server reads `POSTGRES_CONN` from the `connection` key of `postgres-app` and passes it as
`--backend-store-uri`; artifacts go to `s3://mlflow/` with `MLFLOW_S3_ENDPOINT_URL` pointing at an
S3 endpoint. That is the Postgres + object-storage pairing argued for in
[`../README.md`](../README.md#4-the-backing-store-decision).

Three details in `externalsecret.yaml` are load-bearing and easy to miss:

- `creationPolicy: Merge` — the Secret is **not** created by external-secrets. CloudNativePG
  creates `postgres-app` itself; this merges a generated password and a connection string into
  the existing object rather than fighting the operator over ownership.
- `cnpg.io/reload: "true"` — the label that tells CloudNativePG to pick the change up.
- `refreshInterval: 168h` — one week. With a generator source this is a rotation cadence, not a
  sync cadence.

## When to use it

- Use this rather than [`../mlflow/`](../mlflow/README.md) for any new deployment. It is the same
  tool, correctly assembled.
- Where a Postgres operator is already available — CloudNativePG gives backups, failover and
  metrics that a hand-written Deployment does not, at roughly no extra effort.
- On a cloud where workload identity exists (IRSA here). Removing static object-storage keys is
  the single largest security improvement over the first deployment.
- Where Prometheus is scraping, so `--expose-prometheus` and the `PodMonitor` are worth having.

## When not to use it

- **As-is, on an exposed endpoint.** There is no authentication in this folder. See the notes.
- On a cluster without the CloudNativePG operator and external-secrets installed — the
  `postgres/` manifests are inert CRDs without them.
- Outside AWS without changing `serviceaccount.yaml`. The IRSA annotation is AWS-specific; the
  equivalents are Workload Identity on GCP and Azure Workload Identity.
- Alongside [`../mlflow/`](../mlflow/README.md). Both claim the `mlflow` namespace and both create
  a `mlflow-server` Deployment and Service. They are alternatives, not a pair.

## Notes

There was no `doc.md` for this folder. The notes below are read from the manifests.

**The `agentpool: spot` label on the namespace.** A hint that workloads here are expected to land
on spot/preemptible nodes. A namespace label does nothing by itself — it only has an effect if a
mutating policy, a scheduler plugin or a cloud add-on reads it. Worth being deliberate about:
MLflow's server tolerates eviction reasonably (it is stateless, with `Recreate` handling the
restart), but a single-instance CloudNativePG cluster on spot capacity means the tracking database
goes away with the node.

**`MLFLOW_S3_ENDPOINT_URL` is `http://xxxxxxxxxxxxxxxx`.** A placeholder, as with the sanitised
values in the first deployment. The manifest is a template, not a live configuration.

**One CNPG instance.** `instances: 1` means no failover and no read replica; a node loss is an
outage of tracking and the registry. CNPG still earns its place at one instance — backups,
monitoring and a managed upgrade path — but this is not a highly available database, and the
`agentpool: spot` label above makes that more pointed.

**Storage is 2 Gi**, the same as the first deployment. The backend store grows with the number of
runs logged; this is a starting value, not a sized one.

**`--expose-prometheus=/metrics` is set and nothing scrapes it.** The flag makes MLflow serve
Prometheus metrics on the server. There is no `ServiceMonitor` or `PodMonitor` for the MLflow
Service in this folder — only the Postgres cluster has one, via `enablePodMonitor`. The server's
metrics are exposed and unmonitored. See [`../../../observability/metrics/`](../../../observability/metrics/README.md).

**No resource limits.** Only a 1 Gi memory request on the server and 1 CPU / 1 Gi on the Postgres
cluster. Both are burstable and evictable under node pressure — again, notable given the spot
label.

**No authentication, and this is the significant gap.** [`../mlflow/`](../mlflow/README.md) put an
`oauth2_proxy` in front of the UI, restricted to a GitHub org and team. That is gone here. MLflow's
open-source UI has no built-in authentication of its own, and it holds every logged metric,
parameter, dataset sample and model artifact. Whatever fronts this deployment — an ingress with an
auth annotation, an auth proxy, a service mesh — has to supply it, and it is not in this folder.
The pattern lives under
`../../../security/2-cluster/identity-access/authentication/auth-proxy/`.

**Why the folder is named `mlflow2` rather than replacing `mlflow/`.** The first deployment is kept
as history. That is defensible as a record, and it is a trap for anyone who applies the wrong
directory — both target the same namespace with the same object names.

---

[← Lifecycle](../README.md)
