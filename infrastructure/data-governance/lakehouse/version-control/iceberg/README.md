[← Version control](../README.md)

# Iceberg branching and tagging

<https://github.com/apache/iceberg>

---

## The problem it solves

Branching a table with **nothing to deploy**. No extra service, no component in the data path, no
new dependency — it is a property of the table format itself, and it is already there if the tables
are [Iceberg](../../table-formats/iceberg/README.md).

The mechanism falls out of how Iceberg already works. Every commit produces a **snapshot**, and the
table's current state is a pointer to one of them. A branch is just **another named pointer** into
that same snapshot history, and a tag is a named pointer that does not move.

| Concept | What it is |
|---|---|
| **Snapshot** | the table's complete state after one commit — already created on every write |
| **Branch** | a named, movable pointer to a snapshot; writes advance it |
| **Tag** | a named, fixed pointer to a snapshot; it does not move |
| `main` | the default branch — nothing special about it beyond the name |

Because the snapshots already exist, creating a branch **copies no data**. It writes a name into
the table's metadata. That is why this costs nothing and why there is no service: the whole feature
is a few extra entries in a file Iceberg was writing anyway.

## Write-audit-publish, concretely

The pattern [`../README.md`](../README.md) describes, in the form Iceberg gives it:

```sql
-- 1. WRITE: branch off, and write there. Nobody reading main sees it.
ALTER TABLE db.events CREATE BRANCH audit_2026_08_09;
-- the pipeline writes to the branch, e.g. via spark.wap.branch

-- 2. AUDIT: query the branch directly and run the checks
SELECT count(*) FROM db.events.branch_audit_2026_08_09 WHERE user_id IS NULL;

-- 3a. PUBLISH: checks pass — move main to the branch's snapshot
CALL catalog.system.fast_forward('db.events', 'main', 'audit_2026_08_09');

-- 3b. DISCARD: checks fail — drop the branch, and nothing was ever visible
ALTER TABLE db.events DROP BRANCH audit_2026_08_09;
```

Three properties of this are worth stating separately:

**The branch is readable as a table.** `db.events.branch_<name>` is queryable by any engine that
supports Iceberg branching, so the quality checks are ordinary SQL against an ordinary table — no
special integration between the checker and the branching mechanism. That is what makes
[Soda](../../../quality/soda/README.md) or an equivalent work here without knowing branches exist.

**Publishing is a metadata operation.** `fast_forward` moves a pointer. It does not rewrite or copy
data, it is atomic, and it is as fast for a terabyte as for a row.

**Discarding is free.** A failed run drops a name. The data files it wrote become orphans, cleaned
up by `remove_orphan_files` on its normal schedule — which is one more reason maintenance has to be
scheduled.

## Tags are the other half, and are usually forgotten

A tag pins a snapshot by name, permanently:

```sql
ALTER TABLE db.events CREATE TAG month_end_2026_07 RETAIN 365 DAYS;
SELECT * FROM db.events.tag_month_end_2026_07;
```

This is the answer to *"reproduce the report exactly as it was published"*. A timestamp is not the
same answer: timestamps rely on snapshots still existing, and snapshot expiry will eventually
remove them. **A tag is a commitment that a specific state survives**, and expiry respects it.

| Question | Mechanism |
|---|---|
| What did this look like last Tuesday? | time travel by timestamp — until snapshots expire |
| Reproduce the figure we published in July | **a tag** — it survives expiry |
| Test a change before anyone sees it | **a branch** |
| Roll back a bad publish | move `main` back to a known snapshot |

## The interaction with `expire_snapshots`

This is the part that catches people, and it cuts both ways.

`expire_snapshots` is the maintenance job that keeps history — and storage cost — from growing
forever. It deletes snapshots older than a retention threshold, and the data files only they
referenced.

**Branches and tags are references, and expiry will not delete a snapshot a branch or tag points
at.** That is correct behaviour and it has a consequence:

| Situation | Result |
|---|---|
| Branches deleted after each run | expiry works normally; cost is bounded |
| **A branch left behind by a failed run** | its snapshot is retained forever, and so is every data file under it |
| A branch per developer, kept indefinitely | storage grows and expiry cannot reclaim it |
| A tag with no retention | intentional, and it should be a deliberate decision |
| Expiry never scheduled at all | none of this matters, because nothing is ever reclaimed |

Both the [table formats](../../table-formats/README.md#5-the-part-everyone-forgets-maintenance) and
[version control](../README.md#5-anti-patterns) pages list this as an anti-pattern, and it is worth
seeing why they are the same failure: **an abandoned branch is a snapshot that cannot expire.** The
pipeline that drops its branch on failure is not being tidy, it is the thing that keeps storage
bounded.

Branches accept a retention clause — `RETAIN` on creation — which is the belt-and-braces version
for pipelines that will eventually crash before their cleanup step.

## When to use it

- **the default starting point** when the tables are already Iceberg — it costs nothing
- one pipeline run writes **one table**, and needs validating before publication
- reproducible reporting, via tags
- an audit gate is wanted without introducing a component every read passes through

## When not to use it

- a run must update **several tables atomically** — branching is per table, and there is no
  cross-table merge; that is [Nessie](../nessie/README.md)
- non-table files are also in scope — raw landing data, models, images — that is
  [lakeFS](../lakefs/README.md)
- the tables are not Iceberg; [Delta](../../table-formats/delta/README.md) and the others do not
  have an equivalent in this form
- as a **backup**; snapshots expire and none of this survives a deleted bucket

The first exclusion is the real boundary. Per-table branching means five tables branched in one run
are five independent merges, and a failure between the second and the third leaves a state no query
expects. If that matters, the scope is wrong and the answer is a versioned catalog.

## Notes

Reference recorded in [`table-formats/iceberg/`](../../table-formats/iceberg/README.md):

- [Iceberg branching documentation](https://iceberg.apache.org/docs/latest/branching/#overview)

Nothing is deployed here, which is the point — **there is nothing to deploy.** The tables exist,
the catalog exists, and branching is available on them.

**This is the right first step for pikakube.** The recorded substrate is
[Iceberg](../../table-formats/iceberg/README.md) on [MinIO](../../storage/minio/README.md) with a
REST catalog from [`metadata-catalog/`](../../../metadata-catalog/README.md), which means the free
option is already in place and covers the single-table case completely.

One dependency worth naming: **branch operations are catalog operations.** Creating, advancing and
dropping a branch mutates table metadata through the catalog, so branching inherits whatever
availability and concurrency properties the catalog has. It is free in the sense of requiring no new
component — not in the sense of having no dependencies.

The sequence that makes it worth anything, from [`../README.md`](../README.md):

1. branch per pipeline run
2. quality checks against the branch — [Soda](../../../quality/soda/README.md) as an
   [Airflow](../../../../data-engineering/orchestration/airflow/README.md) task
3. `fast_forward` on pass, `DROP BRANCH` on fail
4. `expire_snapshots` on a schedule, which only works because step 3 drops the branch

Step 2 is what turns [`quality/`](../../../quality/README.md) from a report into a control.
Branching without a gate is ceremony.

---

[← Version control](../README.md)
