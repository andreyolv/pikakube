[← Logical dump](../README.md)

# mysql-client

<https://dev.mysql.com/doc/refman/9.7/en/mysqldump.html>

---

## What it is

The standard MySQL command-line tools — `mysql` and `mysqldump`. Present everywhere, no
installation decisions, and the thing that will exist on any host.

## When it is the right choice

- **small databases**, where parallelism buys nothing
- ad-hoc work: dumping one table, inspecting a schema, running a query
- environments where installing [mydumper](../mydumper/README.md) is not worth the step
- scripts that must work anywhere without dependencies

## When it is not

- anything large. Single-threaded dump **and** single-threaded restore, which is the ceiling —
  see [mydumper](../mydumper/README.md)
- selective restore from a large dump, which means parsing a huge SQL file

## The options that matter

```bash
mysqldump --single-transaction --routines --triggers --events \
          -u <user> -p <database> > dump.sql
```

| Option | Why |
|---|---|
| `--single-transaction` | consistent dump of InnoDB **without locking the tables** — omitting it blocks writes for the duration |
| `--routines` | stored procedures and functions, which are **not** included by default |
| `--triggers` | included by default, but worth being explicit |
| `--events` | scheduled events, also excluded by default |

The omissions are the trap. A default `mysqldump` silently leaves out routines and events, and
the restored database looks complete until something calls a procedure that is not there.

## Restoring

```bash
mysql -u <user> -p <database> < dump.sql
```

Serial, and slower than the dump was. See
[`../README.md`](../README.md#the-thing-that-catches-people).

---

[← Logical dump](../README.md)
