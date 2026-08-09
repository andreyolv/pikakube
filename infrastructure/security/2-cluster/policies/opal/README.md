[← Admission policies](../README.md)

# OPAL

<https://github.com/permitio/opal>
<https://github.com/permitio/opal-helm-chart>

Open Policy Administration Layer. It does not decide anything — it keeps OPA's **policies and data**
up to date in real time from Git and from external sources.

---

## The problem it solves

OPA answers questions using two inputs: the policy (Rego) and the data it can see. Rego can express
"deny if the requesting team's quota is exhausted"; it cannot *fetch* the quota. Whatever OPA does
not already hold, it cannot reason about.

That leaves two bad options for anything that depends on state outside the policy bundle:

| Option | Problem |
|---|---|
| Call out to an API during evaluation | the decision is now as slow and as available as that API — on the admission path, that is unacceptable |
| Bake the data into the policy bundle and rebuild it periodically | decisions are made on data that is minutes or hours stale |

OPAL is the third option. It is a **pub/sub layer** for OPA's inputs:

| Component | Job |
|---|---|
| **OPAL Server** | watches a Git repository for policy changes, and subscribes to data sources; publishes updates over a websocket topic |
| **OPAL Client** | runs beside each OPA instance, subscribes to topics, fetches the changed data and writes it into OPA's document store |

The result: a policy change committed to Git, or a row changing in a database, propagates to every
OPA in the fleet within seconds — and evaluation stays a local, in-memory operation with no network
call.

Data sources are pluggable via "fetch providers": HTTP APIs, PostgreSQL, MongoDB, S3. A common
pattern is subscribing to a database's change stream so the authorisation data mirrors the
application's own state.

**This is not an admission controller.** It sits at a different layer from the other three tools in
this folder: [Gatekeeper](../gatekeeper/README.md), [Kyverno](../kyverno/README.md) and
[Kubewarden](../kubewarden/README.md) enforce; OPAL feeds. Its natural pairing is with OPA used for
**application** authorisation — "may this user view this document" — where the answer depends on
data that changes constantly.

## When to use it

- **A policy decision depends on state outside the cluster.** Is this image approved in the CMDB, is
  this team over budget, is this user in the on-call rotation, is this tenant's subscription active.
  Rego can express the rule; OPAL supplies the fact.
- **OPA is used for application authorisation.** This is the mainstream use case and the one the
  project is built around: many OPA sidecars across many services, all needing the same
  user/role/permission data, all needing it fresh.
- **The data changes faster than a bundle rebuild.** Bundle polling gives you minute-scale
  staleness. If a revoked permission must take effect now, polling is the wrong mechanism.
- **You want GitOps for Rego specifically.** OPAL Server watching a policy repository gives OPA the
  same delivery model Flux gives Kubernetes, without packaging bundles by hand.
- **Many OPA instances need the same data.** One server fanning out to N clients beats N clients
  polling the same source.

## When not to use it

- **You want to enforce Kubernetes admission policy.** That is Gatekeeper, Kyverno or Kubewarden.
  OPAL adds nothing on its own — with no OPA to feed, it is a service with no consumer.
- **Gatekeeper already covers the data problem.** Gatekeeper can replicate selected *cluster*
  resources into OPA's cache via its `Config`/`syncSet`, and its external data providers can call
  out for the rest. For policies whose data lives inside the cluster, that is simpler and involves
  one system fewer.
- **The data is static.** If the allow-list changes twice a year, put it in the policy or in a
  ConfigMap and stop.
- **You are not running OPA.** OPAL exists to serve OPA (and Cedar, in newer versions). It has no
  standalone value.
- **You are not ready for another stateful component on the decision path.** OPAL Server is a
  service with websocket connections to every client, plus a broadcast channel (Redis, Postgres or
  Kafka) when the server itself is replicated. That is real infrastructure, and if it stops
  publishing, every OPA carries on happily with **stale data and no error** — decisions keep being
  made, just on old facts. Silent staleness is the failure mode to monitor for.

## Notes

The original `doc.md` contained only the two repository links, which are at the top of this file.
What follows is the state of the deployment in this folder, and how it relates to the rest.

### How it is deployed here

`helm/helmrelease.yaml` installs chart `opal` 0.0.28 from the `permitio` HelmRepository into the
`opal` namespace, with **no values at all** — only a comment pointing at the chart's
`values.yaml`. There is no OPA in this repo for it to feed, no policy repository configured, and no
data source.

The chart version is worth noticing: `0.0.28` is the chart's own version, not OPAL's, and a `0.0.x`
chart is a signal to read it before trusting it in anything that matters.

This is an evaluation stub. Reading it that way is correct — OPAL is in this folder to document a
category, not because it is in the delivery path.

### Why it sits in `policies/` at all

It is the odd one out and it belongs here for one reason: it is part of the OPA ecosystem, and
[Gatekeeper](../gatekeeper/README.md) — which is also OPA — is next door. If the platform ever
committed to OPA as its policy language for both Kubernetes admission *and* application
authorisation, OPAL is the piece that makes the second half practical.

That is the honest framing of when it would earn its place here: not as a fourth admission engine,
but as the thing that would let a single Rego codebase serve both the cluster and the applications
running on it.

### What to check before adopting it

- Which OPA is being fed, and where it sits — sidecar, service, or Gatekeeper.
- Which data source, and whether the fetch provider for it exists or must be written.
- Whether OPAL Server is single-replica (then it is a single point of freshness) or replicated
  (then it needs a broadcast channel: Redis, Postgres or Kafka).
- How you will detect that data has gone stale — the failure is silent by design.
- Whether the same result is achievable with Gatekeeper's resource replication, which requires no
  new component.

---

[← Admission policies](../README.md)
