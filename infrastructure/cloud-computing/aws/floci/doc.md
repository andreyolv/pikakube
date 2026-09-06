https://github.com/floci-io/floci
https://github.com/floci-io/floci-ui

Local AWS emulator. MIT, no account, no auth token, ~84 services on port **4566** —
the same port [localstack](../localstack/doc.md) uses, so pointing an SDK at one or the other is
an endpoint change and nothing else.

Why it exists: LocalStack's community edition sunset in March 2026. That is the reason to have
this recorded, not the benchmarks.

- stateless services run in-process; Lambda, RDS, ElastiCache, ECS, EKS, MSK and friends run as
  real containers, so the Docker socket has to be mounted
- storage backends: memory, persistent, hybrid, or write-ahead log
- Testcontainers modules for Java, Node and Python
- `docker compose up`, or `floci start` with the CLI

**floci-ui** — <https://github.com/floci-io/floci-ui> — is the console over it: an AWS-Console-style
web UI on port **4500** that reads real state from the running runtimes, not mock data. It talks to
all three at once, which is the reason it is filed here rather than under one cloud:

| Runtime | Port | Folder |
|---|---|---|
| AWS — floci | 4566 | this one |
| Azure — floci-az | 4577 | [`azure/floci/`](../../azure/floci/doc.md) |
| GCP — floci-gcp | 4588 | [`gcp/floci/`](../../gcp/floci/doc.md) |

`docker compose --profile multicloud up` brings up the set.
