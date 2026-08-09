[← Cloud control planes](../README.md)

# Azure Service Operator (ASO)

<https://github.com/Azure/azure-service-operator>

---

## The problem it solves

ASO is Microsoft's operator for managing Azure resources as Kubernetes objects. A `ResourceGroup`, a
`FlexibleServer`, a `StorageAccount` or a role assignment becomes a namespaced custom resource, and a
controller in the cluster reconciles it against Azure Resource Manager on an interval.

It installs as a single operator covering many services, rather than one controller per service as
[ACK](../aws-controllers-for-kubernetes/README.md) does. The CRD surface is generated from the Azure
ARM schemas, which is why the API versions in the manifests look like Azure API versions —
`resources.azure.com/v1api20200601` is literally the ARM API version pinned into the group.

That is a useful property once you notice it: choosing a CRD version is choosing which ARM API
contract to reconcile against, and upgrading the operator does not silently move you onto a different
one.

The operator also writes resource outputs into a `Secret` in the namespace, which closes the gap
between "Azure created a database" and "the Deployment has its connection string".

## When to use it

- the platform runs on Azure and Azure resources should live in the same repository and
  reconciliation loop as the workloads
- application teams should declare their own resource groups, databases or storage accounts without a
  separate Terraform workflow
- pinning to a specific ARM API version per resource is valuable
- connection details should reach workloads as a `Secret` rather than as a copied value

## When not to use it

- **cert-manager is not available and is not wanted** — ASO's admission webhooks need certificates,
  and without cert-manager the install does not become ready
- the resources or fields you need are not covered; check the supported-resources list before
  committing
- a reviewed plan before changes to production data stores is a requirement
- there is no appetite to give a cluster controller credentials that can create and delete Azure
  infrastructure

## Notes

Both links from the original note:

- <https://github.com/Azure/azure-service-operator> — the project.
- <https://azure.github.io/azure-service-operator/reference/> — the **resource reference**, and the
  more useful of the two in practice. It lists every supported resource with its CRD group, its
  version and its full field set. Because coverage is the deciding factor for this whole category —
  see [`cloud/`](../README.md) section 2 — this page is where an ASO evaluation actually happens.

### What is checked in, and the one detail that matters

A `HelmRepository` pointing at `https://raw.githubusercontent.com/Azure/azure-service-operator/main/v2/charts`
and a `HelmRelease` installing chart `azure-service-operator` at **1.12.0** into its own namespace.

The important line is not the version:

```yaml
  dependsOn:
  - name: cert-manager
    namespace: cert-manager
```

ASO registers validating and mutating admission webhooks, and webhooks require a serving certificate.
Without cert-manager the webhook configuration exists, the certificate does not, and the API server
starts rejecting requests for ASO resources with TLS errors that name neither cert-manager nor the
missing certificate. It is a genuinely confusing failure, and it is not documented as loudly as it
should be.

Encoding that as a Flux `dependsOn` rather than as a note is the correct fix: helm-controller will not
attempt the release until cert-manager's own release is ready, so the ordering is enforced rather
than remembered. This is the concrete case for `dependsOn` described in [`flux/`](../../../gitops/flux/README.md).

Note also that the chart is served from **`raw.githubusercontent.com`** rather than from a Helm
repository or an OCI registry. It works, and it makes GitHub availability a dependency of your Helm
reconciliation — worth knowing when a release fails to fetch for reasons that have nothing to do with
Azure.

### The examples

`examples/resourcegroup.yaml` is upstream's own sample: a `ResourceGroup` named `aso-sample-rg` in
`westcentralus`, at API version `v1api20200601`. A resource group is the right thing to try first —
it is free, it is trivially deletable, and creating one proves the whole authentication chain works.

`examples/secret.yaml` is the credentials template, with empty `ARM_SUBSCRIPTION_ID`,
`ARM_TENANT_ID`, `ARM_CLIENT_ID` and `ARM_CLIENT_SECRET`. The same four variables appear in the
[tf-controller](../../../gitops/flux/tf-controller/README.md) example, which is a fair summary of how
this platform authenticates to Azure today: a service principal with a client secret.

That is the part to improve before anything real is created this way. A client secret is a long-lived
credential in the cluster with Azure write access; **Azure Workload Identity** replaces it with a
federated token and no stored secret, and ASO supports it. The recorded setup is the quick path, not
the durable one.

### Before creating anything with data in it

The deletion behaviour in [`cloud/`](../README.md) section 4 is not theoretical here. ASO deletes the
Azure resource when the Kubernetes object is deleted, and it supports a reclaim policy that abandons
the resource instead. Set it on anything stateful before it exists, because a deleted namespace or a
Flux `prune` will otherwise do exactly what it was told to.

---

[← Cloud control planes](../README.md)
