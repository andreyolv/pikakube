[← Encryption at rest in Git](../README.md)

# helm-secrets

<https://github.com/jkroepke/helm-secrets>

A Helm CLI plugin that decrypts values files on the fly. A wrapper around
[SOPS](../sops/README.md) (and optionally Vault or other backends) for the specific case of
`helm install -f secrets.yaml`.

---

## The problem it solves

[SOPS](../sops/README.md) encrypts a file. That is enough when the file is a Kubernetes manifest
delivered by Flux, because Flux knows how to decrypt SOPS during reconciliation.

It is not enough when the file is a **Helm values file**, because `helm` does not know anything about
SOPS. Left alone, the options are all bad:

| Option | Problem |
|---|---|
| Decrypt to a temp file, run helm, delete it | the plaintext exists on disk; the cleanup is your job and it fails when the command does |
| Keep secret values in a separate unencrypted file | back to a plaintext credential outside Git, managed by hand |
| Put them in the chart | a plaintext credential in Git |

helm-secrets closes the gap by hooking Helm's plugin mechanism. It intercepts the values files
referenced with the `secrets://` prefix, decrypts them into a temporary location, hands the plaintext
path to Helm, and cleans up afterwards:

```
helm secrets install myapp ./chart -f secrets://values.enc.yaml
```

Everything else — which recipient, which key, which files — is SOPS configuration and behaves exactly
as it does anywhere else, driven by `.sops.yaml`.

It also supports non-SOPS backends (Vault, AWS Secrets Manager, and others) through a
`ref+`-style URI syntax that resolves values at render time, which makes it a lightweight
alternative to [argocd-vault-plugin](../../integrations/argocd-vault-plugin/README.md) for teams
using the Helm CLI directly.

## When to use it

- **You run `helm` from a terminal or a CI job.** This is the case it exists for. If the workflow is
  `helm upgrade --install` in a pipeline, this is the missing piece.
- **Chart values contain credentials.** Database passwords, API keys, and license keys that arrive
  as chart values rather than as separate `Secret` objects.
- **You are already using SOPS.** Same `.sops.yaml`, same keys, same recipients — no new key
  management, no new concepts.
- **You want `helm diff` to work against encrypted values.** The plugin composes with `helm-diff`,
  which is the practical reason people install it: seeing what a release would change without
  decrypting anything by hand.
- **You want the values file reviewable.** SOPS's `encrypted_regex` still applies, so structure stays
  visible.

## When not to use it

- **The platform delivers charts through a GitOps controller.** This is the decisive point for this
  repository. Flux's `HelmRelease` and Argo CD's `Application` render charts inside a controller, not
  through the local `helm` binary, so a CLI plugin has nothing to hook.
  - With **Flux**, the native answer is SOPS-encrypted `Secret` objects plus
    `spec.valuesFrom` on the `HelmRelease`, referencing them. That is what
    [kubescape](../../../posture/kubescape/README.md) does in this repo — its account and access key
    come from a Secret via `valuesFrom` with `targetPath`.
  - With **Argo CD**, it is a config management plugin —
    [argocd-vault-plugin](../../integrations/argocd-vault-plugin/README.md), or the Helm plugin
    support in a custom CMP.
- **Secrets should not be chart values at all.** Passing a credential as a Helm value means it ends
  up in the release's stored manifest in the cluster, readable by anyone who can run
  `helm get manifest`. Referencing an existing `Secret` by name is a better shape, and most charts
  support it.
- **You want rotation, expiry or audit.** It inherits every limitation of
  [`../`](../README.md#5-what-this-approach-cannot-do): static credentials, no read audit, permanent
  ciphertext in Git history.
- **You want fewer moving parts in CI.** It is another plugin to install and version in every place
  Helm runs — every developer laptop and every pipeline image.

## Notes

The original `doc.md` contained only the repository link, which is at the top of this file. What
follows is the state of this folder and why it looks the way it does.

### There is nothing else in this folder

No chart, no HelmRelease, no example. That is correct, and worth stating explicitly rather than
reading as an omission: **helm-secrets is a client-side CLI plugin.** It is installed with
`helm plugin install https://github.com/jkroepke/helm-secrets` on a workstation or into a CI image.
It never runs in the cluster, so there is nothing for Flux to deliver and nothing to configure here.

That is also why it is unlikely to become more than a reference in this repository: this platform
delivers charts through Flux `HelmRelease` resources, and the local `helm` binary is not in the
delivery path.

### Where it sits against the neighbours

| | [SOPS](../sops/README.md) | **helm-secrets** | [sealed-secrets](../sealed-secrets/README.md) |
|---|---|---|---|
| What it encrypts | any structured file | Helm **values** files, via SOPS | Kubernetes `Secret` objects |
| Runs | CLI, and inside Flux | Helm CLI plugin | a controller in the cluster |
| Decryption happens | at reconcile, or locally | at `helm` invocation | in the cluster |
| Needs a cluster component | no | no | yes |
| Useful in this repo | yes — Flux decrypts natively | not in the delivery path | yes |

helm-secrets is not an alternative to SOPS; it is SOPS applied at a different point in the pipeline.
Anyone choosing between the two is asking the wrong question — the real question is where the chart
gets rendered.

### If it were adopted

The things to settle first:

- **Which recipient.** It uses the same `.sops.yaml` mechanism, so an `age` key or a KMS key, with
  the same backup and revocation questions as [SOPS](../sops/README.md).
- **Where the plugin is installed.** Every laptop and every CI image, at a pinned version.
- **Whether the credential belongs in values at all.** Helm stores the rendered release in the
  cluster, so a value passed this way is retrievable with `helm get manifest`. Referencing a `Secret`
  by name keeps it out of the release history.

---

[← Encryption at rest in Git](../README.md)
