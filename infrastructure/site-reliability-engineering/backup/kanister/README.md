[← Backup](../README.md)

# Kanister

<https://github.com/kanisterio/kanister>

---

## The problem it solves

A volume snapshot of a database is bytes on a disk at a moment — possibly a half-written page
and an in-flight transaction. It restores, and it does not work.

Kanister builds its whole model around fixing that. A **Blueprint** describes the actual steps
to back up and restore a specific application: run `pg_dump`, flush and lock, snapshot, unlock,
verify. The logic lives in a CRD instead of in someone's runbook.

| Concept | What it is |
|---|---|
| `Blueprint` | the backup and restore procedure for an application type |
| `ActionSet` | an execution of that procedure against a specific instance |
| `Profile` | where the artefacts go — object storage credentials |

## When to use it

- **databases**, where a correct backup requires application-level coordination
- the same application is backed up repeatedly and the procedure should be codified rather than remembered
- you need restore steps that are more than "put the volume back"

## When not to use it

- ordinary stateless workloads with volumes — [Velero](../velero/README.md) with hooks is simpler
- cluster **objects** also need backing up; this is application-centric by design
- nobody will maintain the Blueprints. They are code, and code rots

## Kanister or Velero hooks

Velero supports pre- and post-backup hooks, which covers freeze-and-flush for many cases.
Kanister goes further: the entire procedure, including restore, is modelled and reusable.

The line is roughly whether the procedure has **steps** or just a **pause**. `fsfreeze` before
a snapshot is a hook. Dump, upload, verify, and a restore path that recreates users and roles
is a Blueprint.

## Related

[K10](../k10/README.md) is the commercial product from the same origin, and uses Kanister underneath.

---

[← Backup](../README.md)
