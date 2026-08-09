[← Feature store](../README.md)

# Feast

<https://github.com/feast-dev/feast>
<https://docs.feast.dev/>

---

## The problem it solves

Feast is the open-source answer to the problem in [`../README.md`](../README.md): one feature
definition, used to build training sets with a point-in-time join and to serve values at
inference latency.

**The thing to understand first: Feast is a framework over infrastructure you already have, not a
database.** It stores almost nothing itself. You point it at the systems you already run and it
supplies the layer that was missing:

| Layer | Who provides it |
|---|---|
| Offline store — feature history | your warehouse, or Parquet on object storage |
| Online store — current values | a key-value store, typically [Redis](../../../databases/nosql/key-value/redis/README.md) |
| Feature definitions | Feast, as Python objects in your repo |
| Registry | Feast, as a file in object storage or a database |
| Retrieval | Feast, as an SDK and an optional HTTP/gRPC feature server |

That composability is its main argument. It is also why **"deploy Feast" is not one decision** —
it is a decision about an offline store, a decision about an online store, a decision about where
the registry lives, and a decision about whether anything serves features over the network. The
Feast component itself is the smallest of the four.

**The pieces:**

| Concept | What it is |
|---|---|
| **Entity** | the thing features are keyed by — a customer, a driver, an order |
| **Data source** | where values already live: a warehouse table, a Parquet path, a stream |
| **Feature view** | a named group of features on an entity, bound to a source and a timestamp column |
| **Feature service** | the set of features one model consumes — the unit a model depends on |
| **Registry** | the serialised catalogue of all of the above, shared by every client |

**The registry** is the part that makes it a shared system rather than a library. It is a single
artefact — historically a file on object storage, and a SQL-backed registry for concurrent
writers — produced by `feast apply` from the Python definitions and read by everything else. Every
training job and every serving process resolves features through the same registry, which is
mechanically how "one definition" is enforced rather than merely intended.

**The two retrieval calls** are the whole API surface that matters:

- `get_historical_features` — builds a training set from an entity dataframe of keys and event
  timestamps, performing the **point-in-time join** described in the parent README. This is the
  correctness feature, and the main reason to use Feast over hand-written SQL.
- `get_online_features` — reads current values for a set of entity keys from the online store, for
  the inference path. Available in-process through the Python SDK or over the network from a
  feature server.

**`feast materialize`** is the seam between the two: it copies values from the offline store into
the online store for a time range, with an incremental variant for scheduled runs. It is an
ordinary job that wants an [orchestrator](../../../data-engineering/orchestration/README.md) and
freshness monitoring — a failed materialisation leaves serving working, on stale values.

**Feast is not a transformation engine.** It reads features from wherever they were already
computed; building them is [`transform/`](../../../analytics-engineering/transform/README.md)'s
job. On-demand feature views added row-level transformations at request time, for values that
depend on the request itself, but the bulk of feature computation stays outside Feast by design.

## When to use it

- **several models or teams share features**, and the definitions have started to diverge
- online inference needs feature values a warehouse cannot serve fast enough
- training sets need point-in-time joins often enough that writing them by hand has become a
  source of bugs
- the storage you would use is already in place — Feast is much cheaper to adopt when the
  warehouse and the key-value store already exist and are operated
- you want the definition layer without buying a hosted platform

## When not to use it

- **one team, a handful of models** — a shared Python library imported by both paths meets the
  actual requirement, as [`../README.md`](../README.md) argues, without two stores and a pipeline
- batch scoring only, with no online path — a warehouse and a reviewed as-of join is the whole
  solution
- you expected it to compute features — that is a transformation framework's job, not this one's
- you have no offline store or no key-value store to point it at; then Feast is not one adoption,
  it is three
- the underlying skew is organisational — two teams that will not agree on a definition are not
  fixed by a registry

## Notes

**Check current maintenance before committing.** Feast started at Gojek, was donated to LF AI &
Data, and has been through more than one change of direction and of commercial stewardship; the
company most associated with it has not stayed in the same relationship to the project. That is
not a reason to avoid it — it is Apache-licensed, self-hosted and the data lives in stores you
own, so the exit cost is low. It *is* a reason to look at recent commit activity and release
cadence yourself rather than at the project's age.

**Check the supported store list for your specific stores.** Offline and online store support is
plugin-shaped and uneven: some backends are first-class, some are contributed and lightly
exercised, and the set changes between releases. The default online store is a local SQLite file,
which is a development convenience and not a deployment. Verify your intended pair against the
current documentation before designing around it.

**The exit is genuinely cheap, and that is the strongest practical argument.** The feature values
are in your warehouse and your key-value store either way. The registry and the definitions are
the only Feast-specific artefacts, and they are Python and a serialised catalogue. Adopting Feast
does not put the data anywhere you could not read without it.

**Operational notes worth having before the first deploy:**

| Decision | Why it bites later |
|---|---|
| Where the registry lives | a file registry is simple and does not handle concurrent writers well; a SQL registry is another component |
| Materialisation schedule, per feature | the lag is the feature's staleness, and it is a correctness property |
| Feature-freshness monitoring | a failed materialisation is silent — serving succeeds on old values |
| SDK-in-process or a feature server | in-process avoids a hop and pins your serving stack to Python; a server is another thing to run and scale |
| Online store capacity | it is on the request path; its degradation is inference degradation |

Placement note: this is the deploy-adjacent side of MLOps, and it depends on there being an
inference path to serve. See [`../../lifecycle/`](../../lifecycle/README.md) for what is actually
deployed in this repository today.

---

[← Feature store](../README.md)
