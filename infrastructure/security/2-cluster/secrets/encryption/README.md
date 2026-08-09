[← Secrets](../README.md)

# Encryption at rest in Git

The secret lives in the repository, encrypted. No extra system has to be running for the platform to
come up.

Tools: [`sops/`](sops/README.md) — encrypt values with age, KMS or PGP ·
[`sealed-secrets/`](sealed-secrets/README.md) — encrypted so that only one specific cluster can
decrypt · [`helm-secrets/`](helm-secrets/README.md) — SOPS for Helm values files

## Contents

1. [Why this approach exists](#1-why-this-approach-exists)
2. [The two models](#2-the-two-models)
   - [Asymmetric to a cluster: sealed-secrets](#asymmetric-to-a-cluster-sealed-secrets)
   - [Encrypt to a key you hold: SOPS](#encrypt-to-a-key-you-hold-sops)
3. [Encrypt the values, not the file](#3-encrypt-the-values-not-the-file)
4. [Key management is the whole risk](#4-key-management-is-the-whole-risk)
5. [What this approach cannot do](#5-what-this-approach-cannot-do)
6. [Anti-patterns](#6-anti-patterns)
7. [How this applies to pikakube](#7-how-this-applies-to-pikakube)

---

## 1. Why this approach exists

GitOps wants one source of truth: the repository. Secrets break that, because a plain Kubernetes
`Secret` in Git is a plaintext credential in Git — base64 is an encoding, not a cipher.

The two ways out are "keep the secret somewhere else and fetch it" ([`../stores/`](../stores/README.md))
or "keep it in Git but encrypted". This folder is the second.

What that buys you:

| Property | Why it matters |
|---|---|
| No runtime dependency | the cluster can bootstrap with nothing else running — no Vault to unseal first |
| Version history | `git log` shows when a credential changed and who changed it |
| Review | a secret change goes through the same pull request as everything else |
| Works anywhere | air-gapped, local Kind cluster, someone's laptop |
| One system fewer to operate | there is no HA stateful service on the critical path |

The bootstrap property is the strongest argument and the one most often overlooked. Something has to
provide the credentials that let the cluster reach the secret store. That something cannot itself be
the secret store.

## 2. The two models

They look similar and behave very differently at the moment you need to restore a cluster.

### Asymmetric to a cluster: sealed-secrets

A controller in the cluster generates a key pair. You encrypt with the **public** certificate using
`kubeseal`, commit a `SealedSecret`, and the controller decrypts it in-cluster and produces a
`Secret`.

The defining property: **only that cluster can decrypt.** Nobody — not you, not CI, not another
cluster — can read the value back, because the private key never leaves the controller. That is
excellent for confidentiality and awkward for everything else:

- The same encrypted file cannot be reused in a second cluster without re-sealing.
- Disaster recovery requires restoring the controller's keys, which means you must have backed them
  up. All of them, including the rotated ones.
- There is no local `decrypt` for a developer who wants to check what the value is.

### Encrypt to a key you hold: SOPS

SOPS encrypts to a recipient you control — an `age` key, a PGP key, or a cloud KMS key. Anything
holding that key can decrypt, anywhere.

That makes it portable across clusters, usable in CI, and decryptable on a laptop for debugging. It
also means the key is now a thing you have to protect and distribute, and if it leaks, every secret
in the repository's history leaks with it.

| | sealed-secrets | SOPS |
|---|---|---|
| Encrypts to | a specific cluster's controller | a key you hold (age / PGP / KMS) |
| Portable across clusters | no — re-seal per cluster | yes |
| Decryptable locally | no | yes |
| Flux support | via the controller producing a `Secret` | native — `decryption.provider: sops` on a Kustomization |
| Key lives | in the cluster, rotated automatically, old keys retained | wherever you put it — the hard part |
| Disaster recovery | restore the controller's key set | have the key |
| Multi-tenant safety | strong: a tenant cannot decrypt another's file | weaker: whoever has the key reads everything encrypted to it |

Neither is strictly better. sealed-secrets is safer by default and more painful to recover; SOPS is
more flexible and puts the entire burden on key hygiene. Using a **cloud KMS** as the SOPS recipient
gets you most of sealed-secrets' safety back, because the key never leaves the KMS and access is
IAM-controlled and audited.

## 3. Encrypt the values, not the file

The single most useful configuration detail in this folder. From `sops/.sops.yaml`:

```
encrypted_regex: '^(data|stringData)$'
```

This tells SOPS to encrypt only the values under `data` and `stringData`, leaving `apiVersion`,
`kind`, `metadata` and the key *names* in plaintext.

Why that matters:

- A diff shows *which* secret changed and *which keys* were added or removed. Encrypting the whole
  file makes every change an opaque blob.
- Kustomize and Flux can still see what kind of object it is before decryption.
- Reviewers can review the shape of the change without being able to read the value.

The trade-off is that key names are metadata you are choosing to leak — `AWS_SECRET_ACCESS_KEY`
tells a reader what kind of credential is there. That is almost always an acceptable trade for a
readable history.

## 4. Key management is the whole risk

Once the file is encrypted, the file stops being interesting and the key becomes the entire attack
surface and the entire operational burden.

**The failure that ends a platform:** the sealed-secrets private key is lost, and every
`SealedSecret` in the repository is permanently unreadable. Not "hard to recover" — the plaintext
does not exist anywhere else. This is why `sealed-secrets/backup-secret/` exists in this repo and
why that folder is the most important one in this subtree.

The rotation problem, per model:

| | Rotating one secret | Rotating the key |
|---|---|---|
| sealed-secrets | re-seal with the cluster's current public cert and commit | the controller creates new keys on a schedule and **retains the old ones** so existing files still decrypt; the key set only grows, and all of it must be backed up |
| SOPS | decrypt, edit, re-encrypt, commit | re-encrypt every file in the repository — mechanical, but touches everything |

A leak of an encrypted file is survivable if the key is intact. A leak of the key means every secret
ever committed is compromised, including the ones you rotated afterwards, because Git history is
forever.

Practical minimum:

1. Back up the key material somewhere that is not the same cluster and not the same repository.
2. Test the restore. A backup you have not restored from is a hypothesis.
3. Prefer a KMS recipient for SOPS over a file-based age key, so revocation is possible.

## 5. What this approach cannot do

Being honest about the ceiling:

| Limitation | Consequence |
|---|---|
| No dynamic secrets | every credential is static and long-lived; nothing generates a per-request database password with a TTL |
| No audit trail of *reads* | `git log` shows changes, not who decrypted what |
| No revocation | once decrypted into a `Secret`, it is a normal Secret with all the usual exposure |
| Rotation is a commit | which means it is a human action someone has to remember |
| Ciphertext is permanent | a compromised key retroactively exposes the entire history |

That last one is the argument for [`../stores/`](../stores/README.md): a store can change a value and
the old one simply stops existing. Git cannot forget.

## 6. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| A plain `Secret` in Git "just for now" | it is in history permanently, even after you delete it | encrypt before the first commit; if it happened, rotate the credential |
| No backup of the sealed-secrets keys | the repository becomes undecryptable if the cluster is lost | back up the full key set, and test the restore |
| Backing up only the current sealed-secrets key | older `SealedSecret` files need the older keys | back up everything labelled `sealedsecrets.bitnami.com/sealed-secrets-key` |
| Encrypting the whole YAML file | every change is an opaque diff and review is impossible | `encrypted_regex` on `data`/`stringData` |
| The age private key committed next to the encrypted files | the lock and the key in the same box | key outside the repo; better still, a KMS recipient |
| Sharing one key across environments | a dev-laptop compromise reads production secrets | separate keys per environment |
| Treating this as a substitute for a store for application credentials | no rotation, no dynamic secrets, no read audit | encryption for bootstrap and platform config; a store for application credentials |
| Rotating the credential but not the key after a key leak | old commits are still decryptable with the leaked key | rotate the key *and* every credential encrypted to it |

## 7. How this applies to pikakube

All three tools are present; SOPS and sealed-secrets are the ones with working configuration.

SOPS is set up as it should be: an `age` recipient in `.sops.yaml`, `encrypted_regex` scoped to
`data` and `stringData`, and a plain `secret.yaml` beside it showing the pre-encryption form. Flux
supports this natively, which makes it the natural choice for anything that must exist before the
rest of the platform does.

sealed-secrets is deployed with a HelmRelease, a worked `example/` showing the `kubeseal` flow, and
— the part that matters most — a `backup-secret/` folder documenting how to export the keys, apply
them to a new cluster, and use `--recovery-unseal` to recover a plaintext Secret from a
`SealedSecret` when you still hold the private key. That procedure is the difference between
sealed-secrets being safe and being a trap.

helm-secrets is a link and nothing else, which is a reasonable place for it to stay: this repo
delivers charts through Flux `HelmRelease` resources rather than by running `helm` locally, and
helm-secrets is a `helm` CLI plugin.

The honest division of labour for a platform like this one: use this folder for the bootstrap layer
— the credentials Flux itself needs, registry pull secrets, the things that must work before Vault
exists — and push application credentials towards [`../stores/`](../stores/README.md), where
rotation and read auditing are possible.

---

[← Secrets](../README.md)
