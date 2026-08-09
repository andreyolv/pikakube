[← MongoDB](../README.md)

# MongoDB Kubernetes Operator

<https://github.com/mongodb/mongodb-kubernetes>
<https://github.com/mongodb/helm-charts>

Samples: <https://github.com/mongodb/mongodb-kubernetes/tree/master/config/samples>

---

## What it is

MongoDB's **current** official operator, unifying what were previously separate community and
enterprise lines into one controller.

That consolidation is the reason it exists, and it is also why the folder next door still has a
page: [`mongodb-operator/`](../mongodb-operator/README.md) is the older
`mongodb-kubernetes-operator`, and a great deal of documentation still refers to it.

| Capability | Detail |
|---|---|
| **Replica sets and sharded clusters** | both topologies, from one operator |
| Ops Manager / Cloud Manager integration | for the enterprise line |
| Users, roles and TLS | as Kubernetes resources |
| Rolling upgrades | ordered, with step-downs |
| **One operator for both editions** | which is the point of the consolidation |

## When to use it

- MongoDB's own tooling is the intended path, and the current one rather than the legacy one
- **enterprise features or a support relationship** matter
- the deployment may move to Atlas or Ops Manager, and consistency with that is worth something
- sharding is required and staying within MongoDB's tooling is preferred

## When not to use it

- **Apache licensing is a requirement** — [Percona's operator](../percona-mongodb-operator/README.md)
  is Apache-2.0 with a complete free feature set
- the useful capabilities turn out to sit behind the enterprise tier
- a single replica set for development, where the plain manifests are enough

## The tiering question

This is what to check before adopting it, and it is not always obvious from the documentation.

The operator is one artefact; the **features it unlocks are tiered**. Backups through Ops Manager,
certain security features and some monitoring integrations belong to the enterprise line.

The practical consequence: it is possible to deploy this operator, have it work, and discover
later that the specific capability it was chosen for requires a commercial agreement. Percona's
alternative avoids the question entirely by having no tiers.

## Choosing between the three

| | Community Operator | **This** | Percona |
|---|---|---|---|
| Status | legacy | **current official** | actively maintained |
| Licence | free, limited scope | tiered | **Apache 2.0** |
| Backups / PITR | no | via Ops Manager | **included** |
| Sharding | no | yes | **yes** |
| Path to Atlas | — | **consistent** | no |

[`../README.md`](../README.md) gives the summary: **Percona for self-hosting, MongoDB's own when
the enterprise relationship or the Atlas path matters.**

## Notes

Mapped as the current official option. The
[samples](https://github.com/mongodb/mongodb-kubernetes/tree/master/config/samples) are the
starting point, as with the previous generation.

For this platform, MongoDB is a **source system** rather than something the platform serves — see
[`../README.md`](../README.md#how-this-applies-to-pikakube). In that position the deciding
questions are narrow: does the deployment produce a replica set, so change streams work, and is
it stable enough to extract from continuously.

Both this and Percona's answer yes. The licence is what separates them, and for a repository that
catalogues open-source tooling, that is not a small distinction.

---

[← MongoDB](../README.md)
