[← Secret integrations](../README.md)

# Secrets Store CSI Driver

<https://github.com/kubernetes-sigs/secrets-store-csi-driver>

Mounts secrets from an external store as files in a pod's volume. The only integration here that does
not create a Kubernetes `Secret`.

---

## The problem it solves

Every other way of getting a credential into a pod ends with a Kubernetes `Secret` object — base64 in
etcd, readable by anyone with `get secrets` in that namespace, present in every etcd backup. The
store was supposed to reduce exposure, and at the last step the credential lands in the least
protected place in the cluster.

The CSI driver does not do that. It is a Kubernetes SIG project that implements the Container Storage
Interface, so:

1. A `SecretProviderClass` describes where to fetch from and which objects to fetch.
2. A pod declares a CSI volume referencing it.
3. At mount time, the driver calls the provider, fetches the values, and writes them as **files** in
   the volume.
4. The credential exists in that pod's mount namespace, and nowhere else.

Someone with `get secrets` in the namespace gets nothing. Reading the value requires `exec` into that
specific pod. That is a genuine reduction in blast radius, and it is the only structural security
difference between the three options in [`../`](../README.md).

The driver itself is generic; the store-specific part is a **provider** installed alongside it —
Vault, Azure Key Vault, AWS, GCP. That two-part shape is worth knowing because "I installed the
driver and nothing works" is usually a missing provider.

Two things it also does:

- **Rotation.** With `enableSecretRotation`, it polls and rewrites the file when the value changes.
- **`syncSecret`.** Optionally mirrors the mounted values into a real Kubernetes `Secret` — which
  gives away the advantage above. See [`../README.md`](../README.md#why-syncsecret-gives-the-advantage-back).

## When to use it

- **You genuinely want no Kubernetes `Secret`.** This is the only reason to prefer it, and it is a
  good one — as long as `syncSecret` stays off.
- **The application reads files.** JKS truststores, kubeconfigs, service-account JSON, TLS material,
  anything that wants a path rather than an environment variable.
- **You want failure to be loud.** If the store is unreachable, the volume does not mount and the pod
  does not start. That is worse for availability and better for security than
  [external-secrets](../external-secrets/README.md), which serves a stale value indefinitely. Know
  which you signed up for.
- **You want rotation the app can pick up without a restart.** The file content changes in place, so
  an application that re-reads it gets the new value. That is more than a `Secret`-backed environment
  variable can do.
- **The cloud provider's own integration is this.** On AKS and EKS, the vendor-supported path for
  Key Vault / Secrets Manager is a provider for this driver.

## When not to use it

- **Anything consumes the credential by reference.** `imagePullSecrets`, Ingress TLS, most operators
  and most Helm charts want a `Secret` name. None of them can mount a volume. This is the constraint
  that pushes most deployments to `syncSecret` and therefore back to
  [external-secrets](../external-secrets/README.md), more simply.
- **`syncSecret` would be on globally.** Then you are paying CSI complexity — a DaemonSet, a
  provider, a `SecretProviderClass` per workload — and creating Secrets anyway.
- **The store's availability is not good enough.** A resealed Vault means every new pod that mounts a
  secret is stuck in `FailedMount`, cluster-wide, including during a node drain.
- **Many workloads need the same secret.** A `SecretProviderClass` is namespaced, and each pod mounts
  independently, so N pods means N fetches per rotation interval.
- **You want one API across stores.** Providers vary in maturity and in their configuration shape;
  ESO's abstraction is more uniform.

## Notes

There was no `doc.md` in this folder. `example/doc` contains a full worked tutorial against Vault —
translated, explained and preserved below — plus the state of the deployment.

### References collected

> <https://github.com/saiyam1814/csi-secret-store>
> <https://gist.github.com/vfarcic/f300b3452691346c8028fa62605c9ccc>
> <https://github.com/vfarcic/secrets-store-csi-demo/tree/main/k8s>
> <https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-secret-store-driver>
> <https://github.com/kubernetes-sigs/secrets-store-csi-driver/tree/main/test/bats/tests/vault>

Five references for the same integration. The last one is the most durable: the driver's own BATS
test suite for Vault is executable, maintained by the project, and updated when the API changes —
which blog posts are not.

### The worked tutorial, step by step

All commands from `example/doc`, in order.

**1. Put a secret in Vault.**

```bash
kubectl -n vault exec -it vault-0 -- /bin/sh

vault kv put secret/my-pass password="kubernetes"
vault kv get secret/my-pass
```

Executes into the Vault pod and writes a KV secret at `secret/my-pass`. The mount here is the default
`secret/` rather than the `pikakube` path used by
[external-secrets](../external-secrets/README.md) in this repo — the two examples were built
independently.

**2. Enable the Kubernetes auth method.**

```bash
vault auth enable kubernetes
vault write auth/kubernetes/config kubernetes_host="https://212.2.244.66:6443"
```

**This is the important step and the reason this example is worth more than the rest of the folder.**
It tells Vault to accept Kubernetes ServiceAccount tokens as proof of identity: Vault takes the
token, calls the API server's `TokenReview` to verify it, and maps the ServiceAccount to a policy.

No credential is stored anywhere. Contrast with
[external-secrets](../external-secrets/README.md) in this repo, which authenticates with a static
Vault token held in a Kubernetes Secret — a credential the store was supposed to remove.

The hard-coded IP is this cluster's API server address. On a real setup that is
`https://kubernetes.default.svc:443` from inside the cluster.

**3. Write a policy scoped to one path.**

```bash
vault policy write read-only - <<EOF
path "secret/data/my-pass" {
  capabilities = ["read"]
}
EOF
```

Read-only, one path, nothing else. Note `secret/data/my-pass` rather than `secret/my-pass`: KV v2
inserts `data/` into the API path, and the mismatch between the CLI path and the policy path is one
of the most common Vault mistakes.

**4. Bind a role to a specific ServiceAccount.**

```bash
vault write auth/kubernetes/role/mysecret \
    bound_service_account_names=secret-sa \
    bound_service_account_namespaces=secrets-store-csi-driver \
    policies=read-only \
    ttl=20m
```

This is the authorisation model in four lines: **only** the ServiceAccount `secret-sa`, **only** in
the namespace `secrets-store-csi-driver`, gets the `read-only` policy, and the resulting token lives
20 minutes.

Both `bound_` fields matter. Without the namespace binding, any namespace could create a
ServiceAccount called `secret-sa` and read the secret. That is the whole authorisation boundary.

**5. Read the file from inside the pod.**

```bash
cat /mnt/secrets-store/my-password
```

The payoff, and the demonstration of what makes this driver different: the credential is a file
inside the pod. `kubectl get secret -n secrets-store-csi-driver` shows nothing.

### The example manifests

| File | Role |
|---|---|
| `example/secretproviderclass.yaml` | `provider: vault`, `vaultAddress: http://vault.vault:8200`, `roleName: mysecret` — matching the role created in step 4 — and an `objects` list mapping `secret/data/my-pass` key `password` to the file name `my-password` |
| `example/sa.yaml` | the `secret-sa` ServiceAccount that the Vault role is bound to |
| `example/pod.yaml` | a busybox pod with `serviceAccountName: secret-sa` and a CSI volume with `driver: secrets-store.csi.k8s.io`, `readOnly: true`, `volumeAttributes.secretProviderClass: vault-connect`, mounted at `/mnt/secrets-store` |

The chain is worth tracing once: pod → ServiceAccount → Vault role binding → policy → path. Every
link is explicit and narrow, and that is what makes this the best-documented authentication example
in the repository.

### How it is deployed here

`helm/helmrelease.yaml`, chart `secrets-store-csi-driver` 1.3.4:

| Setting | Value | Comment |
|---|---|---|
| `syncSecret.enabled` | `true` | **creates a mirror Kubernetes `Secret`**, which removes the driver's main advantage |
| `enableSecretRotation` | `true` | poll for changes and rewrite the file |
| `rotationPollInterval` | `10s` | one request to the store per mounted secret per pod every ten seconds |

Both of those are demo settings rather than deployment settings, and they are worth stating plainly:
`syncSecret: true` means this deployment produces the same exposure as
[external-secrets](../external-secrets/README.md) with more machinery, and a ten-second poll is a
load generator against Vault at any real scale. Minutes is the production figure.

Note also that no **provider** is deployed in this folder. The driver alone cannot talk to Vault —
the Vault CSI provider is a separate DaemonSet — so the example above requires a component that is
not in this repository.

---

[← Secret integrations](../README.md)
