[← Data lineage](../README.md)

# Egeria

<https://github.com/odpi/egeria>
<https://github.com/odpi/egeria-charts>

---

## What it is

Not a lineage tool. An **open metadata standard and integration framework**, from the ODPi project
under the Linux Foundation.

Its ambition is much larger than anything else in [`data-governance/`](../../README.md): a common
metadata model, and a protocol for tools to exchange metadata with each other, so that a catalogue,
a lineage tool, a quality tool and a security tool share one understanding of the estate rather
than four.

| Concept | What it is |
|---|---|
| **Open Metadata Types** | a standard type system for datasets, processes, people, governance |
| **Open Metadata Repository Services (OMRS)** | a federation protocol between metadata repositories |
| Integration connectors | to bring metadata in from real systems |
| **Governance Action Framework** | governance as executable actions, not documentation |
| Servers | metadata access, integration and engine host servers |
| Egeria UI | reference interfaces over the above |

## The idea worth understanding

Every other tool in this discipline builds **its own** metadata model and its own connectors. Move
from DataHub to OpenMetadata and the model, the ingestion and the integrations are all re-done.

Egeria's proposition is a **standard** underneath, so metadata federates between repositories
rather than being re-collected — which is the same argument
[OpenLineage](../open-lineage/README.md) makes for lineage events, applied to all metadata.

That is a genuinely good idea and it is why the project exists under a foundation rather than a
vendor.

## When to use it

- a **large enterprise metadata programme**, with dedicated people
- several metadata tools already exist and must interoperate
- the standard itself is the requirement — a regulated environment where the model matters
- a metadata strategy spanning years rather than quarters

## When not to use it

- **almost every other case** — the surface is far larger than a platform team can absorb
- lineage is the requirement — [OpenLineage](../open-lineage/README.md) into
  [Marquez](../marquez/README.md) answers it with a fraction of the effort
- a catalogue is the requirement — [`platform/`](../../platform/README.md)
- there is no dedicated metadata team; this needs one

## The honest assessment

Egeria is ambitious, well-governed, and disproportionate to most problems.

Its concept count is the practical obstacle. Understanding what to deploy requires learning
several server types, a repository federation protocol, a type system and a connector framework —
before any metadata moves. That investment makes sense when metadata integration across many tools
*is* the programme; it makes no sense when the requirement is a lineage graph.

The comparison worth holding:

| Requirement | Tool | Effort |
|---|---|---|
| Lineage | [OpenLineage](../open-lineage/README.md) + [Marquez](../marquez/README.md) | configuration |
| Catalogue | [OpenMetadata](../../platform/open-metadata/README.md) | a deployment |
| **Metadata interoperability across an enterprise** | **Egeria** | **a programme** |

There is nothing wrong with the third row. It is simply a different size of undertaking, and
adopting it for the first row's requirement is the mistake this page exists to prevent.

## Notes

Mapped with the [official charts](https://github.com/odpi/egeria-charts).

Nothing here is deployed and nothing should be. It is catalogued for two reasons:

**The idea is worth knowing.** A standard metadata model underneath the tools is the correct
long-term answer to a real problem — every catalogue re-collecting the same metadata in its own
format — and it is useful to know that a serious attempt exists.

**Its scale is a useful calibration.** Placing Egeria beside Marquez in the same folder makes the
range of this discipline visible: the same word, "lineage", covers a configuration change and a
multi-year enterprise programme. Knowing which one a requirement calls for is most of the decision.

For this platform, the answer is the first row of that table, and
[`../README.md`](../README.md#7-how-this-applies-to-pikakube) says why.

---

[← Data lineage](../README.md)
