[← Lifecycle](../README.md)

# MLflow

<https://github.com/mlflow/mlflow>

---

## The problem it solves

Experiments are not reproducible and not recorded. Somebody trained a model that scored well, and
a week later nobody can say which parameters produced it, which data it saw, or where the file
came from.

MLflow answers that with a tracking server: every run logs its parameters, metrics, tags and
artifacts to one place with a UI and an API. On top of that sits a **Model Registry** — named
models with versions, stages and aliases — which is the handoff artefact between "we trained
something" and "we deployed something".

It is deliberately **a library plus a server**, not a platform. It does not run your training, it
does not schedule anything, and it does not manage a cluster. That narrowness is why it is the
pragmatic default: the whole install is one container and one database. See
[`../README.md`](../README.md) for how its four components split, and for the MLflow-vs-Kubeflow
decision.

**This folder is the first of two deployments.** It is the earlier one — a hand-assembled stack
with authentication solved and operations not. The rebuild is [`../mlflow2/`](../mlflow2/README.md).

### What is deployed here

| Folder / file | What it contains |
|---|---|
| `namespace.yaml` | the `mlflow` namespace |
| `deployment/mlflow-server.yaml` | the MLflow server, image `joshsgoldstein/mlflow-server:latest`, port 5000, 2 workers, `Recreate` strategy |
| `deployment/postgres.yaml` | a hand-written PostgreSQL 14.6 `Deployment`, backing store for runs and the registry |
| `service/mlflow-server.yaml` | ClusterIP service on 5000 |
| `service/postgres-mlflow.yaml` | ClusterIP service on 5432 |
| `pvc/mlflow-postgres.yaml` | a 2 Gi `ReadWriteOnce` PVC on storage class `standard`, mounted at the Postgres data directory |
| `secrets/mlflow-minio.yaml` | one `Secret` holding the MinIO access/secret keys, the Postgres username/password, **and** the full connection string |
| `oauth/deployment.yaml` | an `oauth2_proxy` v6.1.1 in front of the server, GitHub provider, restricted to a GitHub org and team |
| `oauth/service.yaml` | ClusterIP service on 4180 for the proxy |

The server is configured with `--backend-store-uri` pointing at Postgres and
`--default-artifact-root=s3://mlflow/`, with `MLFLOW_S3_ENDPOINT_URL` set to the in-cluster MinIO
service. That is the correct pairing described in [`../README.md`](../README.md#4-the-backing-store-decision):
a database for metadata, object storage for artifacts.

## When to use it

- You need experiment tracking and a registry, and you want that capability this week rather than
  after a platform migration.
- You have a handful of models and one or two teams. This is the overwhelming majority of cases.
- Training already runs somewhere you are happy with — a notebook, a container, an Airflow DAG.
  MLflow does not want to take that over.
- You want the option to leave. The data is rows in a Postgres you own and files in a bucket you
  own.
- You want a uniform way to load a model regardless of the library that produced it — the
  `pyfunc` flavor.

## When not to use it

- You need pipeline orchestration, notebook provisioning, multi-tenant isolation or distributed
  training operators. MLflow does none of those; that is [Kubeflow](../kubeflow/README.md).
- You want an install that is one Helm command. It is not — see the notes below.
- You expect it to serve production traffic. `mlflow models serve` exists and is a development
  convenience; production serving is KServe, Seldon or BentoML.
- You expect it to monitor a deployed model. MLflow records what happened during training. Drift
  and prediction quality in production are a separate tool (Evidently) and a separate job.

## Notes

**"Still no Helm chart, unbelievable" — <https://github.com/mlflow/mlflow/issues/6118>**

The original note, in Portuguese: *"ainda sem helm chart, inacreditável"*. The complaint is that
a project this widely used ships no official Helm chart, so every Kubernetes deployment is
hand-assembled from scratch. Issue 6118 is the upstream request for one.

This is not a cosmetic gripe — it is why this folder looks the way it does. Everything here
(Deployment, Service, PVC, Secret, the Postgres, the auth proxy) had to be written by hand, and
that is the reason a second deployment exists: there is no upstream artefact to upgrade, so
improving the deployment means rewriting it.

**Recorded characteristics of this deployment, and what each implies:**

| Observation | What it means |
|---|---|
| Image is `joshsgoldstein/mlflow-server:latest` | a third-party image on a floating tag. Unpinned means the server — and its database schema migrations — can change on any pod restart. `mlflow2/` moves to the official `ghcr.io/mlflow/mlflow` image at a pinned version. |
| `secrets/mlflow-minio.yaml` is committed with `xxxxxxxxx` base64 values | placeholders, not real credentials — the file is a template. It still means real secrets are injected by hand somewhere outside the repo, which is what `mlflow2/` replaces with `external-secrets`. |
| One Secret holds MinIO keys, Postgres credentials **and** the connection string | convenient, and it couples unrelated rotations: rotating the object-storage key touches the same object as the database password. |
| Postgres is a plain `Deployment` with a PVC | no backups, no failover, no monitoring, and a manual major-version upgrade path. `mlflow2/` replaces it with a CloudNativePG `Cluster`. |
| `strategy: Recreate` on both Deployments | correct here. A `ReadWriteOnce` PVC cannot be attached to old and new pods simultaneously, so a rolling update would deadlock. |
| PVC is 2 Gi on storage class `standard` | small. The metadata database grows with the number of runs, and this is not a size anyone chose deliberately. |
| `imagePullSecrets: acr-secret` | the server pulls through an Azure Container Registry pull secret that is not defined in this folder. |
| `--workers=2` | two gunicorn workers. Fine for a small team; the limit is concurrent UI and logging clients, not model size. |
| No resource limits, only `requests` (1 Gi server, 500 Mi Postgres) | the pods are burstable and can be evicted under node pressure. |

**The oauth2-proxy in front of the UI**

`oauth/` puts [oauth2_proxy](https://quay.io/pusher/oauth2_proxy) v6.1.1 between users and the
MLflow server: it authenticates against GitHub, restricts access to a named org and team, and
forwards to `http://mlflow-server:5000` as its upstream. This is the standard **auth-proxy
pattern** — put authentication in front of an application that has none of its own — and MLflow's
open-source UI has none of its own. The pattern is documented under
`../../../security/2-cluster/identity-access/authentication/auth-proxy/`.

Two things about it are worth recording:

- `OAUTH2_PROXY_COOKIE_SECRET`, `CLIENT_ID` and `CLIENT_SECRET` are present with empty values.
  The manifest is a template; the proxy will not start until they are filled.
- `quay.io/pusher/oauth2_proxy` is the **abandoned** original. The maintained fork is
  `oauth2-proxy/oauth2-proxy` (`quay.io/oauth2-proxy/oauth2-proxy`), and v6.1.1 dates from 2020.
  Anything reusing this manifest should switch images.

**What this deployment gets right that the rebuild dropped:** authentication. `mlflow2/` has none.

---

[← Lifecycle](../README.md)
