[← Data catalogs](../README.md)

# Magda

<https://github.com/magda-io/magda>

---

## The problem it solves

Magda is a **data portal for open data** — software for publishing datasets to an external
audience. It was built by Australia's CSIRO Data61 and it powers government open-data portals.

That is a different problem from the rest of this folder, and getting the distinction right is the
entire value of this page:

| | **Magda** | [`platform/`](../../platform/README.md) — OpenMetadata, DataHub |
|---|---|---|
| Audience | **the public**, or another organisation | **internal analysts and engineers** |
| Unit of publication | a **dataset** — a file, an API, a download | a **table**, with columns and a schema |
| Metadata model | **DCAT** — the open-data interchange standard | technical and business metadata |
| How it fills up | **harvesting** other portals, plus manual publication | **ingestion connectors** crawling warehouses and pipelines |
| Typical question | "is there open data on air quality?" | "which of our tables should I use, and can I trust it?" |
| Lineage | not the point | central |

Its real capabilities follow from that audience: federated **harvesting** from other portals
(CKAN, DCAT endpoints), a public search experience with faceting, dataset request and approval
workflows, and a preview layer for tabular and geospatial files.

## When to use it

- there is a requirement to **publish datasets externally** — an open-data portal, a transparency
  obligation, a research data portal
- datasets must be **harvested from or exposed to other portals** using DCAT
- the audience is people who do not have access to the platform and will not be given any
- the unit being published is a **file or an API**, not a table in a warehouse

## When not to use it

- **internal data discovery** — this is the wrong tool, and it is the mistake this page exists to
  prevent. Magda has no concept of a table's columns, no ingestion from a warehouse, no lineage,
  and no connection to the systems that actually produce metadata here. Deploying it for internal
  discovery means hand-publishing dataset entries, which is
  [the failure mode described in](../README.md#what-actually-decides-a-catalogues-success)
  [`../README.md`](../README.md) with extra steps
- a **technical catalog** for query engines is what is meant — that is
  [`metadata-catalog/`](../../metadata-catalog/README.md), a completely different component
- the requirement is ownership, glossary, classification and lineage over internal tables —
  [OpenMetadata](../../platform/open-metadata/README.md)

## Notes

The only thing recorded here is the project link:

> <https://github.com/magda-io/magda>

Which is fair, because there is no deployment finding — nothing here was run. The
[`helm/`](helm/helmrelease.yaml) manifests point Flux at the project's Git repository at tag
`v4.2.3` and build from `deploy/helm/magda` in the source tree, with empty `values`. That is a
`GitRepository` source rather than a chart repository, which is the pattern used elsewhere in this
repo for projects that do not publish charts to a registry.

The useful note is therefore the categorical one, and it is worth stating clearly because Magda
appears in every list of open-source data catalogues, alongside tools that solve a different
problem:

**Magda is for open data portals — DCAT metadata, harvesting, public-facing search. It is not
internal platform metadata, and adopting it for internal discovery is the wrong tool.**

The project is genuinely good at what it does, which is why the distinction matters rather than a
dismissal. Unlike [Amundsen](../amundsen/README.md) and [Atlas](../atlas/README.md) in this same
folder, Magda is **not dead** — it is maintained and in production at real organisations. It is
simply answering a question this platform is not asking.

If the question ever changes — if datasets from this platform have to be published to an external
audience with standards-compliant metadata — then Magda is a serious answer and nothing in
[`platform/`](../../platform/README.md) is.

---

[← Data catalogs](../README.md)
