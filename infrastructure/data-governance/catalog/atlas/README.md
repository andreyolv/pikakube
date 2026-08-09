[← Data catalogs](../README.md)

# Apache Atlas

<https://github.com/apache/atlas>
<https://github.com/manjitsin/atlas-helm-chart>

Deployment write-up:
<https://manjitsingh664.medium.com/deploying-apache-atlas-on-kubernetes-a880d91ce0b4>

---

## What it was

The Hadoop ecosystem's metadata and governance service. For years it was *the* answer to
classification, lineage and governance in an enterprise Hadoop estate, and it was integrated
across Hive, HBase, Sqoop and Kafka.

Its ideas were genuinely ahead of the field:

| Capability | Why it mattered |
|---|---|
| **A typed metadata model** | entities and relationships defined as types, extensible |
| **Classification propagation** | tag a column as PII and the tag follows it downstream through lineage |
| Lineage | captured from Hive and Spark hooks |
| **Ranger integration** | classifications drove access policy — governance and security joined |

The second and fourth rows together are the interesting part, and they are still not common: mark
a column sensitive once, have the marking flow to every derived table, and have access control
enforce it automatically. Most modern catalogues do the first two and stop.

## The state of the project

**The project and the Helm chart are both dead** for practical purposes.

Atlas is tied to the Hadoop ecosystem, and that ecosystem has receded. Development continues at a
very low rate, the deployment story on Kubernetes was never good, and the community chart that
existed is unmaintained.

Its dependencies are the other half of the problem: HBase and Solr, plus Kafka for the
notification path. That is a substantial Hadoop-era stack to operate for a metadata service, and
it is why nobody deploys it on Kubernetes by choice.

## Notes

Recorded from evaluating it here:

> Project and Helm chart both dead.

The chart referenced above is a community effort rather than an official one, which is itself the
signal — a project whose only Kubernetes packaging is a third-party chart and a Medium post is a
project that expects to be installed on VMs by a Hadoop distribution.

## What survives from it

Worth noting, because the ideas outlived the implementation:

| Atlas idea | Where it lives now |
|---|---|
| Classification propagation through lineage | [OpenMetadata](../../platform/open-metadata/README.md), partially |
| Typed, extensible metadata model | [DataHub](../../platform/datahub/README.md)'s entity model |
| Governance driving access control | still largely unsolved outside commercial platforms |
| Lineage from execution hooks | [OpenLineage](../../lineage/open-lineage/README.md), done better |

The third row is the honest gap. Atlas plus Ranger connected *classification* to *enforcement* —
tagging a column as sensitive actually restricted who could read it. Most current open-source
catalogues document sensitivity without enforcing anything, and closing that loop is still an open
problem. See [`security/`](../../../security/README.md) for the enforcement half.

## What to use instead

[OpenMetadata](../../platform/open-metadata/README.md) is the closest successor in ambition and it
installs, which is the deciding difference — see
[`platform/`](../../platform/README.md) for the comparison and the recorded findings on all three
options.

## Why it is still in the catalogue

Because "we could use Apache Atlas" is a sentence that still gets said, usually by someone
remembering it from a Hadoop deployment, and the answer deserves to be a line in a repository
rather than a week of investigation.

The same reasoning applies to [Amundsen](../amundsen/README.md) in the folder next door.

---

[← Data catalogs](../README.md)
