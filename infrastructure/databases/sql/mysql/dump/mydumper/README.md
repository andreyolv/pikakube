[← Logical dump](../README.md)

# mydumper

<https://github.com/mydumper/mydumper>

---

## The problem it solves

`mysqldump` is single-threaded and writes one file. On a database of any real size that is the
bottleneck — the dump takes hours and the restore takes longer, because both are serial.

mydumper parallelises both:

| | `mysqldump` | mydumper |
|---|---|---|
| Dump | single thread, one file | **parallel**, file per table and chunk |
| Restore (`myloader`) | serial replay | **parallel** |
| Consistency | possible, with locking care | consistent snapshot across tables |
| Selective restore | parse a large SQL file | file per table — trivial |
| Compression | pipe it yourself | built in |

The per-table files matter as much as the speed: restoring one table means loading one file
rather than extracting statements from a multi-gigabyte dump.

## When to use it

- **any database large enough that `mysqldump` is slow** — which is most of them
- major version upgrades, where a logical dump is required
- migrating between hosts, clouds or providers
- restoring a subset rather than everything

## When not to use it

- routine operational backup — [XtraBackup](../../mysql/README.md) is faster in both directions
- tiny databases, where `mysqldump` is one fewer tool

## Usage shape

```bash
mydumper  --host <h> --user <u> --outputdir /backup --threads 8 --compress
myloader  --host <h> --user <u> --directory /backup --threads 8
```

Thread count is the tuning knob. More threads means faster and more load on the source — worth
being deliberate about when dumping from a production primary, or dumping from a replica
instead.

## The reminder that matters

**Plan for the restore, not the dump.** A logical restore replays every statement and rebuilds
every index; it is routinely several times slower than producing the dump was.

Parallel restore is exactly why this tool exists, and it still does not make a logical restore
fast — it makes it feasible.

---

[← Logical dump](../README.md)
