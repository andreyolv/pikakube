[← Kyverno policies](../README.md)

# sync-secret

<https://kyverno.io/docs/writing-policies/generate/>

A Kyverno `generate` policy that clones a TLS Secret from one namespace into every other namespace,
and keeps the copies in sync.

---

## The problem it solves

`Secret` and `ConfigMap` are namespaced, and Kubernetes has no native way to say "this one should
exist everywhere". Anything that needs the same Secret in many namespaces — a TLS certificate for
ingress, an image-pull credential, a CA bundle — hits this immediately.

The three ways out without a tool are all bad: copy it by hand and watch it drift, script it and
watch the script rot, or give up and use a different certificate per namespace.

`sync-tls-secret.yaml` here does it as a policy:

```yaml
generate:
  generateExisting: true
  apiVersion: v1
  kind: Secret
  name: mkcert-tls-secret
  namespace: "{{request.object.metadata.name}}"
  synchronize: true
  clone:
    namespace: ingress-nginx
    name: mkcert-tls-secret
```

Read it as: when a `Namespace` is admitted, create a Secret named `mkcert-tls-secret` **in that new
namespace** (`{{request.object.metadata.name}}` is the namespace's own name), cloned from
`ingress-nginx/mkcert-tls-secret`.

The three flags that make it work:

| Field | Without it |
|---|---|
| `clone` | you would have to inline the Secret's data in the policy — a credential in Git |
| `synchronize: true` | the copies never receive updates, and deleting one does not bring it back |
| `generateExisting: true` | only namespaces created *after* the policy is applied get the Secret |

`rbac.yaml` beside it grants what Kyverno needs to do this: `kyverno:secrets:view` (get/list/watch,
aggregated to the admission, reports and background controllers) and `kyverno:secrets:manage`
(create/update/delete, aggregated to the background controller only). Kyverno does not have Secret
access by default, and this is why.

## When to use it

- **A cluster-wide TLS certificate.** The case here: mkcert issues one certificate for
  `*.127.0.0.1.nip.io`, and every ingress in the cluster wants it.
- **Image-pull credentials.** A `dockerconfigjson` Secret that every namespace needs and nobody
  should have to remember to create.
- **You already run Kyverno.** This is the "install nothing new" answer. A dedicated replication
  controller (Reflector, Replicator) does the same job; if Kyverno is present, a policy is one file
  instead of another Deployment.
- **Any per-namespace default.** The same `generate` mechanism produces a default NetworkPolicy, a
  ResourceQuota, or a LimitRange. Those are better uses of it than Secrets, because they carry no
  key material.

## When not to use it

- **The Secret contains a private key.** This one does — a TLS Secret is a certificate *and* its
  key. Cloning it means the key exists in every namespace, so compromising any namespace leaks it.
  For a local mkcert certificate that is an acceptable trade; for a real certificate it is not, and
  the correct answer is per-namespace **re-issuance** by cert-manager rather than replication.
- **You only need to distribute public trust material.** Distributing CA bundles (no keys) is what
  `certificates/trust-manager` is for, and it does things a generic clone cannot — merging with the
  public CA bundle, converting to JKS/PKCS#12, and restricting which namespace may act as a source.
- **The Secret differs per namespace.** `generate` clones; it does not template per target.
- **Kyverno should not have Secret access.** Applying the RBAC here means the Kyverno controllers can
  read every Secret in the cluster and write Secrets anywhere. That is a real increase in the value
  of compromising Kyverno, and it should be a decision rather than a side effect.

## Notes

Every original note from `doc.md`, translated and explained.

### It only covers new namespaces

> Fine, but it only works for namespaces created from now on; not for old ones.

This is the defining limitation of `generate`, and it is why the policy in this folder carries
`generateExisting: true`. A `generate` rule is triggered by an admission event — a namespace being
created — so without that flag the rule never fires for namespaces that already exist.

`generateExisting: true` makes Kyverno's background controller sweep existing matching resources and
apply the rule to them as well. It is the flag that turns "from now on" into "everywhere", and the
note is the record of discovering that the hard way.

The same trap applies to `mutate` rules; the Kyverno answer there is `mutateExistingOnPolicyUpdate`,
and [`../../examples/label-existing-namespaces/`](../../examples/README.md) is the worked example.

### Applying it

> ```
> kubectl apply -f
> rbac
> secret
> clusterpolicy
> namespace
> ```

The order to apply the four pieces in, and the order is not arbitrary:

1. **rbac** — Kyverno cannot read or create Secrets without it, so applying the policy first
   produces a rule that fails silently with a permissions error in the controller log.
2. **secret** — the source Secret must exist in `ingress-nginx` before anything can be cloned from
   it. In this repo the source is created by mkcert and cert-manager, not by a file here.
3. **clusterpolicy** — `sync-tls-secret.yaml`.
4. **namespace** — creating a namespace is what triggers the rule, so this is the test.

The `kubectl apply -f` prefix with no filename is shorthand in the original note, not a command to
run verbatim. Note also that applying by hand is itself the finding: none of this is in the Kyverno
`kustomization.yaml`, so Flux does not deliver it.

### Verifying it worked

> ```
> k get secret -n foobar2
> ```

After creating a namespace (`foobar2` here), list its Secrets. `mkcert-tls-secret` should be present
without anyone having created it. If it is not, the two things to check are the Kyverno background
controller's logs and whether the RBAC was applied.

`../../examples/namespace.yaml` in this repo creates a namespace called `foobar`, which is the same
test with a different number.

---

[← Kyverno policies](../README.md)
