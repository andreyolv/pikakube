[← Storage](../README.md)

# Azure lifecycle policy

<https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview>

---

## The problem it solves

Object storage grows forever unless something deletes things. A lifecycle policy is that something:
a rule the storage system evaluates on its own schedule, moving data to cheaper tiers and expiring
it, with nobody running anything.

[`../README.md`](../README.md) makes the general case. This folder is the **worked example** —
actual Azure Blob Storage policy JSON, a naming convention for rules, and the part that turned out
to be hard, which was not the JSON.

Two rules are recorded here, and they are the two shapes worth knowing.

**Delete on last access.** Expire anything under a prefix that has not been read for N days:

```json
"actions": { "baseBlob": { "delete": { "daysAfterLastAccessTimeGreaterThan": 2 } } },
"filters": { "blobTypes": ["blockBlob"], "prefixMatch": ["mtolv/teste"] }
```

**Tier down, then delete.** One rule walking data through the tiers on age since modification, and
expiring it at the end:

```json
"actions": { "baseBlob": {
  "tierToCool":    { "daysAfterModificationGreaterThan": 2 },
  "tierToCold":    { "daysAfterModificationGreaterThan": 4 },
  "tierToArchive": { "daysAfterModificationGreaterThan": 6 },
  "delete":        { "daysAfterModificationGreaterThan": 7 }
} },
"filters": { "blobTypes": ["blockBlob"], "prefixMatch": ["mtolv/sandbox"] }
```

The day counts are deliberately tiny — these were written to be observed working, not to be
deployed. The structure is the point: **one rule, scoped to a prefix, carrying the entire lifetime
of the data under it.**

## The naming convention

Recorded alongside the policies, because rules accumulate and unnamed rules become undeletable —
nobody will remove a rule they cannot explain.

```
name: StoragePath-Action-Policy-NumberOfDays
name: (1)-(2)-(3)-(4)
```

| Part | Values recorded |
|---|---|
| **(1) StoragePath** | `mtolv/teste`, `mtolv/sandbox`, … — the prefix the rule applies to |
| **(2) Action** | `Cool` → `tierToCool` · `Cold` → `tierToCold` · `Archive` → `tierToArchive` · `Delete` → `delete` · `Auto` → `enableAutoTierToHotFromCool` |
| **(3) Policy** | `Creation` → `daysAfterCreationGreaterThan` · `Modification` → `daysAfterModificationGreaterThan` · `LastAccess` → `daysAfterLastAccessTimeGreaterThan` |
| **(4) NumberOfDays** | `30`, `60`, … |

So `mtolv/sandbox-Cool/Cold/Archive/Delete-Modification-2/4/6/7` reads as: the sandbox prefix,
tiered down and then deleted, on time since modification, at 2, 4, 6 and 7 days.

**Encoding the whole intent in the name is the right call.** A lifecycle rule is invisible
infrastructure that silently deletes data, and the audit question — *why did this disappear* — has
to be answerable from the rule list alone, without reading JSON.

## The trigger conditions are the actual decision

The three `Policy` values are not interchangeable, and picking the wrong one is the mistake that
produces either surprise deletions or a policy that never fires:

| Trigger | Fires on | Right for | Wrong for |
|---|---|---|---|
| **Creation** | age since written | immutable batch drops, landing zones | anything updated in place |
| **Modification** | age since last change | working areas, sandboxes | data written once and read for years |
| **Last access** | age since last **read** | **archival decisions** | anything where read tracking is off or unsupported |

Last access is the one that answers the question people actually have — *is anyone still using
this?* — and it is why the delete example above uses it. It is also the one with caveats: access
tracking must be enabled, it costs something to track, and the equivalent support varies across
providers. Verify it before designing around it.

## The hard part: path or tag

The recorded reasoning, which is the most valuable thing in this folder, because it is the decision
that has to be made before any JSON is written.

**Option A — users tag their own data, policies filter on tags.**

Attractive: each team declares the lifecycle it wants, on its own data, without a platform request.
The rules stop being a central bottleneck.

Recorded objection: *service principals would need RBAC permissions to change tags, which requires
large structural changes.* Blob index tags are governed by their own role assignments —
see [Microsoft's RBAC notes on finding blobs by tag](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-manage-find-blobs?tabs=azure-portal#role-based-access-control) —
so every writing identity needs a new permission, granted deliberately, across the estate.

There is a governance objection underneath the operational one: **if the writer sets the tag, the
writer sets the retention policy.** Data lifetime stops being a governed decision and becomes
whatever each pipeline author happened to write, which is the opposite of the point.

**Option B — manage it by path in the lake, automating at access-request time.**

The alternative recorded here: keep the rules keyed on prefixes, and automate their creation via
Python or the management API **as part of the access request** — when someone asks for a directory,
they get a directory with an owner, permissions and a lifecycle rule, together.

Reference code recorded for this:

- [Azure management SDK sample — `manage_management_policy.py`](https://github.com/Azure-Samples/azure-samples-python-management/blob/main/samples/storage/manage_management_policy.py)
- [Python for Azure — automated access tiering and purge](https://medium.com/python-for-azure/python-for-azure-blob-data-lifecycle-management-automated-access-tiering-purge-c8d4003cfc3d)

**Option B is the better answer**, and not only because tags need RBAC changes. The per-directory
model in [`../README.md`](../README.md#6-notes) already keys owners, permissions, size and
transaction counts on the path. Keying lifecycle on the same thing means one identifier governs
everything about a directory — and the lifecycle rule gets created at the one moment when someone
is actually thinking about the data, which is when they ask for the space.

Tag-based policy is the more elegant design and the wrong one here. It distributes a decision that
should be governed, and it requires the permission model to be loosened to do it.

## When to use it

- any object storage prefix that grows — which is all of them
- landing zones, sandboxes and scratch space, where nobody will ever volunteer to clean up
- old table snapshots and non-current object versions, whose cost is invisible until it is not
- wherever cost has to be attributable to a directory owner

## When not to use it

- **table metadata prefixes** — manifests, transaction logs and snapshot pointers are small,
  constantly read, and archiving them makes the table unreadable while saving nothing
- anything a query engine reads, if the action is `tierToArchive` — archived blobs must be
  rehydrated over hours, so queries fail rather than slow down
- data with a shorter life than the tier's minimum retention period, where tiering costs more than
  staying hot
- as a substitute for snapshot expiry and orphan cleanup in the table format itself — those are
  [maintenance jobs](../../table-formats/README.md#5-the-part-everyone-forgets-maintenance), and a
  storage rule cannot tell a live file from an orphan

That last exclusion is the one to be careful about. A lifecycle rule deletes objects by age; a
table's manifest may still reference an object that is old. **Deleting a referenced data file
corrupts the table**, and the storage system has no way to know. Expiry inside a lakehouse bucket
belongs to `expire_snapshots` and `remove_orphan_files`, not to a blob rule.

## Notes

Everything above is recorded work rather than description: the two policy JSON documents, the
naming pattern, and the path-versus-tag reasoning are all in this folder.

Three things transfer beyond Azure:

**The mechanism is provider-independent.** S3 lifecycle configuration has the same shape — a
filter, a set of transition and expiration actions, and a day count — and the equivalent is
configured against MinIO in the
[`06-lifecycle`](../minio/boto3/boto3-client/README.md) notebooks. Anything decided here applies
there with different field names.

**The naming convention transfers unchanged.** It solves a human problem, not an Azure one.

**The path-versus-tag decision transfers unchanged**, and it is the one worth carrying over. It is
a governance question — who is allowed to decide how long data lives — wearing a configuration
question's clothes.

The reason the Azure work is worth keeping in a self-hosted repository: **this is the part of
storage governance that is usually skipped**, and it was actually thought through here. The
per-directory model in [`../README.md`](../README.md#6-notes) is the same reasoning generalised,
and this folder is where it came from.

Provider context for Azure itself is under
[`site-reliability-engineering/storage/cloud/azure/`](../../../../site-reliability-engineering/storage/cloud/azure/README.md).

---

[← Storage](../README.md)
