[← Operators](../README.md)

# Kopf

<https://github.com/nolar/kopf>
<https://github.com/yashvardhan-kukreja/pycon-india-2021-talk>
<https://www.youtube.com/watch?v=JwLP2RJA8d4>

---

## The problem it solves

Kubernetes Operator Pythonic Framework. Writing an operator in Go with `controller-runtime` means
scaffolding, code generation, informers, work queues and a project layout. Kopf makes it a Python
file with decorators:

```python
@kopf.on.create('example.com', 'v1', 'mycrds')
def create_fn(spec, **kwargs):
    ...
```

The framework handles watching, queuing, retries with backoff, status updates and finalizers. What
you write is the handler. For a team that writes Python and not Go, that is the difference between an
operator existing and the idea being abandoned at the scaffolding stage.

## When to use it

- The team writes Python and does not write Go
- Internal automation: provisioning backing services, reacting to custom resources, glue
- Prototyping an operator before committing to a Go implementation
- The domain logic is the hard part and Kubernetes plumbing is incidental

## When not to use it

- Operators distributed to other people — Go and [Operator SDK](../operator-framework/README.md) are the ecosystem norm
- High-frequency reconciliation at large scale; Python's performance profile becomes relevant
- Where typed clients and compile-time checking against the API matter
- When the project's maintenance status is a concern — check before committing

## Notes

**This is the most complete piece of original work in this part of the repository.** Not a link, not
a chart — a working operator:

| File | What it is |
|---|---|
| `docker/operator.py` | the Kopf entry point |
| `docker/kafka.py`, `minio.py`, `mongo.py`, `postgres.py` | per-backend handlers |
| `docker/Dockerfile`, `build.sh`, `requirements.txt` | the image |
| `kubernetes/crds/kafkagen.yaml`, `miniogen.yaml`, `postgresgen.yaml` | the CRDs |
| `kubernetes/deployment.yaml`, `rbac.yaml`, `namespace.yaml` | how it runs |
| `examples/kafkagen.yaml`, `miniogen.yaml`, `mongogen.yaml`, `postgresgen.yaml` | sample resources |

The design is the interesting part: one operator, several resource kinds — `KafkaGen`, `MinioGen`,
`MongoGen`, `PostgresGen` — each handled by its own module. Apply a `PostgresGen` and the operator
provisions what a Postgres consumer needs. That is a small internal platform: developers ask for a
database in a manifest instead of asking a person.

Note the asymmetry worth flagging: there are **four handler modules and example resources for four
kinds, but only three CRDs** — `mongogen.yaml` is missing from `kubernetes/crds/`. Either it lives
elsewhere or it was never committed; applying `examples/mongogen.yaml` against this CRD set will
fail with "no matches for kind".

**Learning references recorded:**

- <https://github.com/yashvardhan-kukreja/pycon-india-2021-talk> — the accompanying repository
- <https://www.youtube.com/watch?v=JwLP2RJA8d4> — the talk itself

A conference talk plus its repository is a good way into this framework: Kopf's own documentation is
thorough on mechanics and thin on how a complete operator is shaped, and a talk fills exactly that
gap.

**Before extending this**, the three things that separate a working operator from a good one:

- **RBAC.** `rbac.yaml` is where the operator's power is defined. An operator that creates
  StatefulSets, Services and Secrets across namespaces has broad permissions by necessity; keep them
  enumerated rather than wildcarded.
- **Idempotency.** Handlers are called again — on operator restart, on resource update, on resync.
  Creating rather than converging produces duplicates.
- **Finalizers.** If the operator provisions anything outside the cluster, deletion needs a finalizer
  and the finalizer needs to work. A broken one leaves objects that cannot be deleted; the recovery
  commands are in [`core/`](../../core/README.md).

**Project status is the one caution.** Kopf's development has been quiet. It works, and it is not
where a long-lived production operator should be started without checking the repository first.

---

[← Operators](../README.md)
