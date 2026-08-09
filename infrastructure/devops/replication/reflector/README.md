[← Replication](../README.md)

# Reflector

<https://github.com/emberstack/kubernetes-reflector>

---

## The problem it solves

`ConfigMap` and `Secret` are namespaced, and there is no built-in way to make one available in
another namespace. Every platform hits this within weeks:

- an `imagePullSecret` for a private registry, needed by every namespace that pulls an image
- a wildcard TLS certificate issued once, needed by Ingresses in six namespaces
- a shared CA bundle
- a licence key or a common configuration value

The alternatives without a tool are all bad: paste the Secret into every namespace's manifests and
watch them diverge, or write a `CronJob` that copies them and hope it is running.

Reflector watches source resources and mirrors them into other namespaces. What makes it
distinctive is that **the source declares the policy**:

| Annotation on the **source** | Effect |
|---|---|
| `reflector.v1.k8s.emberstack.com/reflection-allowed: "true"` | this resource may be mirrored at all |
| `reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: "ns1,ns2,namespace-.*"` | into which namespaces — literal names or regular expressions |
| `reflector.v1.k8s.emberstack.com/reflection-auto-enabled: "true"` | create the mirrors automatically, rather than waiting for a target to ask |
| `reflector.v1.k8s.emberstack.com/reflection-auto-namespaces: "..."` | where the automatic mirrors go |

Mirrors stay in sync: change the source and every copy updates. Reflector also has explicit
cert-manager awareness, which is why it turns up so often in TLS setups.

## When to use it

- `imagePullSecret` distribution — the single most common legitimate use, and the one with the
  weakest argument against it, since the credential is already effectively cluster-wide
- a wildcard TLS certificate that several namespaces' Ingresses need
- when the owner of the source resource should control who may copy it. The source-side
  `reflection-allowed` model is a real security property, not a convenience: a namespace cannot
  help itself to a Secret it was not offered

## When not to use it

- **for CA bundles.** [trust-manager](../../../security/2-cluster/certificates/trust-manager/README.md)
  is purpose-built for exactly that, merges the private CA with the public trust store, converts to
  JKS and PKCS#12 for JVM workloads, and restricts sources to a single trusted namespace. Reflector
  copies bytes and does none of it
- **for private keys.** A full TLS Secret replicated across ten namespaces is one private key with
  ten times the exposure. The correct answer is cert-manager issuing a certificate per namespace
- as a general answer to "several namespaces need this". Each replicated Secret weakens namespace
  isolation, and the isolation is usually the reason the namespaces exist
- if a policy engine is already deployed — Kyverno's `generate` rule does the same job with no
  additional component

## Notes

The only recorded reference is the repository:
<https://github.com/emberstack/kubernetes-reflector>.

**Deployed here**, via a Flux `HelmRelease` against the `emberstack` Helm repository, chart version
`7.1.262`, with default values. No example resources are recorded — unlike
[replicator](../replicator/README.md), which has a worked set — so this is deployed but not
demonstrated.

**Reflector versus [replicator](../replicator/README.md)** is the choice this folder exists to make,
and it comes down to which side declares the intent:

| | Reflector | Replicator |
|---|---|---|
| Policy lives on | the **source** — "who may copy me" | either side — push from the source, or pull from the target |
| Target selection | namespace names and regular expressions | namespace names, regular expressions, **and label selectors** |
| Resource kinds | ConfigMap, Secret | ConfigMap, Secret, **Role, RoleBinding, ServiceAccount** |
| cert-manager | explicit integration | none |

Reflector's source-only model is the safer default, because a namespace cannot pull in a Secret that
was not offered to it. Replicator's pull mode is more flexible and gives that property away. If
neither consideration decides it, having both deployed is the thing to avoid: two controllers
copying Secrets is twice the surface and twice the confusion when a copy is stale.

---

[← Replication](../README.md)
