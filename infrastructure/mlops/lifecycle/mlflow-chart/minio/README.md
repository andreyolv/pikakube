[← MLflow](../README.md)

# MinIO

<https://github.com/minio/minio>

---

## Why it is here

[MLflow](../README.md) writes artifacts — models, plots, datasets, anything logged from a run —
to **S3-compatible object storage**. In a cloud that means S3, Blob Storage or GCS. On a local or
on-prem cluster there is no such service, and MinIO fills that gap.

It is not an MLOps component. It is the object storage backend that makes MLflow's artifact
design work outside a cloud, and the same role applies to
[Loki](../../../../observability/logs/storage/loki/minio/README.md),
[Thanos](../../../../observability/metrics/long-term-storage/thanos/README.md) and anything else
that expects a bucket.

The specific thing it makes testable: MLflow clients upload artifacts to the artifact root
**directly**, not through the tracking server. That path is easy to get wrong and impossible to
exercise without a bucket, so a broken artifact root usually shows up the first time somebody
logs a model rather than at deploy time.

## When to use it

- local or on-prem clusters where MLflow needs a bucket and no cloud provides one
- development environments that should behave like production without a cloud account
- air-gapped deployments

## When not to use it

- running in a cloud that already offers object storage — use it; there is no reason to operate a storage system to reach a service that already exists
- you need the durability guarantees of a managed provider without operating for them

## What it costs you

Object storage is where the data actually lives. Running it yourself means owning replication,
capacity and backup for the layer everything else assumes is reliable — which is a real
responsibility, and easy to skip past when it is "just the MLflow backend".

---

## Notes

**How it is wired.** The bucket is `mlflow`, matching `mlflow.defaultArtifactRoot: s3://mlflow/`
in [`../helm/helmrelease.yaml`](../helm/helmrelease.yaml). The server reaches it at
`http://minio.mlflow.svc.cluster.local:9000` through `MLFLOW_S3_ENDPOINT_URL`, and authenticates
with `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` read from `minio-credentials`.

**This turns the IRSA annotation off in practice.** `serviceAccount.annotations` still carries an
`eks.amazonaws.com/role-arn`, and it does nothing while those two environment variables are set —
boto3 resolves environment credentials before the web-identity token. That is the intended
behaviour for a test, and it is also the thing to remember when moving back to real S3: removing
the `env` block is what re-enables the role, not adding the annotation.

**The credentials are committed.** `pikakube` / `pikakube`, base64 in `secret.yaml`, the same pair
the other MinIO deployments in this repository use. Fine for a local stand-in and not a pattern to
carry anywhere else — [`../postgres/`](../postgres/) shows what the alternative looks like when it
matters.

**Clients need the endpoint too.** Setting `MLFLOW_S3_ENDPOINT_URL` on the server covers the
server's own reads. Anything that logs artifacts — a notebook, a training job — uploads to MinIO
itself and needs the same variable and credentials in its own environment. The service is
`ClusterIP`, so from outside the cluster that means a port-forward:

```bash
kubectl port-forward -n mlflow svc/minio 9000:9000
```

Python client reference: <https://github.com/boto/boto3>

MinIO speaks the S3 API, so `boto3` works against it unchanged — which is what makes it a
faithful local stand-in for S3 in pipelines and tests as well as for MLflow.

---

[← MLflow](../README.md)
