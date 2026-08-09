[← Encryption at rest in Git](../README.md)

# SOPS

<https://github.com/getsops/sops>

Encrypts the **values** in a YAML, JSON, ENV or INI file while leaving the structure readable.
Recipients can be `age`, PGP, or a cloud KMS. Flux decrypts it natively.

---

## The problem it solves

A Kubernetes `Secret` is base64, not encryption, so committing one is committing a plaintext
credential. The usual alternatives are an external store — which must be running before anything else
can start — or encrypting the whole file, which turns every change into an opaque blob nobody can
review.

SOPS takes the third path: encrypt each **value**, leave the keys and structure in the clear.

```yaml
data:
    username: ENC[AES256_GCM,data:...,tag:...]
    password: ENC[AES256_GCM,data:...,tag:...]
sops:
    age:
        - recipient: age1p7zzz...
```

What that buys, and it is the whole argument for SOPS over the alternatives:

| Property | Consequence |
|---|---|
| Structure stays readable | `git diff` shows *which* secret changed and *which keys* were added or removed |
| Kubernetes metadata in the clear | tools can see `kind`, `metadata.name`, `namespace` before decryption |
| Reviewable | a reviewer can assess the shape of a change without being able to read the value |
| Per-value envelope encryption | a data key encrypts the values; the recipients encrypt the data key. Adding a recipient does not re-encrypt the data |

That last row is what makes multiple recipients practical: a file can be readable by your age key,
by a colleague's, and by a cloud KMS simultaneously, and adding a fourth is a metadata change rather
than a full re-encryption.

Recipients, and the trade between them:

| Recipient | Key lives | Revocable | Works offline |
|---|---|---|---|
| `age` | a file you hold | no — a leaked key is permanently valid for everything encrypted to it | yes |
| PGP | a keyring, possibly a hardware token | via revocation, awkwardly | yes |
| Cloud KMS (AWS, GCP, Azure, Vault Transit) | the KMS; it never leaves | yes — remove the IAM grant | no |

`age` is the simplest and the default choice for a local or single-operator setup. **KMS is the one
that means something operationally**, because access is IAM-controlled, audited, and revocable
without re-encrypting the repository.

## When to use it

- **Bootstrap secrets.** The credentials Flux itself needs, registry pull secrets, the things that
  must exist before Vault does. A store cannot hold the credential used to reach the store.
- **Flux is the delivery mechanism.** Flux decrypts SOPS natively — `decryption.provider: sops` on a
  Kustomization, with the key in a Secret. No extra controller, no CRDs, no webhook.
- **Cluster-level configuration that must not depend on a running service.** Anything on the critical
  path of the cluster coming up.
- **Air-gapped or local clusters.** No external system to reach.
- **You want the change history.** `git log` on an encrypted file is a real audit trail of *changes*
  — who, when, and in the same pull request as the code that needed it.
- **Multiple environments with different keys.** A `.sops.yaml` can route paths to different
  recipients, so a dev-laptop key cannot decrypt production.
- **Non-Kubernetes secrets too.** SOPS is not Kubernetes-specific — Terraform variables, CI
  configuration, `.env` files all work the same way.

## When not to use it

- **For credentials that need real rotation.** Rotation is a human editing a file and committing it.
  Nothing expires, nothing rotates on its own, and there are no dynamic secrets — see
  [`../../stores/`](../../stores/README.md#2-dynamic-secrets).
- **When you need to know who *read* a secret.** Git records changes, not decryptions. There is no
  read audit and no revocation of someone who already decrypted the file.
- **Where the ciphertext being permanent is unacceptable.** Git history is forever. A key
  compromised in three years decrypts everything committed today, including the credentials you
  rotated in between.
- **Many people need write access.** Everyone who can encrypt needs a key, everyone who can decrypt
  can read everything encrypted to that key, and there is no per-secret authorisation. A store has
  policies; SOPS has one key per audience.
- **The value must not be readable by any human.** Anyone with the key can decrypt locally. That is
  the feature that makes it convenient and the property that makes
  [sealed-secrets](../sealed-secrets/README.md) safer.
- **The secret is very large or binary.** SOPS is for structured configuration; the `sops -e` binary
  mode exists but is not what it is good at.

## Notes

Every original note from `doc.md`, translated and explained, plus the state of this folder.

### The Flux + SOPS reference

> <https://medium.com/picus-security-engineering/manage-your-secrets-with-mozilla-sops-and-gitops-toolkit-flux-cd-v2-7aa98f626001>

A write-up of the exact pattern this folder implements: SOPS-encrypted Secrets in Git, decrypted by
Flux v2 during reconciliation. Note "Mozilla SOPS" in the title — the project was originally
Mozilla's, was archived, and is now maintained under the CNCF as **getsops**, which is the repository
linked at the top. Older documentation and blog posts still say Mozilla, and the CLI is the same
tool.

The mechanism the article covers is the one worth knowing: Flux's `Kustomization` takes a
`decryption` block naming a provider (`sops`) and a Secret holding the private key. The
kustomize-controller decrypts in memory as it builds — nothing decrypted is ever written to the
cluster except the resulting `Secret`.

### The configuration here

`.sops.yaml` is three lines and every one of them is a decision:

```yaml
creation_rules:
  - path_regex: .*.yml
    encrypted_regex: '^(data|stringData)$'
    age: age1p7zzzyj6qajqqdy9qssz3exwn8hws9l5swjxqhx7ryuznhza0yjsaeast4
```

| Field | What it does | Worth noting |
|---|---|---|
| `path_regex: .*.yml` | which files this rule applies to | matches `.yml` — and the file beside it is `secret.yaml`. The unescaped `.` also matches any character, so `.yml` matches `ayml` too. Both are worth tightening to something like `\.ya?ml$` |
| `encrypted_regex: '^(data\|stringData)$'` | encrypt only these top-level keys | the setting that makes diffs reviewable — see [`../README.md`](../README.md#3-encrypt-the-values-not-the-file) |
| `age: age1p7zzz...` | the recipient | a **public** key, safe to commit. The corresponding private key is not in this repository, and must not be |

`secret.yaml` beside it is the plaintext form — a `Secret` named `my-secrets` with base64 values —
kept as an illustration of what gets encrypted. It is a demo credential (`teste` in both fields),
which is the only reason it is acceptable for it to be there in the clear. The naming is also the
reason the `path_regex` matters: a rule targeting `.yml` does not automatically cover a `.yaml` file.

### The commands

Not in the original notes, but the three that matter:

```
sops -e secret.yml > secret.enc.yml     # encrypt, using the matching creation rule
sops -d secret.enc.yml                  # decrypt to stdout
sops secret.enc.yml                     # open in $EDITOR, decrypted; re-encrypts on save
```

The third is the one to use day to day — editing in place means the plaintext never exists as a file
on disk.

`SOPS_AGE_KEY_FILE` points at the private key. On the cluster side, Flux reads it from a Secret in
`flux-system`; that Secret is the one thing that cannot itself be SOPS-encrypted, and it is the
bootstrap credential the whole scheme rests on.

### What is missing here

There is no `age` key backup procedure documented in this folder — unlike
[sealed-secrets](../sealed-secrets/README.md), which has one in `backup-secret/`. The failure mode is
identical: lose the private key and every file encrypted to that recipient is permanently
unreadable. That gap is worth closing before this is used for anything beyond a demo, and the
stronger fix is moving the recipient from a file-based `age` key to a KMS key, which makes the
backup question somebody else's problem and makes revocation possible.

---

[← Encryption at rest in Git](../README.md)
