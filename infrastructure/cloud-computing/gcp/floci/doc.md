https://github.com/floci-io/floci-gcp

The GCP counterpart to [floci](../../aws/floci/doc.md) (AWS) and
[floci-az](../../azure/floci/doc.md). MIT.

- 20+ services: Cloud Storage, Firestore, Datastore, Pub/Sub, Managed Kafka, Eventarc,
  Secret Manager, Cloud KMS, IAM, Firebase Auth, Cloud Run, Cloud Functions, GKE, Cloud SQL
  (PostgreSQL), Cloud Logging, Cloud Tasks, Cloud Scheduler, BigQuery (phase 1)
- everything on port **4588**, one listener, HTTP/2 ALPN — no per-service emulator daemon,
  which is the usual GCP local-dev experience
- `docker compose up -d`, Docker socket mounted for the services backed by real containers

The youngest of the three runtimes and the one to verify before relying on: several services are
marked phase 1. BigQuery in particular is worth checking against what a pipeline actually calls
before assuming it covers it.

Narrower alternative for storage alone: [fake-gcs-server](../fake-gcs-server/doc.md).
Console: [floci-ui](../../aws/floci/doc.md).
