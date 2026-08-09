[← Data governance](../README.md)

# Data contracts

Moving quality from the consumer, where it is discovered, to the producer, where it is caused.

Tools covered: [`datacontract-cli`](datacontract-cli/README.md) · [`soda`](soda/README.md)

Standard: <https://github.com/bitol-io/open-data-contract-standard>
Further reading: <https://github.com/AltimateAI/awesome-data-contracts> ·
<https://github.com/datamesh-manager/datamesh-manager-ce/>

## Contents

1. [The problem](#1-the-problem)
2. [What a contract contains](#2-what-a-contract-contains)
3. [Where it runs, which is the whole point](#3-where-it-runs-which-is-the-whole-point)
4. [The tools](#4-the-tools)
5. [Adopting them without boiling the ocean](#5-adopting-them-without-boiling-the-ocean)
6. [Anti-patterns](#6-anti-patterns)
7. [How this applies to pikakube](#7-how-this-applies-to-pikakube)

---

## 1. The problem

[`quality/`](../quality/README.md) checks data **after it arrives.** That catches problems, and it
catches them at the wrong end:

| | Quality checks | Data contracts |
|---|---|---|
| Run at | the consumer | **the producer** |
| Detect | a problem that already happened | a change **before it ships** |
| The fix | a conversation with the upstream team | the upstream build fails |
| Who is inconvenienced | the person who did not cause it | the person who did |

The recurring incident: an upstream team renames a column, drops a field, or changes a type. Their
tests pass — their application still works. The downstream pipeline breaks, and the downstream
team finds out from a failed DAG.

Nobody did anything wrong. There was simply no statement anywhere about what the downstream
depended on.

A data contract is that statement, in a machine-readable form, tested in the producer's CI.

## 2. What a contract contains

| Section | What it declares |
|---|---|
| **Schema** | fields, types, nullability — the shape |
| **Quality expectations** | uniqueness, ranges, freshness, volume |
| **Ownership** | who is responsible, and how to reach them |
| **SLAs** | how fresh, how available, how often |
| Semantics | what the fields actually mean |
| Versioning | how it changes, and what counts as breaking |
| Terms of use | who may consume it, and for what |

The ownership and SLA rows are the ones that make it a **contract** rather than a schema
definition. A schema says what the data looks like; a contract says who is accountable when it is
not that.

**Semantics is the section that is hardest and most valuable.** "`status` is a string" is a
schema. "`status` is one of these five values, `cancelled` means cancelled before dispatch, and a
sixth value has not been used since 2021" is what a consumer actually needs.

## 3. Where it runs, which is the whole point

A contract file that nobody executes is documentation, and documentation drifts.

The value comes entirely from where the check runs:

| Position | Effect |
|---|---|
| **In the producer's CI** | a breaking change fails their build — this is the goal |
| In the producer's pipeline | bad data never published |
| In the consumer's pipeline | better than nothing; it is a quality check with extra steps |
| Nowhere | a YAML file that describes what used to be true |

The first row is what distinguishes this from [`quality/`](../quality/README.md). If the contract
is only ever checked downstream, the producer never experiences the constraint and nothing about
the dynamic has changed.

## 4. The tools

| Tool | Where it shines | Detail |
|---|---|---|
| **datacontract-cli** | **the specification plus a CLI** — lint, test against a real source, and run in CI | [→](datacontract-cli/README.md) |
| **Soda** | the check engine — the same tool used from the quality side, applied to the contract | [→](soda/README.md) |

[ODCS](https://github.com/bitol-io/open-data-contract-standard) — the Open Data Contract Standard,
from the Bitol project under the Linux Foundation — is the emerging specification, and worth
preferring over a bespoke format for the usual reason: tooling that reads a standard is
replaceable.

[Data Mesh Manager](https://github.com/datamesh-manager/datamesh-manager-ce/) is the adjacent
category: contracts as part of a data-product catalogue with a subscription model between
producers and consumers. Relevant when contracts are being adopted as an organisational programme
rather than as a technique.

## 5. Adopting them without boiling the ocean

Contracts fail when they are adopted as a policy — "every dataset needs a contract" — because that
is an enormous amount of work, most of it on interfaces that have never broken.

The order that works:

**1. The boundaries that have already caused incidents.** The interfaces where an upstream change
broke something downstream. There are usually few of them, and everyone can name them.

**2. Schema and freshness only.** The two things that break most often. Semantics and SLAs can
come later.

**3. In the producer's CI.** This is the step that changes behaviour, and skipping it makes the
rest theatre.

**4. Extend where it pays.** More fields, more expectations, more datasets — driven by incidents
rather than by a checklist.

## 6. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Contracts for every dataset | enormous effort, mostly on interfaces that never break | start where incidents happened |
| Checked only in the consumer's pipeline | the producer never feels the constraint | run it in their CI |
| A contract nobody executes | documentation, and it drifts | automate it |
| Schema only, no ownership | it says what, and not who to call | ownership is what makes it a contract |
| No versioning strategy | any change is either breaking or ignored | define what breaking means |
| Contracts imposed on producers | they become a compliance exercise, filled in minimally | agree them; both sides benefit |
| A bespoke format | tooling becomes yours to maintain | [ODCS](https://github.com/bitol-io/open-data-contract-standard) |
| Contracts without quality checks | the shape is guaranteed and the content is not | pair with [`quality/`](../quality/README.md) |

## 7. How this applies to pikakube

Mapped, with real depth on
[datacontract-cli](datacontract-cli/README.md) — including the CI shape, the installation extras
per source type, and a set of open questions about credentials that are the genuinely hard part of
adopting this.

The recorded finding on [Soda's contract module](soda/README.md) is that its documentation is
broken and the module it describes does not import. That is worth knowing before choosing it as
the contract engine, and it does not affect Soda's use from the
[quality](../quality/README.md) side, which works.

Where this connects for the platform:

- [`quality/`](../quality/README.md) — the same checks, run at the other end
- [`api-contract/`](../../docs/api-contract/README.md) — the same idea for interfaces; AsyncAPI is
  the event equivalent
- [`data-streaming/schema-registry/`](../../data-streaming/schema-registry/README.md) — enforcement
  for streaming payloads, which is a contract with teeth

The honest position: contracts matter when there is more than one team, and this platform has one.
The technique is worth having documented because it is the answer to the most common data-platform
complaint — *"upstream changed something and broke us"* — and that complaint has no technical fix
at the consumer end.

---

[← Data governance](../README.md)
