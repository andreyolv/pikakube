[← Encryption at rest in Git](../README.md)

# Sealed Secrets

<https://github.com/bitnami-labs/sealed-secrets>
<https://github.com/bitnami-labs/sealed-secrets/blob/main/docs/bring-your-own-certificates.md>

A controller generates a key pair in the cluster. You encrypt with the public certificate using
`kubeseal`, commit the result, and **only that cluster can decrypt it**.

---

## The problem it solves

Committing a `Secret` to Git is committing a plaintext credential. Sealed Secrets makes the encrypted
form safe to commit and, unusually, safe to commit **publicly**: the private key never leaves the
controller, so nobody — not the author, not CI, not another cluster — can read the value back.

The flow:

```
secret.yaml  --kubeseal + public cert-->  sealed-secret.yaml  --commit-->  Git
                                                                            |
                                          controller (holds private key)  <-+
                                                                            |
                                                              Secret in the cluster
```

The `SealedSecret` CRD is a normal Kubernetes object with ciphertext in it. The controller watches
for them, decrypts, and creates the corresponding `Secret` as an owned resource — so deleting the
`SealedSecret` deletes the `Secret`.

Two properties define it, and they are the same property viewed from two sides:

| | Consequence |
|---|---|
| Only the cluster can decrypt | strongest confidentiality of anything in [`../`](../README.md) — a leaked repository leaks nothing |
| Only the cluster can decrypt | no local decrypt for debugging; no reuse across clusters without re-sealing; disaster recovery requires the key backup |

There is a scope field that is easy to get wrong and worth knowing up front. By default a
`SealedSecret` is bound to **both** its namespace and its name — the name and namespace are mixed
into the encryption — so the same ciphertext cannot be moved elsewhere by anyone who obtains it.
`--scope namespace-wide` relaxes the name binding; `--scope cluster-wide` relaxes both. Each
relaxation is a convenience and a small weakening: a cluster-wide sealed secret can be mounted into a
namespace it was never intended for.

## When to use it

- **A public or widely-readable repository.** This is where it beats [SOPS](../sops/README.md)
  outright. There is no key an attacker could obtain from the repo, from CI, or from a laptop.
- **You want the simplest possible key story.** No `age` key to distribute, no KMS to configure, no
  recipient management. The controller handles it.
- **Multi-tenant clusters.** A tenant cannot decrypt another tenant's sealed secret, and with the
  default scope cannot even reuse their own in another namespace.
- **Anything works, including Argo CD, Helm and plain kubectl.** It is a CRD and a controller, not a
  GitOps-engine feature. SOPS decryption in Flux is a Flux feature; this is not tied to anything.
- **Bootstrap secrets.** Like SOPS, it needs nothing running except the controller, so it works
  before a secret store exists.

## When not to use it

- **You have not planned the key backup.** This is not a nice-to-have. Lose the controller's keys and
  every `SealedSecret` in the repository is permanently unreadable — the plaintext exists nowhere
  else. The procedure is in the Notes below and it is the most important thing in this folder.
- **The same secret must exist in several clusters.** Each cluster has its own key, so the same
  plaintext must be sealed once per cluster. `bring-your-own-certificates` (linked above) is the
  escape hatch — a shared key pair across clusters — and it trades away the property that made
  sealed-secrets safe in the first place.
- **Developers need to read the value.** There is no local decrypt. `--recovery-unseal` exists and
  requires the private key, which is exactly what you were not distributing.
- **You need rotation, expiry or dynamic secrets.** Same ceiling as everything in
  [`../`](../README.md): every credential is static, and rotation is a human re-sealing a file.
- **You want a read audit.** Git records changes, not decryptions.
- **The credential is high-value and long-lived.** The ciphertext in Git is permanent. A compromise
  of the controller's key set retroactively exposes everything ever sealed to it.

## Notes

Every original note from `doc.md` and from `backup-secret/tutorial`, translated and explained, plus
the state of this folder.

### Bring your own certificates

> <https://github.com/bitnami-labs/sealed-secrets/blob/main/docs/bring-your-own-certificates.md>

The documented way to supply your own key pair instead of letting the controller generate one. Two
reasons it matters:

1. **Disaster recovery becomes predictable.** With a key you generated, restoring a cluster is
   "apply the key Secret first" rather than "restore whatever the controller happened to create".
2. **Several clusters can share a key**, so one sealed file works everywhere.

The second is a real trade-off, not a free win: the whole security argument for sealed-secrets is
that the private key exists in exactly one place. A key you generated and copied to three clusters is
a key that exists in four places, and it is now your job to protect it — at which point
[SOPS](../sops/README.md) with a KMS recipient is a more honest version of the same design.

It also affects the recovery procedure below: whether the key was generated by the controller or
supplied by you changes how you get a usable PEM out of it.

### Key backup and recovery

From `backup-secret/tutorial`, translated:

> **BACKING UP THE KEYS**
> ```bash
> kubectl get secret -l sealedsecrets.bitnami.com/sealed-secrets-key -o yaml > main.key
> ```

The label selector is the important part. The controller creates a **new key pair periodically** and
keeps the old ones, so that previously-sealed secrets still decrypt. That means:

- The set of keys **grows over time**.
- Backing up only the current one is not enough — older `SealedSecret` files need the older keys.
- The label is what selects all of them at once. Any backup that names a single Secret is wrong.

This command should be run against the controller's namespace (`sealed-secrets` here) and the output
is a plaintext private key. Where `main.key` is then stored is the whole security of the scheme: not
in this repository, not in the same cluster, and encrypted at rest wherever it lands.

> **APPLYING THE KEYS TO THE CLUSTER**
> ```bash
> kubectl apply -f main.key
> ```

Restoring into a rebuilt cluster. Apply the keys **before** the controller starts, or restart it
afterwards — it loads keys at startup. Once they are present, every existing `SealedSecret` in the
repository decrypts again and the cluster rebuilds itself from Git.

> **IF IT WAS GENERATED AUTOMATICALLY, CONVERT .key TO .pem WITH:**
> ```bash
> openssl rsa -in tls.key -out tls.pem
> ```
> **IF IT WAS GENERATED MANUALLY, tls.pem = tls.key from main.key**

The key Secret is a `kubernetes.io/tls` type, so it holds `tls.crt` (the public certificate) and
`tls.key` (the private key), base64-encoded. `kubeseal --recovery-private-key` wants a PEM file.

For a controller-generated key, `openssl rsa` converts the extracted `tls.key` into the PEM form the
CLI expects. For a key you generated yourself — the bring-your-own-certificates path — it is already
in that form and no conversion is needed. That distinction is why the note has two branches.

> **RECOVERING THE PLAINTEXT**
> ```bash
> kubeseal --format=yaml --recovery-unseal --recovery-private-key tls.pem < sealed-secret.yaml > recoverySecret.yaml
> ```

The escape hatch: given the private key, turn a `SealedSecret` back into a plain `Secret` **offline**,
without a running controller or cluster.

This is what you do when a cluster is gone and you need the credentials back, or when you need to
verify what a sealed file actually contains. It is also the clearest possible demonstration of what
the key is worth: whoever holds `tls.pem` can decrypt every sealed secret ever produced by that
controller.

`backup-secret/` contains `sealed-secret.yaml` and `recoverySecret.yaml` — the input and output of
exactly this command, kept as a worked example.

### Sealing a secret

`example/encrypt.sh`:

```bash
# Usage: encrypt.sh <secret.yaml>
# Needs to have kubeseal cli installed
# kubeseal --cert pub-cert.pem -f secret.yaml -o yaml > sealed-secret.yaml

kubeseal --cert pub-cert.pem <"$1" >"${1%.*}-sealed.yaml" -o yaml
```

A thin wrapper: take a plain `Secret`, produce `<name>-sealed.yaml` beside it. `${1%.*}` strips the
extension.

The `--cert pub-cert.pem` flag is what makes this work **offline**. Without it, `kubeseal` contacts
the controller to fetch the public certificate, which requires cluster access. With a fetched
certificate on disk, anyone can seal a secret from anywhere — including CI — with no cluster
credentials at all. That is a genuinely useful property and the reason to keep the public cert
around.

Fetching it is documented in the HelmRelease comments:

```bash
kubeseal --fetch-cert --controller-name=sealed-secrets --controller-namespace=sealed-secrets > pub-cert.pem
```

Both flags are needed because this deployment does not use the chart's default names.

`example/` also holds `secret.yaml` (the plaintext input) and `sealed-secret.yaml` (the output), so
the whole round trip is readable in one place.

### How it is deployed here

`helm/helmrelease.yaml`, chart `sealed-secrets` 2.14.1 into the `sealed-secrets` namespace, with
`install.crds: Create` and `upgrade.crds: CreateReplace` — the correct settings, since Helm does not
upgrade CRDs on its own and the `SealedSecret` CRD is the whole interface.

No values are set beyond that. The two `kubeseal` commands are kept as comments in the HelmRelease,
which is a reasonable place for them but not a substitute for the backup procedure above being run
on a schedule rather than by hand.

The one thing this folder documents better than most: **the recovery path is written down and there
is a worked example of it.** That is the difference between sealed-secrets being safe and being a
trap, and it is missing from the [SOPS](../sops/README.md) folder next door.

---

[← Encryption at rest in Git](../README.md)
