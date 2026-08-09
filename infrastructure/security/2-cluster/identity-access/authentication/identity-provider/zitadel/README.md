[← Identity providers](../README.md)

# Zitadel

<https://github.com/zitadel/zitadel>
<https://github.com/zitadel/zitadel-charts>

---

## The problem it solves

Zitadel is the architecturally distinctive option in this folder: a single Go binary, and an
**event-sourced** identity provider.

That second property is not a marketing detail, and it changes what the product is good at.
Every change — a user created, a role granted, a password reset, a login succeeded — is stored
as an **immutable event**. Current state is a projection of that event stream rather than the
primary record.

| Consequence | Why it matters |
|---|---|
| **The audit trail is the storage model** | you cannot have state that is not explained by an event. In a conventional IdP the audit log is written alongside the change and can drift, be truncated, or be disabled |
| **Point-in-time reconstruction is inherent** | "what permissions did this user have on that date" is answerable by replaying to a timestamp, not by hoping a log was retained |
| **Tampering is structurally awkward** | altering history means rewriting the event stream, not editing a row |
| **The database is the performance story** | every read is served from projections that must be kept current. Zitadel is opinionated about its database for this reason |

The second distinguishing feature is **multi-tenancy as a first-class concept**. Zitadel has
*Instances*, *Organizations*, *Projects* and *Applications* as a real hierarchy, with users
belonging to organisations and permissions granted per project. Keycloak's realms achieve
isolation, but each realm is a separate universe that must be configured from scratch;
Zitadel's Organizations are designed for the case where creating a new tenant is a routine,
automated, product-level operation.

Add to that: API-first design (everything the console does is a documented gRPC or REST call),
strong passwordless and WebAuthn support, and OIDC/OAuth2 compliance that is taken seriously.

## When to use it

- **Multi-tenancy is a product requirement.** You are building B2B SaaS, "organisation" is a
  domain concept, and tenants must be created programmatically. This is the case Zitadel is
  built for and the clearest reason to choose it.
- **An immutable audit trail is a compliance requirement.** Where "prove what permissions
  existed on this date" must be answerable, event sourcing gives it to you rather than
  requiring log retention discipline.
- **You want API-first, and configuration through Terraform or code** rather than a console.
- **Passwordless matters.** WebAuthn and passkeys are a focus rather than an add-on.
- **You want a single Go binary.** Operationally simpler than a JVM, and simpler than
  Authentik's server + worker + Redis + Postgres.

## When not to use it

- **SAML is central.** Support exists but is not the focus, and the maturity gap against
  [Keycloak](../keycloak/README.md) is real.
- **LDAP or Kerberos federation is required.** Not Zitadel's territory.
- **You want the biggest ecosystem.** Fewer integration guides, fewer people who have hit your
  problem before, fewer examples for any given downstream tool.
- **You are casual about the database.** Event sourcing puts real, sustained load on Postgres,
  and projections must keep up. This is not a component to point at a single unmonitored pod
  with a `ReadWriteOnce` volume.
- **You only need to broker an existing IdP.** [Dex](../../federation/dex/README.md), again.
- **Simple single-tenant internal SSO.** The multi-tenancy that justifies Zitadel is unused, and
  you carry its conceptual weight for nothing.

## Notes

**`https://github.com/zitadel/zitadel`** — the project. Go, Apache-2.0, from a Swiss company of
the same name.

**`https://github.com/zitadel/zitadel-charts`** — the official Helm chart repository, which is
what the staged `HelmRepository` points at.

Worth knowing for context: Zitadel originally required **CockroachDB**, and Postgres support
came later. Older documentation and blog posts still reflect that, which is a source of
confusion when searching. Postgres is now the standard path, and it is what is staged here.

What is staged — a `HelmRelease` at chart version `8.8.1` in the `zitadel` namespace, plus a
`postgres/` subfolder with a plain Deployment, Service, PVC and Secret:

| Setting | What it means |
|---|---|
| `valuesFrom` a Secret named `postgres`, injected at `zitadel.secretConfig.Database.postgres.User.Password` | the database password comes from a Secret rather than the manifest — the same good pattern used by [Dex](../../federation/dex/README.md) |
| `zitadel.masterkey: vZxrx44yXBWOSgvVwzIK58Lg9S5EGAyM` | **the master key, committed in plain text.** This is the key Zitadel uses to encrypt sensitive data at rest — credentials, secrets and keys inside its own store. Anyone with this value and a copy of the database can decrypt all of it. It must come from a Secret. Treat this particular value as burned |
| `ExternalSecure: false` and `TLS.Enabled: false` | Zitadel is told it is *not* behind HTTPS. Necessary to make it start without TLS on a local cluster, and unacceptable anywhere real: tokens and sessions would travel in clear. In production this is `true`, with TLS terminated at the ingress and Zitadel told so |
| `ExternalDomain: 127.0.0.1.sslip.io` | the external hostname. `sslip.io` is a wildcard DNS service — `<anything>.<ip>.sslip.io` resolves to that IP, the same mechanism as the `nip.io` names used elsewhere in this platform. It means no DNS configuration and no `/etc/hosts` editing, and it is the right call for a local cluster |
| `Database.Postgres.Host: postgres.zitadel.svc.cluster.local` | the in-namespace Postgres from the sibling folder |
| `MaxOpenConns: 20`, `MaxIdleConns: 10`, `MaxConnLifetime: 30m`, `MaxConnIdleTime: 5m` | connection pool sizing, tuned explicitly rather than left at defaults — appropriate for an event-sourced system that is continuously reading and projecting |
| `SSL.Mode: disable` for both the `User` and `Admin` database users | unencrypted database connections. Fine within a cluster on a local machine, wrong where the database is remote |
| `replicaCount: 1` | single replica. Consistent with a lab; a single point of failure for all authentication anywhere else |

Note the two database users: Zitadel uses an **admin** user for schema migrations and setup and
a separate **user** for runtime, which is a good separation and one the manifest preserves.

The `postgres/` subfolder is a plain Deployment with a PVC — the same shortcut Dex takes. Given
that the platform runs CloudNativePG, a `Cluster` resource would be more consistent and would
bring backups and failover with it; [Keycloak](../keycloak/README.md) is the folder that gets
this right.

---

[← Identity providers](../README.md)
