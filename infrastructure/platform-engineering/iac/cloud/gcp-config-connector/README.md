[← Cloud control planes](../README.md)

# GCP Config Connector

<https://github.com/GoogleCloudPlatform/k8s-config-connector>

---

## The problem it solves

Config Connector is Google's operator for managing Google Cloud resources as Kubernetes objects. A
Cloud SQL instance, a Pub/Sub topic, a GCS bucket or an IAM policy binding becomes a custom resource
in a namespace, reconciled against the Google Cloud API by a controller in the cluster.

It installs once and brings a large CRD surface with it, rather than one controller per service as
[ACK](../aws-controllers-for-kubernetes/README.md) does. Coverage is comparatively broad, because a
good deal of it is generated from the same resource definitions Google's own tooling uses.

Two things distinguish it from the other two in this folder:

- **It is available as a GKE add-on.** On GKE it can be enabled on the cluster rather than installed,
  which removes the upgrade and lifecycle work entirely — and also removes the choice of version.
- **Namespaces map to projects.** A namespace can be annotated with the Google Cloud project its
  resources belong to, so multi-project estates get a natural boundary that matches the Kubernetes
  one.

## When to use it

- the platform runs on Google Cloud, and especially on GKE where the add-on makes installation a
  cluster setting
- application teams should declare their own Google Cloud resources beside the workloads that use
  them
- **IAM should be declarative too** — Config Connector covers IAM bindings, which is a meaningful
  part of what Terraform is usually kept around for
- several Google Cloud projects are in play and the namespace-to-project mapping is useful

## When not to use it

- not on Google Cloud
- Workload Identity is unavailable, leaving a static service-account key in the cluster as the only
  credential path
- a reviewed plan before changes to production data stores is a requirement
- the manual installation path is being taken on a non-GKE cluster and nobody wants to own the
  upgrade cycle for a cluster-privileged operator

## Notes

Both links from the original note:

- <https://github.com/GoogleCloudPlatform/k8s-config-connector> — the project. Also the place to
  check which resources are covered and at what maturity, which is the same first question as with
  the other two controllers here.
- <https://cloud.google.com/config-connector/docs/how-to/install-manually> — specifically the
  **manual** installation guide, not the GKE add-on one. That choice is informative: the manual path
  is what you need on a cluster that is not GKE, or on GKE when the add-on's version is not the one
  you want. It is also the path that leaves you owning the upgrades.

The manual guide is where the Workload Identity setup lives, and that is the part worth reading
closely. The controller authenticates as a Google service account bound to its Kubernetes service
account; the alternative — exporting a service-account key into a `Secret` — is a long-lived
credential with cloud write access sitting in the cluster.

Nothing is deployed in this folder: two links, no manifests, no commentary. Config Connector is
mapped as the Google Cloud option. The platform is Azure-flavoured throughout — see
[ASO](../azure-service-operator/README.md), the only one of the three here with working manifests.

The deletion behaviour in [`cloud/`](../README.md) section 4 applies here too: Config Connector
supports an abandon-on-delete policy, and without it removing the Kubernetes object removes the
Google Cloud resource.

---

[← Cloud control planes](../README.md)
