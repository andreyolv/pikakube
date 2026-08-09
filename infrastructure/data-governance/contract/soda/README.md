[← Data contracts](../README.md)

# Soda — contracts

<https://github.com/sodadata/soda-core>

---

## What this folder is

Soda appears twice in [`data-governance/`](../../README.md), from two directions:

| Folder | Role |
|---|---|
| [`quality/soda/`](../../quality/soda/README.md) | checks run by the **consumer**, after data arrives |
| **`contract/soda/`** | the same engine expressing a **producer's promise** |

The engine is the same; what changes is who owns the file and where it runs. That is the
distinction made in [`../README.md`](../README.md#3-where-it-runs-which-is-the-whole-point), and
it is the only thing that separates a contract from a quality check.

It also underpins [datacontract-cli](../datacontract-cli/README.md), whose `test` command uses
Soda's connection and check machinery underneath.

## Installation

```bash
pip install soda-core-contracts
```

## Notes

Recorded from actually trying it:

> Documentation is poor.
>
> ```
> ModuleNotFoundError: No module named 'soda.contracts.data_contract_translator'
> ```
>
> Reference: <https://github.com/anoop-qasolve/soda-core/tree/main/soda/contracts>

That is a real blocker, and it is worth being precise about what it means: the documented import
path does not exist in the installed package. The contracts module has moved between locations
across Soda's releases, and the documentation has not tracked it.

The practical consequence: **the version installed and the documentation being read are almost
certainly not the same generation.** Resolving it means reading the source of the installed
package rather than the docs — which is possible and is not what a contract tool should require.

## What to use instead

For contracts specifically, [datacontract-cli](../datacontract-cli/README.md) is the better entry
point, and for a reason beyond this bug:

| | Soda contracts | datacontract-cli |
|---|---|---|
| Format | Soda's own | **[ODCS](https://github.com/bitol-io/open-data-contract-standard)**, an open standard |
| Engine | Soda | **Soda**, underneath |
| Documentation | recorded as broken | workable |
| Exports | no | dbt, Avro, JSON Schema, DDL |
| Lock-in | the format is Soda's | the format is a standard |

So the recommended combination is **datacontract-cli for the contract, Soda for the checks** —
which is what datacontract-cli does anyway, and it means the contract file is written against a
specification rather than against one vendor's tool.

## Where Soda does work well

Worth saying clearly, because this page is otherwise negative: **the quality side is solid.**

[`quality/soda/`](../../quality/soda/README.md) has a complete working example here — the
PostgreSQL connection configuration, the scan commands, and an Airflow orchestration pattern.
Checks as YAML, executed in a pipeline, failing when the data is wrong.

The finding on this page is specific to the contracts module and its documentation, not to Soda as
a check engine.

---

[← Data contracts](../README.md)
