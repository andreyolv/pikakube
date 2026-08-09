[← Management interfaces](../README.md)

# CloudBeaver

<https://github.com/dbeaver/cloudbeaver>
<https://github.com/dbeaver/dbeaver>

---

## The problem it solves

The **multi-engine** option: one web interface for PostgreSQL, MySQL, MongoDB, ClickHouse,
Cassandra and a long tail of others — it is the server edition of DBeaver, so it inherits that
driver catalogue.

For a platform with more than one database, that matters more than any individual feature. The
alternative is [pgAdmin](../pgadmin/README.md) *and*
[phpMyAdmin](../phpmyadmin/README.md) *and* [mongo-express](../mongo-express/README.md) — three
tools, three access models, three things to secure.

| Capability | Detail |
|---|---|
| **Many engines** | relational, document, and several analytical stores |
| **A real user model** | users, roles and per-connection permissions |
| Connection management | defined centrally, so credentials are not distributed |
| SQL editor | with completion, history and result export |
| Data editor | grid editing, which should be granted deliberately |
| Schema browser | with ER diagrams |

## When to use it

- **a mixed estate**, which is the main argument
- analysts and engineers need query access **without cluster credentials**
- connections should be managed centrally rather than configured per person
- the user model is the point — see below

## When not to use it

- PostgreSQL only, and administrative depth matters — [pgAdmin](../pgadmin/README.md) does more
- nobody outside the operating team needs to query anything; a CLI and a port-forward is less to
  secure
- **the access question has not been answered** — see
  [`../README.md`](../README.md#deciding-whether-to-deploy-one-at-all)
- the desktop DBeaver would serve the same people equally well

## The user model is why this one is safe to deploy

This is the feature that separates a shared tool from a shared password.

CloudBeaver has its own users and roles, and connections can be granted per role with distinct
database credentials behind them. An analyst gets read access to one database; the credential
itself never leaves the server.

That is what makes the difference between "we deployed a UI" and "we granted controlled access",
and it is the reason [`../README.md`](../README.md) points here for a mixed estate.

## Deploying it properly

The tool is easy and the deployment is the work:

| Concern | What to do |
|---|---|
| **Authentication** | SSO through the cluster's identity, not CloudBeaver's local users — see [`identity-access/`](../../../../security/2-cluster/identity-access/README.md) |
| **Credentials** | a scoped database user per role, **read-only by default** |
| **Which database** | point it at a **replica**; an exploratory query then costs nothing |
| Exposure | internal ingress with authentication in front, never public |
| `NetworkPolicy` | it should reach the databases and very little else |
| Write access | granted deliberately, per role, not by default |
| Audit | who ran what — log it on the database side too |

The replica row is the cheapest safety measure available and the one most often skipped. Analysts
running exploratory queries against the primary is a well-established way to cause an unrelated
outage.

## The editions

CloudBeaver Community is open source and covers the querying and browsing. Some enterprise
features — certain authentication integrations and advanced administration — belong to the
commercial edition.

Worth checking against what is actually needed, particularly if SSO is the deciding requirement.

## Notes

Mapped as the multi-engine option, and the right one for this platform *if* a management UI is
deployed at all — [`databases/`](../../../README.md) covers PostgreSQL, MySQL and MongoDB, which
is exactly the case a single-engine tool does not serve.

Nothing here is currently the access path; database work happens through the CLI against
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md).

The pairing worth remembering from [`../README.md`](../README.md#how-this-applies-to-pikakube):
giving someone a query interface for a schema nobody can explain moves the bottleneck rather than
removing it — see [`documentation/`](../../documentation/README.md).

---

[← Management interfaces](../README.md)
