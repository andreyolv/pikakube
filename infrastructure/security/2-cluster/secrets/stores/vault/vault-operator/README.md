[← Vault](../README.md)

# Bank-Vaults vault-operator

<https://github.com/bank-vaults/vault-operator/>
<https://github.com/bank-vaults/bank-vaults>
<https://github.com/bank-vaults/secrets-webhook>

An operator that **runs and configures Vault itself**, declaratively. Not a way to read secrets out
of Vault — the opposite direction from
[vault-secrets-operator](../vault-secrets-operator/README.md).

---

## The problem it solves

Read [`../vault/`](../vault/README.md#initialising-vault-step-by-step) and count the manual steps: port
forward, `vault operator init`, save five key shares and a root token somewhere, unseal three times,
log in, enable a secrets engine, write a policy file, create a token, save that too.

Every one of those is done by hand, none of it is in Git, and none of it is reproducible. The cluster
holds a Vault whose configuration exists only in the memory of whoever set it up. Rebuild the
cluster and the procedure has to be repeated correctly from a text file.

That is the problem this operator addresses. It defines a `Vault` custom resource that describes the
**whole instance** — not just the deployment, but its configuration:

| Declared in the CR | Replaces |
|---|---|
| storage backend, replicas, resources | the Helm chart's values |
| unseal configuration | `vault operator init` plus three `vault operator unseal` calls |
| auth methods (Kubernetes, JWT, ...) | `vault auth enable` |
| secrets engines and their config | `vault secrets enable` |
| policies | `vault policy write` |
| roles and bindings | `vault write auth/kubernetes/role/...` |

The operator initialises Vault, stores the unseal keys and root token in a configured backend (a
cloud KMS bucket, a Kubernetes Secret), unseals automatically, and then reconciles the configuration
continuously — so drift is corrected and the CR is the source of truth.

**Automatic unsealing** is the operational headline. A restarted Vault normally serves nothing until
a human supplies key shares; here the operator does it, with the keys held in a KMS rather than in a
HelmRelease. That is the difference between the correct answer and the shortcut currently used in
[`../vault/`](../vault/README.md), where the unseal key is committed to Git.

**`secrets-webhook`** is the companion project: a mutating webhook that injects Vault values into
pods at admission, based on annotations and `vault:` prefixed environment variable values. It is
Bank-Vaults' alternative to the agent injector and to
[external-secrets](../../../integrations/external-secrets/README.md) — so the Bank-Vaults stack is a
complete alternative to the HashiCorp stack, not a component of it.

## When to use it

- **Vault's configuration must be reproducible from Git.** This is the whole argument. Engines,
  policies, auth methods and roles as declarative resources rather than a runbook.
- **Unattended unsealing without putting the key in Git.** The operator handles init and unseal with
  keys in a KMS or cloud storage bucket.
- **Several Vault instances.** Per environment, per tenant. A `Vault` CR per instance beats running
  the same manual procedure repeatedly.
- **Vault configuration drift is a real problem.** Someone enabled an engine by hand six months ago
  and nobody knows why. Continuous reconciliation makes the CR authoritative.
- **You want one project for the whole lifecycle.** Bank-Vaults covers running Vault, configuring
  it, and injecting secrets into pods.

## When not to use it

- **HashiCorp's chart plus manual setup is good enough.** For one Vault that is configured once, the
  operator is a layer of indirection over a procedure you will run twice.
- **You want vendor support.** Bank-Vaults is a community project (CNCF sandbox), not HashiCorp.
  HashiCorp's supported path is `vault-helm` plus
  [vault-secrets-operator](../vault-secrets-operator/README.md).
- **You need the newest Vault features immediately.** The operator abstracts Vault's configuration,
  so a new engine or field is usable when the operator supports it.
- **You are on OpenBao.** The [licence-driven fork](../../openbao/README.md) is API-compatible, but
  compatibility with an operator that manages the full lifecycle is a thing to verify, not assume.
- **You already committed to the HashiCorp stack.** Running both operators means two things believe
  they own the Vault instance.
- **You would use only the webhook.** `secrets-webhook` is usable independently, and adopting the
  operator for it is unnecessary.

## Notes

Every original note from `doc.md`, translated and explained, plus the state of this folder.

### The three repositories

> <https://github.com/bank-vaults/vault-operator/>
> <https://github.com/bank-vaults/secrets-webhook>
> <https://github.com/bank-vaults/bank-vaults>

Three projects, and the split is worth knowing because the naming is confusing:

| Repository | What it is |
|---|---|
| `vault-operator` | the operator and the `Vault` CRD — this folder |
| `secrets-webhook` | a mutating webhook injecting Vault values into pods at admission |
| `bank-vaults` | the umbrella project, its CLI and shared libraries — the umbrella under which the other two sit |

The project was reorganised from a single `bank-vaults` repository into separate ones, so older
documentation refers to paths and binaries that have since moved. When following a tutorial, check
which era it was written in.

`secrets-webhook` is the one to consider alongside the operator: it makes the Bank-Vaults stack
end-to-end, replacing the need for external-secrets or the Vault agent injector.

### How it is deployed here

Three files, and the deployment is the least finished in this subtree:

`helm/ocirepository.yaml` — an `OCIRepository` in `flux-system` pointing at
`oci://ghcr.io/bank-vaults/helm-charts/vault-operator`, with the `ref.tag` block **commented out**:

```yaml
  #ref:
   # tag: v5.17.0
```

Without a `ref`, Flux resolves the `latest` tag. For a component that would own the lifecycle of the
cluster's secret store, an unpinned chart means an unattended upgrade at some future reconcile. The
tag is right there in a comment; uncommenting it is the fix. Compare with the
[Kyverno](../../../../policies/kyverno/README.md) and [OpenBao](../../openbao/README.md)
`OCIRepository` files in this repo, which pin both a tag and a digest.

`helm/helmrelease.yaml` — a `HelmRelease` referencing that source with **no values**, and a comment
pointing at `https://github.com/bank-vaults/vault-helm-chart/blob/main/vault/values.yaml`.

`namespace.yaml` — the `vault-operator` namespace.

**No `Vault` custom resource exists anywhere in this repository.** The operator would install and
have nothing to reconcile — which means the one capability that justifies it, declarative Vault
configuration, is not being used.

### Why this folder is worth more than it looks

The [`../vault/`](../vault/README.md) deployment has two properties that are recorded there as
compromises:

1. Its configuration — engines, policies, tokens — exists only as `init.sh`, a written procedure
   nobody can apply automatically.
2. It auto-unseals with `VAULT_AUTO_UNSEAL_KEY_0: pikakube` in the HelmRelease, which puts the unseal
   key in Git.

This operator addresses both directly: the `Vault` CR replaces the procedure, and KMS-backed unseal
key storage replaces the committed key. That makes it, on paper, the most valuable folder in
[`../`](../README.md) and the one with the least in it.

The honest counterweight: adopting it means moving off HashiCorp's chart, and it competes with
[vault-secrets-operator](../vault-secrets-operator/README.md) and
[external-secrets](../../../integrations/external-secrets/README.md) — which is the one actually
working here — for the same role. Three Vault-adjacent controllers installed is an evaluation set,
and the decision to make explicitly is which stack this platform runs: HashiCorp's, Bank-Vaults', or
the vendor-neutral one.

---

[← Vault](../README.md)
