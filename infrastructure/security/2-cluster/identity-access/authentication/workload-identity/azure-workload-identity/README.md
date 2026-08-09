[← Workload identity](../README.md)

# Azure Workload Identity

<https://github.com/Azure/azure-workload-identity>

---

## The problem it solves

A pod on AKS needs to read from Blob Storage, pull a secret from Key Vault, or call any Azure
API. The old answer was a service principal's client ID and **client secret** in a Kubernetes
Secret — a credential with an expiry measured in years, copied through a terminal and a pipeline
before it ever reached the cluster.

Azure Workload Identity removes it entirely, using OIDC federation:

1. The cluster publishes an **OIDC issuer** — a discovery document and a JWKS endpoint. On AKS
   this is a single flag; on any other cluster it can be a static file in blob storage.
2. In Entra ID, a **federated identity credential** is added to a managed identity or app
   registration, saying: trust tokens from *that* issuer whose `sub` is
   `system:serviceaccount:<namespace>:<name>` and whose `aud` is `api://AzureADTokenExchange`.
3. A **mutating webhook** in the cluster sees a pod labelled for workload identity and injects
   a projected ServiceAccount token plus the environment variables the Azure SDKs look for.
4. The pod's SDK exchanges that token at Entra ID's token endpoint for a **short-lived Azure
   access token**.

The result matches the argument in [`../README.md`](../README.md) exactly:

| | Service principal secret | Workload identity |
|---|---|---|
| Stored credential | yes, in a Secret | **none** |
| Lifetime | months to years | minutes |
| Rotation | manual, and it expires and breaks production | automatic |
| Attribution in Azure logs | "a service principal" | the specific ServiceAccount and namespace |
| If the cluster is compromised | the secret is exfiltrable and works anywhere | a token that expires in an hour and is audience-bound |

Two further points worth knowing:

- **It replaces AAD Pod Identity**, which is deprecated. The old approach intercepted the
  instance metadata endpoint — the same fundamentally weak pattern as `kube2iam` on AWS, with
  the same weaknesses: host-network pods bypass it, and identity rests on a pod annotation
  rather than anything cryptographic. Workload identity is federation, not interception.
- **It is not AKS-only.** Because the trust anchor is an OIDC issuer, it works on any Kubernetes
  cluster that can publish a discovery document reachable by Entra ID — self-managed clusters,
  or clusters in other clouds. AKS just makes the issuer a checkbox.

## When to use it

- **Any pod on AKS that calls any Azure service.** There is essentially no argument for a stored
  service principal secret once this is available.
- **Non-AKS clusters that need Azure resources**, where you can host the OIDC discovery document
  somewhere Entra ID can reach.
- **Migrating off AAD Pod Identity**, which is deprecated and should not be carried forward.
- **When Azure-side attribution matters.** Azure's activity log naming the ServiceAccount and
  namespace instead of an opaque service principal is a real operational improvement during an
  incident.

## When not to use it

- **You are not on Azure.** Use the equivalent: **IRSA** or EKS Pod Identity on AWS, **Workload
  Identity Federation** on GCP.
- **You need identity for service-to-service traffic inside the cluster.** This federates *to
  Azure* and does nothing for pod-to-pod authentication. That is [SPIRE](../spire/README.md) or
  a service mesh.
- **The workload cannot use a current Azure SDK.** The exchange relies on the SDK's
  `WorkloadIdentityCredential`. Very old SDK versions and hand-rolled HTTP clients need updating
  or must perform the token exchange manually.
- **The target does not accept Entra ID tokens.** A Postgres instance with password
  authentication is not helped — though Azure Database for PostgreSQL does support Entra ID
  authentication, which is worth checking before concluding a password is required.

## Notes

**`https://github.com/Azure/azure-workload-identity`** — the project. It is the mutating webhook
plus the `azwi` CLI; the actual token exchange is done by the Azure SDK inside your workload,
not by this component.

The recorded notes were working notes about the labels and annotations, in Portuguese in part.
Preserved and explained:

**`pod label azure.workload.identity/use`**

Correct, and the mechanism is worth stating: the mutating webhook only acts on pods carrying
`azure.workload.identity/use: "true"`. Without that label nothing is injected — no projected
token volume, and none of the environment variables the SDK reads
(`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_FEDERATED_TOKEN_FILE`,
`AZURE_AUTHORITY_HOST`). This is the single most common reason a correctly configured setup
silently fails: the federated identity credential is right, the ServiceAccount is right, and the
**pod template** is missing the label. Note that the label goes on the *pod template*, not on
the Deployment.

**`sa label azure.workload.identity/client-id`  `azure.workload.identity/tenant-id`**

Two corrections worth recording, because the note was working from memory:

- These are **annotations** on the ServiceAccount, not labels. `azure.workload.identity/client-id`
  is the annotation that tells the webhook which Entra ID application or managed identity this
  ServiceAccount maps to. Getting the label/annotation distinction wrong produces exactly the
  same silent failure as above.
- The pod-level `azure.workload.identity/use` **is** a label. So the two live in different
  places, which is precisely why this is easy to get wrong.

**`(talvez pegue automático como default, testar)`** — Portuguese for *"maybe it picks it up
automatically as a default, test it"*, written about the tenant ID.

The author's guess was right. The tenant ID does **not** normally need to be set per
ServiceAccount: the webhook is deployed with a cluster-wide default (`azureTenantID` in the Helm
values), and it uses that unless a ServiceAccount overrides it with
`azure.workload.identity/tenant-id`. The per-ServiceAccount annotation exists for the
multi-tenant case, where different workloads federate to identities in different Entra ID
tenants. For a single-tenant cluster, the chart-level value is sufficient — and the staged
HelmRelease does exactly that.

Also worth adding, since it is the other common tuning point:
`azure.workload.identity/service-account-token-expiration` on the ServiceAccount controls the
projected token's lifetime. The default is one hour and it is almost always right; lengthening
it gives back the property that made the change worthwhile.

What is staged: a `HelmRepository`, a `Namespace` `azure-workload-identity`, and a `HelmRelease`
for the `workload-identity-webhook` chart at version `1.4.1`.

| Setting | What it means |
|---|---|
| `azureTenantID: xxxxxxxxxxxx` | the cluster-wide default tenant, placeholder as staged — the value the note above was asking about |
| `nodeSelector.agentpool: sysephem` | pins the webhook to a specific **AKS node pool**. This is an import from a real Azure cluster; `agentpool` is an AKS-specific node label and means nothing on any other cluster |
| `tolerations: CriticalAddonsOnly=true:NoSchedule` | tolerates the taint AKS puts on system node pools, so the webhook can run there. Correct for AKS — a mutating webhook in the admission path is genuinely a critical addon, and it should not be scheduled onto user workload nodes |

The node selector and toleration together are the clearest evidence that these manifests came
from a working AKS deployment rather than being written from documentation. On a local Kind
cluster they would prevent the pod from scheduling at all.

---

[← Workload identity](../README.md)
