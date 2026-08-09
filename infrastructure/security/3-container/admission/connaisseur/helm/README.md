[← Connaisseur](../README.md)

# Connaisseur — Helm deployment

The Flux resources that install Connaisseur.

---

## What is here

| File | Resource | What it does |
|---|---|---|
| `helmrepository.yaml` | `HelmRepository` (`flux-system`) | registers `https://sse-secure-systems.github.io/connaisseur/charts` as a chart source |
| `helmrelease.yaml` | `HelmRelease` (`connaisseur`) | installs chart `connaisseur` version `2.3.2`, reconciled every 5 minutes |
| `../namespace.yaml` | `Namespace` | creates the `connaisseur` namespace |

## The one value that is set

```yaml
kubernetes:
  deployment:
    replicasCount: 1
```

A single replica of an admission webhook sitting in the path of every pod creation. For a
development cluster that is a reasonable saving. For anything with real workloads it is the
first thing to change, because it interacts badly with either choice of `failurePolicy`:

| `failurePolicy` | With one replica |
|---|---|
| `Fail` | the pod is rescheduled or the node drains → no webhook → **no pod in the cluster can be created**, including Connaisseur's own |
| `Ignore` | the same event silently disables signature verification, and nothing tells you |

The standard mitigation is at least two replicas, a `PodDisruptionBudget`, and the webhook's own
namespace excluded from its `namespaceSelector`. See [`../../README.md`](../../README.md)
section 6.

## What this does not do

**No validators and no image policy are configured.** Connaisseur's behaviour comes entirely
from its `validators` and `policy` values — which signature format to check, for which image
globs, and what the default rule is. With chart defaults and none of that supplied, this
installs the controller without giving it anything to enforce.

The rollout order that works — detection mode first, then scoped enforcement — is in
[`../../README.md`](../../README.md) section 5.

## Notes

- The chart values references kept in the file:
  <https://artifacthub.io/packages/helm/connaisseur/connaisseur> and
  <https://github.com/sse-secure-systems/connaisseur/blob/master/helm/values.yaml> — the second
  is where the `validators` and `policy` structure is documented.

- Three verifiers are staged in this tree — this one,
  [sigstore policy-controller](../../sigstore-policy-controller/README.md) and
  [Ratify](../../ratify/README.md). Only one should ever be enforcing.

---

[← Connaisseur](../README.md)
