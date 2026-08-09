[← Aggregation](../README.md)

# GUAC

<https://github.com/guacsec/guac>
<https://github.com/guacsec/helm-charts>

---

## The problem it solves

Supply-chain evidence arrives as a pile of unrelated documents: SBOMs in two formats, in-toto
attestations, SLSA provenance, VEX statements, OSV advisories, Scorecard results. Each answers
one question about one artefact. None of them can be traversed.

GUAC — Graph for Understanding Artifact Composition — ingests all of them into a single graph
where artefacts, packages, source repositories, builders and attestations are nodes and the
relationships between them are edges. The queries it makes possible are the ones that cross
document boundaries:

- this CVE affects this package — which of our images contain it, and which deployments run
  those images?
- this build was compromised — what else did that builder produce, and where did it go?
- this dependency's repository was taken over — what is downstream of it, transitively?
- do we have provenance for every artefact in production, and which builder signed it?

Dependency-Track answers the first of those. GUAC is built for all four, because the answer
lives in the connections rather than in any single document.

## When to use it

- several **kinds** of evidence already exist — SBOMs *and* attestations *and* VEX — and the
  work has moved from collecting them to correlating them
- the questions being asked are about **blast radius and ancestry**, not component inventory
- you want one place that ingests from OSV, deps.dev, Scorecard and your own documents, and
  keeps the relationships between them
- an incident response process needs to traverse from a disclosure to deployments in one
  system rather than by joining spreadsheets
- there is appetite to operate a graph store and a set of collectors, and to learn its model

## When not to use it

- the question is "which projects contain component X?" —
  [Dependency-Track](../dependency-track/README.md) answers it with far less to run
- nothing produces attestations or provenance yet. GUAC's value is proportional to the number
  of evidence types you feed it; with only SBOMs it is an expensive Dependency-Track
- a small estate. The graph pays off when the relationships are too many to hold in your head,
  and a handful of images does not qualify
- operational budget is tight — it is a younger project with more moving parts, and the
  learning curve is the model, not the deployment
- as a first step into supply-chain security. It is the second or third step

## Notes

Original references recorded for this tool:

> <https://github.com/guacsec/guac>
> <https://github.com/guacsec/helm-charts>

Worth recording a discrepancy: the chart staged in this repository comes from
`https://kusaridev.github.io/helm-charts` (chart `guac`, version `0.6.2`), not from the
`guacsec` repository listed in the note. Kusari are the main contributors behind GUAC, so this
is expected rather than wrong — but it is the kind of thing that makes a chart hard to find
later, and it is why the source is written down here.

The project is an OpenSSF effort and is younger than most things in this folder. That shows up
as a moving data model and API rather than as instability at runtime, which is the right way
round, but it does mean queries and integrations written against it are more likely to need
revisiting than those against Dependency-Track.

The staged `HelmRelease` has an empty `values:` block and its own `guac` namespace, so nothing
has been exercised. Before it would do anything useful here, something has to be producing the
evidence it exists to correlate — and at present this platform produces one signature and no
attestations, which is not enough graph to be worth traversing.

---

[← Aggregation](../README.md)
