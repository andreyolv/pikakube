[← Data contracts](../README.md)

# datacontract-cli

<https://github.com/datacontract/datacontract-cli>
<https://github.com/datacontract/datacontract-specification>
<https://github.com/datacontract/datacontract-editor>

---

## The problem it solves

A contract is only worth writing if something executes it. This is the piece that does: a CLI that
**lints** a contract file and **tests it against the real data source**.

```bash
datacontract lint          # is the contract itself valid?
datacontract test --server production   # does the actual data match it?
```

Those two commands are what turn a YAML file into a control. `lint` runs on every commit; `test`
runs against a real database or bucket and fails if the data no longer matches what was promised.

| Capability | Detail |
|---|---|
| **Lint** | validates the contract against the specification |
| **Test** | connects to the source and verifies schema and quality expectations |
| `init --template` | scaffolds a contract from a template |
| Import | generate a contract from an existing schema |
| Export | to dbt, Avro, JSON Schema, SQL DDL, and others |
| **Multi-source** | Postgres, S3, Kafka, Delta, Snowflake, BigQuery |

The export capability is worth noting: one contract can generate dbt model schemas, Avro
definitions and DDL — so the contract becomes the source rather than a fourth description of the
same thing.

## Installation

The connectors are extras, installed per source type:

```bash
pip install datacontract-cli[postgres]
pip install datacontract-cli[s3]
pip install datacontract-cli[kafka]
pip install datacontract-cli[deltalake]
```

Testing is implemented on [Soda](../soda/README.md)'s engine underneath — the
[connection implementations](https://github.com/chgl/datacontract-cli/tree/main/datacontract/engines/soda/connections)
are worth reading when a source does not behave as expected.

## The CI shape

The intended usage, and the one that makes it a control rather than documentation:

| Step | Where |
|---|---|
| `datacontract lint` | on every commit, with `datacontract.yaml` at the repository root |
| `datacontract test --server <env>` | against the environment matching the branch |
| Fail the build | so a breaking change does not merge |

Running this in the **producer's** repository is the whole point — see
[`../README.md`](../README.md#3-where-it-runs-which-is-the-whole-point). The same commands run
from a consumer's pipeline are a quality check with extra steps.

## Notes

Recorded from evaluating it, including the questions that are genuinely the hard part:

> `datacontract lint` — keep the `datacontract.yaml` file at the repository root.
>
> `datacontract test --server` — the server changes per branch, for validation against the right
> environment.
>
> **Open questions:**
> - How does the contract connect to the data source — a service principal? environment
>   variables?
> - Where are the environment variables set — in GitHub Actions?
> - What if there are several service principals in one repository?
>
> How does this join up with monitoring and alerting in Airflow?
>
> Custom fields can be added to the YAML without breaking `lint`, which is useful.

Those questions are the right ones, and they are where adoption actually stalls. The contract file
is easy; **giving CI credentials to read production data is not.**

The realistic answers:

| Question | Approach |
|---|---|
| **How does it authenticate?** | environment variables, read from CI secrets — the connection implementations show which variables each source expects |
| **Where do they live?** | GitHub Actions secrets, or better, an OIDC-federated identity so no long-lived credential exists |
| **Several principals in one repo?** | one server block per environment in the contract, each with its own variable names; the workflow selects which to inject |
| **Joining to Airflow alerting?** | `datacontract test` returns a non-zero exit code, so it runs as a task and fails the DAG — the alert path is then the platform's existing one, see [`alerting/`](../../../observability/alerting/README.md) |

The multiple-principals point deserves emphasis, because it is where the design decision sits: a
contract with several `servers` entries, each naming its own credential variables, keeps the
contract portable across environments without embedding anything secret in it.

The **custom fields** observation is a genuinely useful finding. The specification tolerates
additional keys, so organisation-specific metadata — a cost centre, a system of record, a
retention class — can travel with the contract without a fork or a broken lint.

For this platform, the shape that would work: contracts in the producing repository, `lint` on
every commit, and `test` as an
[Airflow](../../../data-engineering/orchestration/airflow/README.md) task so that a contract
violation fails the DAG and reaches the same alerting path as everything else.

---

[← Data contracts](../README.md)
