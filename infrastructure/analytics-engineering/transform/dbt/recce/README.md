[← Transform](../README.md)

# Recce

<https://github.com/DataRecce/recce>
<https://datarecce.io/>

---

## The problem it solves

**Recce is not an alternative to [dbt](../dbt/README.md) or
[SQLMesh](../sqlmesh/README.md).** It is a review tool for dbt changes and it requires a dbt
project to work on. It sits in this folder because that is where the change it reviews is
authored, not because it is a third option to choose between.

The gap it fills is specific. A pull request that edits a dbt model shows up in GitHub as a **SQL
diff**: twelve lines changed, a `CASE` rewritten, a join condition adjusted. A reviewer reads it,
decides it looks reasonable, and approves. What the diff cannot show is the only thing anyone
actually cares about — **what happened to the data**:

| The reviewer sees | The reviewer cannot see |
|---|---|
| a join condition changed | the join now fans out and the table has 4× the rows |
| a filter added | it silently dropped 40% of a downstream mart |
| a `CASE` branch reordered | one category's values all moved to `other` |
| a cast added | nulls appeared where the cast failed |
| a column renamed | three downstream models still reference the old name |

Recce closes that gap by running **both versions** — the base branch and the change — and
comparing the **output**, not the code. The review comment becomes a statement about the data.

**What it compares:**

| Diff | The question it answers |
|---|---|
| **Row count** | did this change how many rows exist, anywhere downstream? |
| **Schema** | did columns appear, disappear or change type? |
| **Profile** | did a column's distribution, null rate or cardinality shift? |
| **Value** | which specific rows differ between the two versions, and how? |
| **Query** | run arbitrary SQL against both environments and diff the result |
| **Lineage** | which models are affected by this change at all |

It runs two ways, and both matter: an **interactive local server** for the person making the
change, where they explore the impact before opening the pull request, and a **CI run** that
produces a shareable summary to attach to the review. The output is a checklist of validations
someone actually performed, rather than an approval based on the SQL looking sensible.

**This is the missing half of the dbt pull-request workflow.** dbt gives you the model graph,
tests and CI. Tests assert things you already knew to assert; the model graph tells you what is
downstream. Neither tells you *what changed in the numbers* — and that is the question a reviewer
is implicitly answering when they click approve.

**Where it sits relative to data governance:**

| | [`data-governance/quality/`](../../../data-governance/quality/README.md) | **Recce** |
|---|---|---|
| Validates | data, **after** it lands | a **change**, before it merges |
| Compares against | rules and expectations you declared | the current production output |
| Catches | a bad load, a broken source, a drifting upstream | a modelling change that moves the numbers |
| When it fires | in the pipeline, in production | in the pull request |

They are complementary and neither substitutes for the other: a quality check would eventually
catch a fan-out — after it reached a dashboard. Recce catches it while it is still a diff.

The other half of the same question is
[`data-governance/lineage/`](../../../data-governance/lineage/README.md): *what breaks downstream
if I change this?* Lineage answers which models are affected; Recce answers **how** they are
affected. Knowing that fourteen models depend on the one you edited is only useful if you can then
find out that two of them changed their row counts.

## When to use it

- a dbt project where **model changes are reviewed in pull requests** and reviewers are approving
  SQL they cannot fully evaluate
- models that feed dashboards or reporting where a silent number change is expensive
- a team that has been bitten by a change that passed tests, passed review, and moved a metric
- onboarding: it makes "what does this change actually do" answerable without deep project
  knowledge
- alongside dbt tests, not instead of them — tests assert known invariants, Recce surfaces
  unknown deltas

## When not to use it

- **not on dbt** — it is dbt-specific; SQLMesh already does change categorisation and virtual
  environments natively, and a non-dbt stack has nothing for it to read
- you cannot materialise both versions anywhere — see the caveat below, it is the real blocker
- the project is small enough that a person reasonably knows the impact of every change
- you wanted continuous data quality monitoring — that is
  [`data-governance/quality/`](../../../data-governance/quality/README.md); Recce is a
  point-in-time comparison of two versions

## Notes

**The cost is real: you need both versions materialised somewhere.** Comparing outputs means both
outputs must exist, which means the base version and the changed version are both built — a
development warehouse, a per-pull-request schema, or duplicated compute against production data.
On a warehouse billed by scanned bytes, that is a line item, and on large models it is not a small
one. Teams that already run dbt CI into a dev target have most of this; teams that do not are
being asked to build it first.

Mitigations worth knowing: scope the comparison to the models a change actually touches rather
than the whole project, and use row-count and schema diffs as the cheap first pass, reserving
value and profile diffs for models where the numbers matter.

**It is a younger project than the tools around it.** Smaller community, fewer people who have
operated it, and a faster-moving surface. The counterweight is that it is additive — it reads a
dbt project and compares environments, so removing it leaves nothing to unwind. Verify commands
and options against the current documentation rather than assuming stability.

**It works on dbt's own artifacts**, comparing a base environment against the current one. That
means the setup question is really *"where does the base environment come from, and is it fresh?"*
— stale base artifacts produce diffs that describe drift rather than the change under review.

**The honest framing:** Recce is worth adopting once the team has already been surprised by a
merged change. Before that it reads as extra process, and the argument for it is hard to make. It
belongs next to dbt in the review workflow, not in the shortlist beside dbt and SQLMesh.

---

[← Transform](../README.md)
