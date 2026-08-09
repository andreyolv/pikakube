[← Document stores](../README.md)

# TinyDB

<https://github.com/msiemens/tinydb>

---

## The problem it solves

A document store **in a Python file**. No server, no dependency beyond the library, and the
database is a JSON file on disk.

```python
from tinydb import TinyDB, Query
db = TinyDB('state.json')
db.insert({'name': 'nightly-load', 'last_run': '2026-08-08'})
Job = Query()
db.search(Job.name == 'nightly-load')
```

It is not competing with anything else in [`document/`](../README.md). It occupies the position
that [SQLite](../../../sql/sqlite/README.md) occupies for relational data: the right answer when
a script needs to remember something and a database server would be absurd.

## When to use it

- **a script or a CLI that needs to persist state** between runs
- tests, where a real document store would be scaffolding
- prototyping a data model before deciding where it will actually live
- small tools where the data is measured in hundreds of records

## When not to use it

- **concurrent writers** — it is a JSON file with no locking worth the name
- more than a few thousand records; the whole file is read into memory
- anything a service depends on
- a real document workload — [MongoDB](../mongo/README.md), or PostgreSQL `JSONB`

## The honest scope

The entire file is loaded, modified in memory, and written back. That is fine for a few hundred
documents and unusable beyond a few thousand — and there is no gradual degradation, it simply
becomes slow and then memory-bound.

There is also no concurrency story. Two processes writing to the same TinyDB file will lose data,
and nothing will report an error.

Those are not defects. They are the trade that makes it a single dependency with no setup, and
the mistake is only in expecting otherwise.

## The comparison worth knowing

| | TinyDB | [SQLite](../../../sql/sqlite/README.md) |
|---|---|---|
| Model | documents | relational |
| Query | a Python API | SQL |
| Concurrency | none | one writer, many readers |
| Scale | hundreds of records | **millions** |
| Dependency | a pure-Python library | in the standard library |
| Durability | rewrite the file | WAL, and [Litestream](../../../sql/sqlite/litestream/README.md) |

**SQLite is usually the better choice** even for this size of problem, because it is in Python's
standard library, handles vastly more data, and has real transactions. TinyDB wins when the data
is genuinely document-shaped and the schema is still changing — which is a narrow but real case.

## Notes

Mapped as the smallest thing in the category, and included for the same reason SQLite is included
in [`sql/`](../../../sql/README.md): the in-process option is consistently underrated, and having
it in the catalogue makes "do we need a database for this?" a question with a third answer.

For platform work the realistic use is a **utility script** — a maintenance job, a one-off
migration helper, a CLI that caches results between invocations. Reaching for
[Redis](../../key-value/redis/README.md) or a Postgres table for that is how small tools acquire
infrastructure dependencies they do not need.

---

[← Document stores](../README.md)
