[← Backup](../README.md)

# Stash

<https://github.com/stashed/stash>
<https://stash.run/>

---

## What it is

Volume and database backup for Kubernetes from AppsCode, built on Restic, with CRDs for
scheduling, retention and application-specific backup logic.

Feature-wise it sits between [K8up](../k8up/README.md) and [Kanister](../kanister/README.md): Restic-based volume
backup, plus per-database add-ons that handle application-consistent dumps.

## When to use it

- you are already in the AppsCode ecosystem — KubeDB and related tooling
- database-aware backup with less modelling than Kanister blueprints require

## When not to use it

- **check the licensing first.** AppsCode has moved parts of its portfolio to commercial
  licensing, and "open source" here needs verifying for the version you would deploy. This is
  the first thing to establish, not a footnote
- open source with an unambiguous licence is a requirement — [Velero](../velero/README.md) or [K8up](../k8up/README.md)
- you want the broadest community and the most written material

## The honest positioning

Mapped for comparison. It is capable, and it is the option in this folder where the licence
question is most likely to change the answer — worth resolving before investing time, because
a backup tool is a poor place to discover a licensing surprise later.

---

[← Backup](../README.md)
