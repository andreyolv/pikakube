[← Data governance](../README.md)

# Anonymization

How lower environments get realistic data without becoming a privacy incident.

Tools covered: [Neosync](https://github.com/nucleuscloud/neosync)

## Contents

1. [The problem](#1-the-problem)
2. [Four approaches](#2-four-approaches)
3. [What makes anonymization hard](#3-what-makes-anonymization-hard)
4. [Neosync](#4-neosync)
5. [Anti-patterns](#5-anti-patterns)
6. [How this applies to pikakube](#6-how-this-applies-to-pikakube)

---

## 1. The problem

Development and staging environments need data that behaves like production — real distributions,
real edge cases, real volume. The path of least resistance is restoring a production dump, and
that is how personal data ends up in an environment with weaker access controls, no audit, and
credentials shared across a team.

It is rarely a decision. It is a restore somebody ran once because the bug only reproduced with
real data.

| The reasoning | What actually happened |
|---|---|
| "We need realistic data to test" | production personal data now exists in staging |
| "It is only a subset" | the subset is still real people |
| "Access is restricted" | to a wider group than production, with no audit |
| "It gets refreshed monthly" | so the exposure is continuous rather than one-off |

Under GDPR and comparable regimes this is processing personal data outside its stated purpose,
and the environments involved are the ones least likely to survive an audit.

## 2. Four approaches

| Approach | What it does | Keeps data realistic | Reversible |
|---|---|---|---|
| **Masking** | replaces values with fake ones of the same shape | mostly | no |
| **Pseudonymisation** | replaces identifiers with consistent tokens | yes | **yes, with the key** |
| **Synthetic generation** | creates data from a model of the real data | depends | no |
| **Subsetting** | takes a referentially-complete slice | yes — it is real data | **it is still real data** |

The distinction that matters legally: **pseudonymised data is still personal data**, because it
can be re-identified with the mapping. Only genuinely anonymised data falls outside the
regulation.

Subsetting is worth separating out because it is frequently mistaken for anonymisation. A
referentially-consistent 1% slice of production is smaller and just as personal.

In practice the useful combination is **subset, then mask** — a small slice with a complete
referential graph, with the personal fields replaced.

## 3. What makes anonymization hard

Not the masking itself. Four things around it:

**Referential integrity.** A `customer_id` masked in one table must be masked identically in the
twenty tables referencing it, or the database no longer joins. This is the single biggest source
of failure, and it is why naive per-column masking produces an unusable database.

**Format preservation.** A masked email must still look like an email, a masked postcode must
still validate, and a masked card number must still pass a Luhn check — otherwise application
validation rejects the data and nothing can be tested.

**Distribution preservation.** If 80% of orders are in one country and masking randomises it
uniformly, query plans change and performance testing becomes meaningless.

**Re-identification.** Removing names is not anonymisation. A date of birth, a postcode and a
gender identify most individuals uniquely. Anonymising the obvious fields while leaving the
quasi-identifiers is the common and comfortable mistake.

The last one is worth taking seriously: whether data is anonymous is a property of the whole
dataset, not of the fields that were changed.

## 4. Neosync

[Neosync](https://github.com/nucleuscloud/neosync) is the tool mapped here, and it addresses the
list above rather than just the masking step:

| Capability | Why it matters |
|---|---|
| **Referentially-consistent transformation** | the same input maps to the same output across every table |
| **Subsetting** | a slice with its foreign-key graph intact |
| Format-preserving transformers | emails, names, addresses that still validate |
| Synthetic generation | where masking is not enough |
| **Pipelines** | production → anonymised → lower environment, repeatable |
| Kubernetes-native | Helm-deployed, API-driven |

The first row is the one that makes it a tool rather than a script. Deterministic transformation —
the same `customer_id` always producing the same fake value — is what keeps the database joinable,
and it is exactly what an ad-hoc `UPDATE` statement does not do.

## 5. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Restoring production into staging | personal data in an environment with weaker controls | anonymise in the pipeline |
| Masking only the obvious fields | quasi-identifiers re-identify most people | consider the dataset, not the columns |
| Per-column masking with no consistency | the database stops joining and becomes untestable | deterministic, referentially-consistent transformation |
| Subsetting called anonymisation | a smaller amount of real personal data | subset **and** mask |
| Random values that break validation | application-level validation rejects them | format-preserving transformers |
| A one-off anonymisation script | correct once, drifts as the schema changes | a pipeline, run on refresh |
| Keeping the mapping table forever | pseudonymised data is still personal data | discard the key, or protect it like production |
| Anonymising after loading | the raw data existed in the target, briefly and permanently in the logs | transform in transit |

## 6. How this applies to pikakube

Mapped, not deployed — and it is the capability in
[`data-governance/`](../README.md) least likely to be needed in a homelab and most likely to
matter in the corporate case this repository is modelling.

The connections that already exist here:

- [`quality/`](../quality/README.md) — the same pipeline position; a transformation step between
  source and target
- [`contract/`](../contract/README.md) — a data contract can declare which fields are personal,
  which makes anonymisation a policy rather than a list someone maintains
- [`security/`](../../security/README.md) — classification and access control are the other half; masking
  is what you do when access control is not enough
- [`analytics-engineering/integration/`](../../analytics-engineering/integration/README.md) — the
  extraction tooling that would carry the transformation

The point worth carrying: **anonymisation belongs in the pipeline, not as a cleanup step.** Once
production data has been written to a lower environment, it has also been written to that
environment's logs, backups and replicas — and removing it afterwards is not something a `DELETE`
accomplishes.

---

[← Data governance](../README.md)
