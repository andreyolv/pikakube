[← Replication](../README.md)

# Replicator

<https://github.com/mittwald/kubernetes-replicator>

---

## The problem it solves

The same problem as [Reflector](../reflector/README.md) — namespaced resources that several
namespaces need — with two differences that decide when to pick it.

**It replicates more than ConfigMaps and Secrets.** It also handles `Role`, `RoleBinding` and
`ServiceAccount`, which matters when what needs standardising across namespaces is *access* rather
than *data*.

**It works in both directions.**

| Mode | Annotations | Who decides |
|---|---|---|
| **Push** | on the source: `replicator.v1.mittwald.de/replicate-to: "foo,bar"` | the source pushes into named namespaces |
| **Push by label** | on the source: `replicator.v1.mittwald.de/replicate-to-matching: "team=data"` | the source pushes into namespaces matching a label selector |
| **Pull** | on the source: `replicator.v1.mittwald.de/replication-allowed: "true"`, plus on the target: `replicator.v1.mittwald.de/replicate-from: "namespace/name"` | the target asks; the source must have consented |

Push-by-label is the capability Reflector does not have, and it is genuinely useful: label a
namespace and it receives the registry credential, with no list to maintain anywhere.

Replicas stay in sync with the source, and removing the annotation stops the replication.

## When to use it

- **`Role`, `RoleBinding` or `ServiceAccount` need to be identical across many namespaces** — this
  is the case Reflector cannot cover at all
- namespaces should receive shared resources by **label** rather than by being named — the
  onboarding case, where a new team's namespace should just work
- when the natural place to express the intent is the target ("this namespace needs that Secret")
  rather than the source

## When not to use it

- **for CA bundles** — use
  [trust-manager](../../../security/2-cluster/certificates/trust-manager/README.md), for all the
  reasons given in its README: merging with the public trust store, JKS and PKCS#12 output, and a
  restricted source namespace
- **for private keys.** Replicating a TLS Secret multiplies the exposure of one key; cert-manager
  issuing per namespace does not
- **in pull mode, without thinking about it.** Pull looks convenient and moves the decision to the
  consumer. The source still has to set `replication-allowed`, but the habit of setting it broadly
  and letting namespaces help themselves erodes exactly the isolation namespaces provide
- alongside [Reflector](../reflector/README.md). Pick one

## Notes

The only recorded reference is the repository:
<https://github.com/mittwald/kubernetes-replicator>.

**Deployed here**, via a Flux `HelmRelease` against the mittwald Helm repository, with a worked
example under `example/`:

| File | What it shows |
|---|---|
| `namespaces/foo.yaml`, `namespaces/bar.yaml` | the two target namespaces |
| `secrets/example.yaml` | push mode — `replicate-to: "foo,bar"` on a generic `Opaque` Secret |
| `secrets/acr-secret.yaml` | an `imagePullSecret` for a container registry |
| `secrets/tls-secret.yaml` | a TLS Secret |

Those three Secrets are, deliberately or not, a ranking of how defensible each use is:

- The **registry credential** is the strong case. It is needed everywhere images are pulled, and
  it is already effectively cluster-wide
- The **generic Secret** is fine as a demonstration and a question mark in production — the answer
  depends entirely on what is in it
- The **TLS Secret** is the one to be careful about, because it contains a **private key**. It is a
  legitimate pattern for a wildcard certificate serving several Ingresses, and it is also how one
  private key ends up readable by anyone with `get secrets` in any of those namespaces. The
  alternative worth weighing every time is cert-manager issuing a separate certificate per
  namespace, so the key never travels

The wider argument about when replication is the right shape of answer at all — and when it is
namespace isolation being quietly dismantled — is in [`../README.md`](../README.md).

---

[← Replication](../README.md)
