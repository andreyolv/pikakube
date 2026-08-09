[← Unit and integration testing](../README.md)

# Testcontainers

<https://github.com/testcontainers/testcontainers-python>

<https://testcontainers.com/guides/getting-started-with-testcontainers-for-python/>
<https://golang.testcontainers.org/quickstart/>
<https://node.testcontainers.org/quickstart/>

---

## The problem it solves

**Integration tests that run against the real dependency, started from inside the test and thrown
away afterwards.**

The historical choice for testing code that talks to a database was bad in both directions: mock it
and test nothing, or share one test database and inherit every flake that comes with shared state.

Testcontainers removes the choice. A few lines in the test start a **real PostgreSQL container**, and
the library hands back the connection string. Migrations run against it, the tests run, the container
is destroyed.

| What it replaces | Why it was a problem |
|---|---|
| **A mocked database** | asserts your beliefs about SQL, not SQL — no dialect errors, no constraints, no migrations |
| **A shared test database** | fixture pollution, order dependence, schema drift, "someone is running migrations" |
| **A local install everyone maintains** | version drift between developers and CI |
| **docker-compose started by hand** | lifecycle managed outside the test, so it is forgotten or left running |

The last row is the underrated one. The container's lifecycle belongs to the test process, so there
is nothing to start beforehand and nothing left behind — the same command works locally and in CI.

It is not only databases: brokers, caches, object stores, search engines, and any image at all
through a generic container API.

## When to use it

- **integration tests against a database** — the highest-value use, by a wide margin
- anything with a wire protocol: RabbitMQ, Kafka, Redis, MinIO, Elasticsearch
- verifying that **migrations actually apply**, on every run
- reproducing a production version exactly — the same image tag as the deployed cluster
- replacing a shared test database that has become a source of flakes

## When not to use it

- **unit tests** — a test that starts a container is not a unit test; keep the layers separated by
  marker, per [`unit/`](../README.md) section 1
- **CI with no usable container runtime** — it needs a Docker socket, and some sandboxed runners do
  not provide one; this is the real adoption blocker
- when the dependency is a third party you cannot run — mock it, or use a fake; see
  [`test-double/`](../../test-double/README.md)
- fast feedback on every save — container startup is measured in seconds
- as a way to run the whole system for end-to-end tests; that is a different layer with a different
  cost

## Notes

Four links were recorded, and the shape of that list is the point:

**<https://github.com/testcontainers/testcontainers-python>** — the Python implementation, matching
[`language/python/`](../../../language/python/README.md) as the primary language here.

**<https://testcontainers.com/guides/getting-started-with-testcontainers-for-python/>** — the Python
quickstart.

**<https://golang.testcontainers.org/quickstart/>** — the **Go** quickstart.

**<https://node.testcontainers.org/quickstart/>** — the **Node** quickstart.

Recording three languages rather than one says what testcontainers actually is: **not a Python
library, but the same idea implemented per language**, with a shared model and per-language APIs.
That matters for this repository because [`language/`](../../../language/README.md) covers Python and
Go, so the same integration-testing approach carries across both — one pattern to learn, not two.

Nothing is deployed for it. It is a test dependency of the application, and its only infrastructure
requirement is that **CI can reach a container runtime**. That is worth checking before adopting it,
because it is the one thing that can make the whole approach unavailable.

The practices that make it fast rather than slow:

| Practice | Why |
|---|---|
| **One container per session**, not per test | startup is the cost; pay it once |
| **Roll back a transaction per test** for isolation | far cheaper than recreating the schema |
| **Run the real migrations** against it | half the value is proving they apply |
| **Pin the image tag** to the production version | the point is to match the dialect and behaviour |
| **Wait on a readiness condition**, not a sleep | the library provides wait strategies; use them |
| Reuse containers locally where supported | a faster inner loop, at the cost of a clean slate |

For pikakube specifically, the image to pin is the **PostgreSQL version running under CloudNativePG**
in [`databases/`](../../../../databases/README.md). Testing against a different major version defeats
the purpose — the reason to run a real database is that the behaviour matches the deployed one.

---

[← Unit and integration testing](../README.md)
