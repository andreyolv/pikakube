[← Secret integrations](../README.md)

# Argo CD Vault Plugin

<https://github.com/argoproj-labs/argocd-vault-plugin>

Substitutes placeholders in manifests with values from a secret store, at the moment Argo CD renders
an Application. Text substitution, not an operator.

---

## The problem it solves

The other two integrations in [`../`](../README.md) are controllers: something runs in the cluster,
watches a CRD, and reconciles a value from a store into a `Secret` or a volume. That means another
component, another set of CRDs, and another thing on the critical path.

argocd-vault-plugin takes a different route. Argo CD already renders manifests — Helm templates,
Kustomize overlays, plain YAML — before applying them. The plugin hooks that render step and
substitutes placeholders:

```yaml
kind: Secret
metadata:
  name: example-secret
  annotations:
    avp.kubernetes.io/path: "path/to/secret"
data:
  password: <password-vault-key>
```

At render time, `<password-vault-key>` is replaced with the value read from the store at
`path/to/secret`. There is no CRD, no operator, and no reconciliation loop — the credential is
resolved once, into the manifest Argo CD then applies.

Two placeholder styles:

| Style | Form |
|---|---|
| Path annotation plus key name | `avp.kubernetes.io/path` on the object, `<key>` in the value |
| Inline path | `<path:secret/data/foo#bar>` directly in the value |

The first is tidier when every value in an object comes from one path; the second is necessary when
they come from several.

`avp.kubernetes.io/secret-version` (commented out in `secret.yaml` here) pins a KV v2 version, which
makes the render reproducible rather than "whatever is current".

It supports many backends — Vault, AWS Secrets Manager, Azure Key Vault, GCP, 1Password, SOPS,
Kubernetes Secrets — so it is not Vault-specific despite the name.

## When to use it

- **Argo CD is the delivery mechanism.** This is the only condition under which it works at all. It
  is a config management plugin; nothing else invokes it.
- **You want no additional controller.** No CRDs, no operator, no reconciliation loop. Argo CD is
  already there and already renders manifests.
- **The values change rarely.** Static configuration credentials, license keys, third-party API
  tokens.
- **You want the credential resolved before it reaches the cluster.** The rendered manifest is what
  Argo CD diffs and applies, so the value is decided at sync time rather than by a controller later.
- **Existing manifests should keep working.** The placeholders sit inside otherwise normal YAML, so
  adopting it does not mean rewriting anything into a new CRD.

## When not to use it

- **The platform delivers with Flux.** This is decisive for this repository — and see the Notes.
  There is no equivalent hook in Flux's `Kustomization` or `HelmRelease`.
- **The credential rotates.** The value is baked into the rendered manifest and only changes when
  Argo CD re-renders. Until the next sync, the cluster keeps the old credential. For a short-TTL or
  dynamic secret, this is the wrong mechanism entirely.
- **You want a resource that reports its own health.** An `ExternalSecret` has a status condition you
  can alert on. A substitution failure is a sync failure — visible, but only in Argo CD's own
  reporting.
- **Secrets should not appear in the rendered manifest.** They do. Argo CD's diff view, its manifest
  cache and its API can expose the resolved values, so `get applications` becomes another way to
  read credentials. Argo CD's RBAC is now part of the secrets threat model.
- **The repo-server is shared across tenants.** The plugin runs there with the store credentials
  available to it, so any Application rendered by that repo-server can reach anything those
  credentials permit.
- **You need per-namespace store credentials.** Authentication is configured for the plugin, not per
  Application.

## Notes

The original `doc.md` contained only the repository link, which is at the top of this file. What
follows is the state of this folder and how to read the two manifests in it.

### This platform uses Flux, not Argo CD

The most important thing about this folder. `pikakube` delivers with Flux — `HelmRelease`,
`Kustomization`, `OCIRepository` — and there is no Argo CD in it. A config management plugin for Argo
CD has nothing to plug into.

So this is a reference for what the Argo CD approach looks like, kept for comparison. It is not going
to run here, and the equivalent capability in Flux is either SOPS-encrypted Secrets decrypted natively
by the kustomize-controller ([`../../encryption/sops/`](../../encryption/sops/README.md)) or
[external-secrets](../external-secrets/README.md), which is the one actually wired up.

### The sidecar installation, explained

`cmp-plugin.yaml` and `deployment.yaml` together are the standard "config management plugin as a
sidecar" pattern, which is worth understanding because it is how every Argo CD plugin is installed
since v2.4.

`cmp-plugin.yaml` is a ConfigMap holding a `ConfigManagementPlugin` definition with two blocks:

| Block | What it does |
|---|---|
| `discover.find.command` | how Argo CD decides this plugin applies to a directory. Here: `find . -name '*.yaml' \| xargs -I {} grep "<path\|avp\.kubernetes\.io" {} \| grep .` — literally grep the manifests for either placeholder style |
| `generate.command` | `argocd-vault-plugin generate .` — the substitution itself |

The `discover` block is the whole plugin-selection mechanism made visible: Argo CD runs that command
in the Application's directory, and a non-empty result means "this plugin handles it". Applications
with no placeholders are rendered normally.

`deployment.yaml` patches `argocd-repo-server` with three pieces:

1. An **init container** that downloads the `argocd-vault-plugin` binary (pinned to `AVP_VERSION`
   1.16.1) into a shared `emptyDir`. Note it pulls from GitHub at pod start, so the repo-server now
   depends on GitHub being reachable when it restarts — a pre-baked image avoids that.
2. A **sidecar container** (`avp`) running `argocd-cmp-server`, with the plugin definition mounted at
   `/home/argocd/cmp-server/config/plugin.yaml` and the binary mounted into `$PATH`.
3. The shared volumes tying them together.

Both files have `namespace:` left empty, so this is a template to be filled in rather than something
to apply.

What is **not** here, and would be required: the store credentials. The plugin reads its
configuration from environment variables or a Secret on the repo-server (`VAULT_ADDR`,
`AVP_TYPE`, `AVP_AUTH_TYPE`, and the credential itself). That is the piece that makes the
repo-server a high-value target, and it is worth planning before adopting this.

### `secret.yaml`, and what it demonstrates

```yaml
metadata:
  annotations:
    avp.kubernetes.io/path: "path/to/secret"
    # avp.kubernetes.io/secret-version: "2"
data:
  password: <password-vault-key> # cGFzc3dvcmQK
```

The `data` field is a placeholder, not base64, and that is the point — the manifest in Git contains
no credential. The trailing comment `cGFzc3dvcmQK` is the base64 of `password`, left as an
illustration of what the substituted result looks like.

The commented-out `secret-version` annotation is worth uncommenting in real use: without it, the
render takes whatever version is current in the store, so the same Git commit can produce different
results at different times. Pinning the version makes the deployment reproducible — at the cost of
having to bump it when the secret changes, which is the same trade-off the whole approach makes.

---

[← Secret integrations](../README.md)
