[← Interoperability](../README.md)

# Apache XTable (incubating)

<https://github.com/apache/incubator-xtable>

---

## The problem it solves

Omnidirectional translation between [Iceberg](../../table-formats/iceberg/README.md),
[Delta](../../table-formats/delta/README.md) and [Hudi](../../table-formats/hudi/README.md), over
the same data files.

The premise is the same one [UniForm](../uniform/README.md) uses: all three formats store Parquet,
and what differs is the metadata describing which files are in the table. XTable reads the source
format's metadata and **writes the target format's metadata** over the same files. No data is
copied.

The difference from UniForm is where it runs. UniForm writes the second metadata layer *inside the
commit*; XTable is a **separate job** that runs after the fact, against a table it did not write.

| | XTable | [UniForm](../uniform/README.md) |
|---|---|---|
| Runs | as a job, after the write | inside the commit |
| Directions | **Iceberg ↔ Delta ↔ Hudi** | Delta → Iceberg |
| Needs the writer's cooperation | **no** | yes |
| Freshness | as stale as the last run | current by construction |
| Failure mode | the translated view lags, silently | the commit fails, loudly |

**The independence is the real advantage.** XTable translates a table whose writer you do not
control — another team's pipeline, a vendor's output, an estate inherited in a migration. UniForm
requires the writer to be configured; XTable does not.

**The lag is the real cost.** A translated view that has not been refreshed since yesterday looks
exactly like a correct view. Nothing about querying it indicates that it is behind, so freshness
has to be monitored explicitly and it usually is not.

## When to use it

- more than one format exists, **the writers cannot be changed**, and both views are needed
- a migration between formats, where consumers move over gradually
- the direction needed is one UniForm does not cover — Iceberg to Delta, or anything involving Hudi
- with an end date attached, as a bridge — see [`../README.md`](../README.md)

## When not to use it

- the format decision is still open; **decide it** rather than translating around it
- the writer can be configured — [UniForm](../uniform/README.md) has no staleness window
- the consumer could simply read the primary format, which is the case more often than it is checked
- production dependence on a translated view, with no freshness alerting
- **the packaging cost is unacceptable**, which is the recorded finding here

## Notes

Recorded from evaluating it:

> Early stage. You have to build the Java package yourself. Rubbish.

Stated less bluntly and without softening the verdict: **it was tried and rejected on packaging.**
At the time it was evaluated there was no ready artefact to consume — using XTable meant building
the Java package from source first, which is a real cost for a tool whose entire job is to be a
supporting utility in a pipeline.

Why that is disqualifying rather than merely annoying:

| | The consequence |
|---|---|
| Build from source | the platform now owns a Java build for a component it did not write |
| Incubating status | APIs, packaging and behaviour can all change under it |
| It sits in a pipeline | a supporting utility with a bespoke build is a supporting utility that breaks on upgrade |
| It is a bridge | the effort has to be justified against a component intended to be removed later |

The last row is the argument. Interoperability tooling is meant to be temporary. Investing in a
custom build pipeline for something you intend to switch off is the wrong shape of effort — and if
the bridge is permanent, the format decision is the thing that should be revisited instead.

**This may well change.** The project is an Apache incubating project, the mechanism is sound, and
packaging is exactly the kind of thing that improves as a project matures. The note records a state
at a point in time, not a permanent judgement on the idea — the idea is fine, the distribution was
not. Re-check the release artefacts before dismissing it a second time.

For pikakube nothing here is needed: the recorded position across
[`lakehouse/`](../../README.md) is a single primary format, which is the condition under which this
folder should stay unused.

---

[← Interoperability](../README.md)
