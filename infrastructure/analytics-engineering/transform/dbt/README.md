[← Transform](../README.md)

# dbt

<https://github.com/dbt-labs/dbt-core>
<https://docs.getdbt.com/>

---

## The problem it solves

Transformation logic used to live inside ingestion tools and stored procedures: invisible,
unreviewable, untestable. dbt makes it **software** — SQL files in Git, with dependencies,
tests, documentation and environments.

What it actually provides:

| Capability | Detail |
|---|---|
| **Model graph** | models `ref()` each other; execution order is derived, not maintained |
| **Tests** | uniqueness, not-null, relationships, accepted values, plus custom SQL assertions |
| **Incremental models** | reprocess only new data instead of rebuilding daily |
| **Docs and lineage** | generated from the code, so they do not drift |
| **Macros and packages** | reuse instead of copy-paste |
| **Environments** | the same models built into dev, staging and production targets |

It compiles SQL and runs it in the warehouse. It does not process data itself — which is why it
pairs with an [orchestrator](../../../data-engineering/orchestration/README.md) rather than
replacing one.

## When to use it

- **the default** for SQL transformation — largest ecosystem, most packages, most practitioners
- transformation logic should be reviewed like code
- documentation and lineage should come from the models rather than a separate tool

## When not to use it

- you need column-level lineage and virtual environments — [SQLMesh](../sqlmesh/README.md) is more rigorous
- the transformation is not SQL — that is [`data-engineering/processing/`](../../../data-engineering/processing/README.md)

## The ecosystem worth knowing

| Project | What it adds |
|---|---|
| [dbt-utils](https://github.com/dbt-labs/dbt-utils) | the macros everyone ends up needing |
| [dbt-project-evaluator](https://github.com/dbt-labs/dbt-project-evaluator) | audits the project against modelling best practice — worth running early |
| [dbt-checkpoint](https://github.com/dbt-checkpoint/dbt-checkpoint) | pre-commit hooks for dbt projects |
| [Elementary](https://github.com/elementary-data/elementary) · [action](https://github.com/elementary-data/run-elementary-action) | data observability on top of dbt — anomalies, freshness, alerting |
| [MetricFlow](https://github.com/dbt-labs/metricflow) | the metrics layer — see [`semantic/`](../../semantic/README.md) |
| [dbt-adapters](https://github.com/dbt-labs/dbt-adapters) · [dbt-trino](https://github.com/starburstdata/dbt-trino) | warehouse adapters, including Trino |
| [dbt-fusion](https://github.com/dbt-labs/dbt-fusion) | the newer engine — [#31](https://github.com/dbt-labs/dbt-fusion/issues/31) · [#38](https://github.com/dbt-labs/dbt-fusion/issues/38) · [#39](https://github.com/dbt-labs/dbt-fusion/issues/39) · [#829](https://github.com/dbt-labs/dbt-fusion/issues/829) |
| [jaffle-shop-classic](https://github.com/dbt-labs/jaffle-shop-classic) | the reference example project |

**dbt-project-evaluator is the underrated one.** It catches the modelling problems that
accumulate silently — models with no tests, direct source references, fan-out, unused models —
before they become the shape of the project.

Small files on a lakehouse, with Athena and Iceberg:
[write-up](https://medium.com/@guilhermenoronha2001/athena-dbt-apache-iceberg-solving-the-small-files-problem-in-the-data-lake-2d9d99e80a6e)

---

## Notes

### Local setup

```bash
python3 -m venv venv
source venv/bin/activate
# deactivate

pip install dbt-core          # or: python3 -m pip install --upgrade dbt-core
dbt --version

dbt init exemplo              # first time only
```

### A Postgres to work against

```bash
# in Kubernetes
kubectl port-forward svc/postgres 5432

# or Docker
sudo docker run --name owspostgres -e POSTGRES_PASSWORD=1234 -p 5432:5432 -d postgres
```

Connect with DBeaver, then create the schema:

```sql
CREATE SCHEMA transactional;
```

### Loading the sample data

```bash
pip install sqlalchemy
pip install psycopg2-binary

python3 import_tables.py
```

```sql
SELECT * FROM transactional.city;
```

```bash
export PASS=postgres123
dbt run
```

> `dbt seed` also loads CSVs placed in the `seed` folder, but it is **not recommended**: it is
> limited, and any data adjustment has to be made in the file itself. Loading through Python
> lets pandas clean the data before it lands.

### The usual loop

```bash
dbt run
dbt test
dbt docs generate
dbt docs serve
```

### Private packages

<https://docs.getdbt.com/docs/build/packages#private-packages>

The docs recommend the first option, but are not clear about it — and it appears to work only
on dbt Cloud. That leaves the second and third: **SSH or token**.

Example project: [`exemplo/`](exemplo/README.md)

---

[← Transform](../README.md)
