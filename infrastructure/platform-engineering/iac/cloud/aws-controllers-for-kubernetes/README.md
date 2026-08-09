[← Cloud control planes](../README.md)

# AWS Controllers for Kubernetes (ACK)

<https://github.com/aws-controllers-k8s/community>

---

## The problem it solves

ACK is AWS's answer to declaring AWS resources as Kubernetes objects. An `S3.Bucket`, an
`RDS.DBInstance` or an `SQS.Queue` becomes a namespaced custom resource, reconciled by a controller
running in the cluster against the AWS API.

Its distinguishing decision is packaging: **one controller per AWS service**. There is an S3
controller, an RDS controller, an SQS controller, each released, versioned and installed separately,
each with its own IAM role. That is unlike [ASO](../azure-service-operator/README.md) and
[Config Connector](../gcp-config-connector/README.md), which install once and bring a broad CRD
surface.

The consequence cuts both ways. Permissions can be scoped tightly — the S3 controller's role need
grant nothing but S3 — and the cluster now has one deployment, one chart version and one IAM role per
service in use. Adopting five services means five of everything.

Service coverage is per-controller and maturity varies widely across them: some are generally
available, others are in preview with a partial field set. This is the check to do first, per
resource, before assuming the pattern applies.

## When to use it

- the platform runs on AWS and application teams should declare their own buckets, queues or topics
  beside the workload that uses them
- connection details should land in a `Secret` in the namespace rather than travel from a Terraform
  output by hand
- **tight IAM scoping matters** — the per-service split is a genuine advantage here
- only a small number of AWS services are involved, so the per-controller overhead stays small

## When not to use it

- the resources needed have no controller, or a controller that does not expose the fields you need —
  verify before committing, not during
- many AWS services are in play; the operational cost multiplies by service
- a reviewed `plan` before changes to production data stores is a requirement
- IRSA or EKS Pod Identity is not available, leaving static credentials as the only option — that
  turns a cluster compromise into an account compromise

## Notes

Both links from the original note, with what each is for:

- <https://github.com/aws-controllers-k8s/community> — the umbrella repository. Worth knowing that
  this is *not* the code: each service controller lives in its own repository, and this one holds the
  issues, the roadmap and, most usefully, the **service maturity table**. That table is the first
  thing to read, because it answers "is the controller for this service usable" before any effort is
  spent.
- <https://aws-controllers-k8s.github.io/community/docs/user-docs/install/> — the install guide. It
  is per-controller: a Helm chart per service, published as OCI artefacts in ECR Public, with the
  service name in the chart path. Expect to repeat the installation for every service adopted.

The install guide also covers the credential setup, which is the part that matters most. The
supported path is **IRSA** — an IAM role assumed by the controller's service account — or EKS Pod
Identity. Each controller gets its own role, and that role should be scoped to the service and, where
possible, to the resources it is expected to manage.

Nothing is deployed in this folder: two links, no manifests, no commentary. ACK is mapped as the AWS
option, and the platform's actual cloud is Azure — see
[ASO](../azure-service-operator/README.md), which is the one here with working manifests.

Before this is ever adopted, the deletion behaviour described in [`cloud/`](../README.md) section 4
is the thing to settle. ACK resources support a deletion policy that leaves the AWS resource in place
when the Kubernetes object goes away; the default does not, and a deleted namespace is a deleted
bucket.

---

[← Cloud control planes](../README.md)
