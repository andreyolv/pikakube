[← Key-value stores](../README.md)

# Valkey

<https://github.com/valkey-io/valkey>

---

## The problem it solves

Redis, under the licence Redis used to have.

When Redis relicensed away from BSD in 2024, the Linux Foundation forked the last BSD-licensed
release as Valkey. Most of the long-standing Redis maintainers moved with it, and AWS, Google and
Oracle backed it.

| | Redis | Valkey |
|---|---|---|
| Licence | RSALv2 / SSPL, plus AGPL since 2025 | **BSD** |
| Protocol | — | **identical** |
| Clients | — | **unchanged** — drivers cannot tell them apart |
| Data files | — | compatible |
| Backers | Redis Ltd. | Linux Foundation, AWS, Google, Oracle |

The second and third rows are what make this a low-risk decision rather than a migration.
`redis-py`, Jedis, `go-redis` and every other client connect to Valkey without modification,
because it speaks the same protocol.

## When to use it

- **anything new** — this is the default recommendation for new deployments
- the licence is a genuine constraint on how the platform or product ships
- an existing Redis should be replaced without touching a single application
- long-term governance matters, and a foundation is preferred to a single vendor

## When not to use it

- an existing Redis deployment that works and where the licence is not a constraint — there is no
  technical reason to move
- a specific Redis Ltd. commercial feature or module is in use
- the ecosystem's very newest additions matter; Redis moves first on its own features

## The migration, honestly

For most deployments it is changing an image tag.

The data format is compatible, the protocol is identical, and clients require no changes. What
should still be checked:

| Check | Why |
|---|---|
| **Modules** | RedisJSON, RediSearch and friends are Redis Ltd.'s; Valkey has its own module story |
| Version parity | the projects have diverged since the fork; features added after it differ |
| Operator support | if an operator manages the deployment, confirm it supports Valkey |
| Managed services | cloud offerings are increasingly Valkey-based, and the naming varies |

The modules row is the only one likely to block a migration. Plain Redis usage — caching,
sessions, counters, queues — moves without incident.

## The realistic position for a platform

Not ideological. Two practical points:

**For new work, Valkey costs nothing and removes a question.** The licence conversation never
happens, and nothing about the deployment is harder.

**For existing work, moving is optional.** Redis with AGPL as an option is acceptable for a great
many uses, and churning a working cache to change a licence header is not obviously worth doing.

The sensible policy is therefore: existing Redis stays, new deployments use Valkey — which is a
decision that can be made once and then not revisited.

## Notes

Mapped as the licence-clean drop-in. For this platform the recommendation in
[`../README.md`](../README.md#8-how-this-applies-to-pikakube) is exactly the policy above: Redis
is what runs today, and Valkey is what new caches should use.

The two settings that decide behaviour under pressure apply identically here — `maxmemory` below
the container limit, and an eviction policy chosen deliberately. Being a fork does not change the
failure mode, and it is the failure mode that causes incidents rather than the licence.

---

[← Key-value stores](../README.md)
