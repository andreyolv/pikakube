[← Identity providers](../README.md)

# Casdoor

<https://github.com/casdoor/casdoor>

---

## The problem it solves

Casdoor is the lightweight end of this folder: a Go identity provider that stands up quickly,
speaks a surprisingly wide range of protocols, and integrates with a very long list of social
login providers.

Its pitch is coverage per unit of operational weight:

| Capability | Detail |
|---|---|
| **Protocols** | OIDC, OAuth2, SAML, CAS, and it can expose an **LDAP** endpoint |
| **Social providers** | one of the widest lists available — GitHub, Google, and a long tail including Chinese providers (WeChat, DingTalk, Alipay) that other IdPs skip entirely |
| **MFA** | TOTP and WebAuthn |
| **Data model** | Organizations, Applications, Users, Providers — flat and quick to grasp |
| **Storage** | a broad set of backends via its ORM — MySQL, Postgres, SQLite, SQL Server and others |
| **Deployment** | a Go binary plus a database, and nothing else |

The CAS support is worth noting because almost nothing else here has it — it is the protocol
used across a lot of university and public-sector infrastructure, and Casdoor is one of the few
open-source IdPs that speaks it natively.

It also sits inside a family of related projects (Casbin for authorization policy, Casdoor for
identity), which is coherent if you are already using Casbin and largely irrelevant otherwise.

## When to use it

- **You want an IdP with genuinely low operational weight.** No JVM, no Redis, no worker
  deployment — a binary and a database.
- **Social login breadth is the requirement**, particularly for providers outside the Western
  default set.
- **You need CAS**, which is a real requirement in academic and public-sector environments and
  hard to satisfy elsewhere.
- **Internal tooling and small platforms**, where the assurance bar is "these are our
  engineers" rather than "this is regulated".
- **You are already using Casbin** for authorization and want the matching identity component.

## When not to use it

- **Anything high-assurance or regulated.** The community is smaller and there is less
  published security review than for Keycloak. That is not an accusation, it is a statement
  about how much scrutiny each has had — and for a component that authenticates everyone,
  scrutiny is the feature.
- **You need mature SAML or LDAP/Kerberos federation.** [Keycloak](../keycloak/README.md).
- **You need complex authentication journeys.** No equivalent to Keycloak's flow builder or
  [Authentik](../authentik/README.md)'s flow/stage model — conditional MFA and step-up
  authentication are not really expressible.
- **You need real multi-tenancy.** Organizations exist, but they are not
  [Zitadel](../zitadel/README.md)'s first-class model.
- **Documentation quality matters to you.** It is uneven, and parts assume familiarity with the
  project's conventions.
- **You only need to broker an existing IdP.** [Dex](../../federation/dex/README.md) — no user
  store at all.

## Notes

**`https://github.com/casdoor/casdoor`** — the project, and the only note recorded for this
folder.

**No manifests are staged here.** Unlike [Keycloak](../keycloak/README.md),
[Authentik](../authentik/README.md) and [Zitadel](../zitadel/README.md), which each have a
HelmRelease and a Postgres alongside, this folder contained nothing but the link. That is the
accurate status: Casdoor was catalogued as an option and not taken further.

Two things to know if it ever is:

- **The bundled default admin account** (`admin` / `123`) is a well-known default and is exactly
  the kind of credential that gets left in place. Change it as part of the first deployment,
  not afterwards.
- **The official Helm chart is less prominent than the Docker Compose path.** Most of the
  project's documentation assumes Compose, so a Kubernetes deployment involves more
  translation than the equivalent for the other three.

For this platform the recommendation in [`../README.md`](../README.md) applies with full force:
there is no user database to be the source of truth of, so
[Dex](../../federation/dex/README.md) brokering GitHub is a better fit than any identity
provider here — and Casdoor's advantage over the others (low weight) is precisely the advantage
Dex has over Casdoor, by a wider margin.

---

[← Identity providers](../README.md)
