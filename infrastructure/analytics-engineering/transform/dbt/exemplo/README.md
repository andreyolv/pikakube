[← dbt](../README.md)

# Example dbt project

A working dbt project used to exercise the setup documented in [../README.md](../README.md) —
models, seeds, tests, macros and snapshots against a local PostgreSQL.

---

## Running it

```bash
dbt run
dbt test
```

Setup — virtualenv, PostgreSQL, loading the sample tables — is in
[../README.md](../README.md#notes).

## What is in here

| Folder | Contents |
|---|---|
| `models/` | the transformations, and where `ref()` builds the dependency graph |
| `seeds/` | CSVs loaded as tables by `dbt seed` |
| `tests/` | custom SQL assertions, beyond the schema tests |
| `macros/` | reusable SQL |
| `snapshots/` | slowly changing dimension tracking |
| `analyses/` | SQL that is compiled but not materialised |

## Note on seeds

`dbt seed` loads the CSVs directly, and the parent README records why that is **not
recommended** for anything real: it is limited, and any correction has to be made in the file
itself. Loading through Python lets pandas clean the data first.

Useful here precisely because this is an example.

## Reference

- [dbt documentation](https://docs.getdbt.com/docs/introduction)
- [Discourse](https://discourse.getdbt.com/) · [Slack](https://community.getdbt.com/) · [blog](https://blog.getdbt.com/)

---

[← dbt](../README.md)
