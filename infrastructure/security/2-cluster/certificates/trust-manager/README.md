# trust-manager

<https://github.com/cert-manager/trust-manager>
<https://cert-manager.io/docs/trust/trust-manager/>

Official cert-manager subproject. Distributes **trust bundles** (the CAs that are trusted)
to every namespace in the cluster.

Context and comparison against the other tools: [../README.md](../README.md)

---

## The problem

Kubernetes has no native mechanism to distribute a CA bundle — `ConfigMap` and `Secret` are
namespaced. Whenever a private CA is in play, every workload that needs to *validate* an
internal endpoint needs that CA in its truststore.

Without a solution there are three ways out, all bad:

1. bake the CA into the base image → rotating the CA forces a rebuild of everything
2. copy a ConfigMap namespace by namespace → it drifts, and nobody knows which copy is right
3. `insecureSkipVerify: true` → what actually happens most of the time

## What it does

A `Bundle` CRD, **cluster-scoped**. You declare:

- **sources** — where the trust material comes from
- **target** — which ConfigMap/Secret to create, and in which namespaces

and it materialises and keeps them in sync. Rotating or renaming the CA becomes a single
resource edit.

### Available sources

| Source | What it is |
|---|---|
| `useDefaultCAs: true` | the public (Mozilla) bundle shipped inside the trust-manager image |
| `configMap` | a ConfigMap from the trust namespace |
| `secret` | a Secret from the trust namespace — typically the `ca.crt` produced by a cert-manager `Certificate` |
| `inLine` | PEM pasted directly into the resource |

### Targets

A ConfigMap or Secret, replicated by `namespaceSelector`. Supported formats:

- **PEM** — the default, for most workloads
- **JKS** and **PKCS#12** — for the JVM

---

## The three details that justify its existence

Without them it would be just another ConfigMap replicator.

**1. `useDefaultCAs` plus the private CA in one bundle.**
Mounting *only* the internal CA breaks TLS to every public endpoint. trust-manager merges
both into a single file. This is the most common mistake when people assemble it by hand.

**2. Conversion to JKS / PKCS#12.**
Kafka, Spark, Trino and Airflow-with-JDBC are JVM workloads and want a JKS truststore, not
PEM. The alternative is a `keytool` initContainer in every chart. For pikakube, which is a
data platform, this is the strongest argument.

**3. Sources restricted to a single namespace.**
It only reads sources from the *trust namespace* (default: `cert-manager`). This is
deliberate: a compromised namespace cannot inject a CA into the whole cluster. A generic
replicator has no such property — whoever controls the source Secret controls everyone's
trust.

---

## What it deliberately does NOT do

It only distributes **public trust material**. By design it refuses to handle private keys.

So it does **not** replace reflector/replicator for:

- a full TLS Secret (certificate + key) needed by several namespaces
- `imagePullSecret` (`dockerconfigjson`)
- generic application ConfigMaps or Secrets

For the TLS Secret case the right answer is not replication anyway: it is cert-manager
**re-issuing** per namespace. Private keys should not travel.

---

## Relationship to the rest of the folder

| Tool | Role | Relationship |
|---|---|---|
| cert-manager | issues certificates | **required pair** — one issues, the other makes them trusted |
| `cainjector` (inside cert-manager) | injects CA data into webhooks and CRD conversion | scoped to the **control plane**, not workloads — not an alternative |
| mkcert | local dev CA | a possible CA source for a Bundle |
| step-ca | private CA as a service | a possible CA source for a Bundle |

Alternatives mapped elsewhere in the repo, and why they do not cover the same ground:

| Alternative | Where it lives | Limitation |
|---|---|---|
| Reflector | `devops/replication/reflector` | copies bytes; no merge with public CAs, no JKS, no restricted source |
| Replicator | `devops/replication/replicator` | same |
| Kyverno `generate` | `security/2-cluster/policies/kyverno` | same — but it is the "install nothing new" option |
| SPIRE | `security/2-cluster/identity-access/authentication/workload-identity/spire` | solves trust via SPIFFE; does not cover anything that does not speak SPIFFE (Postgres, Kafka, S3, external APIs) |
| Service mesh | `network/service-mesh/` | only covers traffic inside the mesh |
| CA baked into the base image | `security/3-container/base-images` | kills rotation |

---

## When it is NOT worth installing

If the cluster only consumes certificates from public CAs, trust-manager adds almost
nothing — the Mozilla bundle already present in every image covers it. It earns its place
when a **private CA is in use**.

In pikakube one is: mkcert, step-ca and the cert-manager CA issuer.

---

## Requirements

- cert-manager installed (trust-manager uses it to issue its own webhook certificate)
- chart lives in the Jetstack Helm repository, the same one cert-manager already uses
- runs in the cert-manager namespace by default, which is also the default trust namespace
