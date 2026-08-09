[← Analytics Engineering](../README.md)

# Semantic layer

Where metric definitions live, so everyone counts the same way.

Tools covered: [`cube`](cube/README.md)

---

## The problem it solves

Two dashboards disagree about revenue. Both queries look reasonable. One excludes refunds, the
other excludes them and cancellations. Nobody knows which is correct, and the meeting stops
being about the business.

That happens because the definition was written **twice**, in two places, by two people — and
nothing made them the same.

A semantic layer moves the definition into one versioned place, and every consumer derives from
it: BI tools, notebooks, APIs, and anything else that asks a question.

| Without | With |
|---|---|
| Metric logic duplicated per dashboard | defined once |
| "Which number is right?" | one answer, by construction |
| Joins re-implemented per query | modelled once |
| Changing a definition means finding every copy | change it in one place |

## What it actually provides

| Capability | Detail |
|---|---|
| **Metric definitions** | revenue, active users, churn — as code, with the filters and exclusions explicit |
| **Dimensions and joins** | the relationships modelled once, so consumers do not re-derive them |
| **Access control** | row and column level, applied consistently regardless of the tool asking |
| **Caching and pre-aggregation** | the same question answered repeatedly does not recompute |
| **An API** | SQL, REST and GraphQL, so it serves applications as well as dashboards |

The last row is the one that separates a semantic layer from a modelling convention: an
application can consume the same definitions as a dashboard, and get the same number.

## The tools

| Tool | Notes | Detail |
|---|---|---|
| **Cube** | the established open-source semantic layer — definitions, caching, pre-aggregation, and SQL/REST/GraphQL APIs | [→](cube/README.md) |

## The alternatives that are not in this folder

Worth naming, because "install a semantic layer" is not always the right answer:

| Approach | Where the definition lives | Trade |
|---|---|---|
| **dbt metrics** | in the [transform layer](../transform/README.md), next to the models | no new component; consumption depends on tool support |
| **Lightdash** | reads dbt metrics directly | ties the layer to one BI tool — see [`viz/`](../viz/README.md) |
| **Modelled marts only** | definitions become tables | simple and durable, but a metric per aggregation |
| **Cube** | a dedicated service | most capable, and one more thing to operate |

For many platforms the third row is enough. A well-modelled mart with the metric already
computed removes most of the ambiguity, and costs nothing to run.

The dedicated layer earns its place when **several different consumers** need the same
definitions — a BI tool, an application, and a notebook — which is exactly when the "define it
in the mart" approach starts being copied again.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Metrics defined in each BI tool | the original problem, with extra steps | one definition, upstream |
| A semantic layer over unmodelled raw tables | it becomes a second transformation layer, undoing the point of ELT | model first, then define metrics |
| Adopting it before the disagreement exists | a service to operate for a problem nobody has | modelled marts until several consumers appear |
| Definitions without owners | they drift, and nobody is accountable for the number | ownership per metric domain |

## How this applies to pikakube

Not deployed. **Cube** is mapped, and the honest note is that this is a capability worth
adopting **after** the transform layer is solid rather than alongside it — a semantic layer over
poorly modelled data moves the problem rather than solving it.

The realistic path here: metrics defined in [dbt](../transform/dbt/README.md) models, and this folder
revisited when more than one kind of consumer needs the same numbers.

---

[← Analytics Engineering](../README.md)
