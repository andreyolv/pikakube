[← Identity providers](../README.md)

# Keycloak

<https://github.com/keycloak/keycloak>
<https://github.com/codecentric/helm-charts>

---

## The problem it solves

Keycloak is the heavyweight default: Red Hat's open-source identity provider, Java, and by a
wide margin the largest installed base of any open-source IdP. If a tool documents "how to
configure SSO", the example is Keycloak.

What you get for that weight is genuinely complete coverage:

| Capability | Detail |
|---|---|
| **Protocols** | OIDC, OAuth2 and **SAML 2.0** as a first-class identity provider, not an afterthought |
| **User federation** | LDAP and Active Directory, with Kerberos/SPNEGO desktop SSO. Users can stay in the directory rather than being copied |
| **Identity brokering** | upstream social and enterprise IdPs — GitHub, Google, Microsoft, any OIDC or SAML provider |
| **Authentication flows** | a builder for multi-step journeys: conditional MFA, step-up authentication, custom execution order, scripted authenticators |
| **Realms** | isolated tenants, each with its own users, clients, keys and policy |
| **Authorization services** | fine-grained, per-resource permission evaluation (UMA 2.0) — an authorization engine bundled inside the IdP |
| **Admin REST API** | everything the console does is scriptable |

The two features that most often decide the choice are **SAML** and **LDAP/Kerberos
federation**. Nothing else in [`../README.md`](../README.md) matches Keycloak's maturity in
either, and both are common hard requirements in an enterprise.

The realm model is worth understanding early because it shapes everything: a realm is a
complete, isolated identity universe with its own signing keys and its own issuer URL. The
`master` realm exists only to administer the others, and putting application users in it is one
of the classic mistakes.

## When to use it

- **SAML is required.** Enterprise SaaS "SSO" tiers frequently mean SAML, and Keycloak is the
  mature open-source answer.
- **LDAP or Active Directory is the source of truth** and you need Kerberos desktop SSO or
  attribute mapping from the directory.
- **You need real multi-step authentication flows** — step-up authentication for admin actions,
  conditional MFA by group or by client, custom execution order.
- **You need commercial support.** Red Hat build of Keycloak is a supported product, which is
  sometimes the actual requirement.
- **Ecosystem matters most.** Every integration guide, every Stack Overflow answer, every
  operator's documentation already assumes Keycloak. That reduces the cost of every subsequent
  integration.

## When not to use it

- **A source of truth already exists and you only want to broker it.** Running a JVM and a
  database to federate GitHub is a very poor trade against
  [Dex](../../federation/dex/README.md).
- **You cannot carry the operational weight.** It needs a real database, JVM memory tuning,
  Infinispan cache configuration for clustering, and upgrade planning. On a single-node cluster
  it is a single point of failure for all authentication.
- **You want configuration as code without pain.** The realm JSON import/export is verbose,
  order-sensitive and awkward to diff. It works; it is not pleasant. Authentik's blueprints and
  Zitadel's API are nicer.
- **You need an ingress-level auth proxy too.** Keycloak does not do forward-auth;
  [Authentik](../authentik/README.md) does, in the same component.
- **Small internal tooling only.** [Casdoor](../casdoor/README.md) or Authelia gets there with a
  fraction of the machinery.

Two operational realities to plan for:

- **Upgrades touch the user database.** Schema migrations run on startup. Take a backup first,
  every time, and read the migration notes — Keycloak has historically made breaking changes
  between major versions, including the Quarkus rewrite that changed startup, configuration and
  the URL layout.
- **The `/auth` path prefix is version-dependent.** Older Keycloak served everything under
  `/auth`; the Quarkus versions dropped it by default. Every stale tutorial on the internet
  assumes the old layout, and this is the most common source of "the URL 404s" confusion.

## Notes

The recorded notes are preserved below in full, translated where they were in Portuguese, with
an explanation of what each one means.

### On packaging — a genuine, unresolved problem

**`https://github.com/keycloak/keycloak`** — the project.

**`https://github.com/codecentric/helm-charts`** and
**`https://artifacthub.io/packages/helm/codecentric/keycloakx`** — a **third-party** Helm chart
(`keycloakx`) maintained by codecentric, not by the Keycloak project.

The author's note, verbatim and then translated:

> *"not helm chart official, só bosta de OLM"*
> — "there is no official Helm chart, only OLM rubbish."

> *"na doc cita operator, mas fezes puríssima, impossível achar código fonte no github do
> operator"*
> — "the documentation mentions an operator, but it is pure garbage — impossible to find the
> operator's source code on GitHub."

Stripped of the profanity, this is an accurate and still-relevant complaint:

- **Keycloak ships no official Helm chart.** The project's supported Kubernetes path is the
  **Keycloak Operator**, distributed through OLM (Operator Lifecycle Manager). Every Helm chart
  in circulation — codecentric's `keycloakx`, bitnami's — is third-party, which means it lags
  releases and can be abandoned. codecentric's chart is the most widely used of them.
- **OLM is a poor fit for a Flux-based GitOps repository.** It introduces a second, parallel
  package manager with its own `Subscription` and `InstallPlan` resources and its own upgrade
  semantics — which is exactly why an operator-only distribution is an obstacle here rather
  than a convenience.
- **The operator's source is hard to locate** because it lives inside the main `keycloak/keycloak`
  monorepo under `operator/` rather than in a separate repository, while the OLM bundles are
  published elsewhere. The frustration recorded is a real discoverability failure.

The two issues recorded are the evidence:

- **`https://github.com/keycloak/keycloak/issues/37636`**
- **`https://github.com/keycloak/keycloak/issues/16210`**

Both are upstream issues about the Kubernetes distribution story. Keeping them here matters
because this is a live constraint on choosing Keycloak in a GitOps repository, not a matter of
taste: you either adopt OLM, or you depend on a third-party chart, and there is no third option.

### What is staged

A Flux `OCIRepository` pointing at `oci://ghcr.io/codecentric/helm-charts/keycloakx`, pinned to
tag `7.2.2` **and** a digest — the correct way to pin, since a tag alone is mutable. Plus a
`HelmRelease` in the `keycloak` namespace, and a `postgres/` subfolder.

Notable choices in the values:

| Setting | What it means |
|---|---|
| `command: kc.sh start --http-port=8080 --hostname-strict=false` | production mode (`start`, not `start-dev`). `--hostname-strict=false` relaxes the hostname check, which is what makes it work behind an ingress or a port-forward without a fully configured public URL — convenient for a lab, and something to tighten in production |
| `--spi-events-listener-jboss-logging-success-level=info` | successful authentication events are logged at `info` rather than being effectively invisible. This is the accounting half of AAA, and turning it on deliberately is the right instinct |
| `JAVA_OPTS_APPEND: -XX:MaxRAMPercentage=50.0` | the JVM sizes its heap from the container limit instead of the host's memory. Without this, Keycloak in a container is a reliable OOMKill |
| `-Djgroups.dns.query=<fullname>-headless` | JGroups clustering via DNS discovery against the headless Service — how replicas find each other to share the Infinispan session cache |
| `KC_DB_*` from the `postgres-app` Secret | database connection details injected from CloudNativePG's generated Secret rather than hardcoded. This is the good pattern, and it is the one the other identity providers in this folder do not follow |
| `dbchecker` with `#enabled: true` **commented out** | the init container that waits for the database is disabled. Keycloak will start before Postgres is ready and crash-loop until it is — survivable, but noisy, and the fix is one uncommented line |
| `secrets.admin-creds` with `user: admin`, `password: secret` | **the bootstrap admin credentials, in plain text in the manifest.** These are chart placeholders and must be replaced by an ExternalSecret or a generated Secret before this is applied anywhere reachable |
| `serviceMonitor.enabled` and `prometheusRule.enabled` | Prometheus Operator scraping and alerting rules, so the platform's existing monitoring covers it |

The `postgres/` subfolder holds a CloudNativePG `Cluster` plus an `ExternalSecret` and a
password Secret — consistent with how the rest of the platform runs Postgres, and a better
choice than the plain Deployment used by Dex and Zitadel.

### The recorded tutorial

A `tutorial/` subfolder holds screenshots, a `realm-export.json`, and a set of working notes
from a real integration exercise. Translated and explained:

**Port-forward to reach the admin console:**

```bash
kubectl port-forward svc/keycloak-http 8080:80
```

**Create a realm** — through the UI, named `Analytics`. Application users and clients belong in
a dedicated realm; the `master` realm is for administering Keycloak itself.

**Configure GitHub as an identity provider**, following
`https://www.keycloak.org/docs/latest/server_admin/#_github`. The recorded procedure:

1. In Keycloak, open *Identity Providers* → *GitHub*, and copy the Redirect URL it displays.
2. At `https://github.com/settings/developers`, register an OAuth App with:
   - Application name: `keycloak-integration`
   - Homepage URL: `http://127.0.0.1:8080/auth/realms/Analytics`
   - Authorization callback URL:
     `http://127.0.0.1:8080/auth/realms/Analytics/broker/github/endpoint` — this must be the
     Redirect URL copied from Keycloak, pasted exactly
3. Copy the Client ID and Client Secret from GitHub into Keycloak.

The note recorded a literal Client ID and Client Secret from that exercise. **They are not
reproduced here.** They are real GitHub OAuth App credentials that were committed to this
repository, which means they must be treated as compromised: delete the OAuth App at
`https://github.com/settings/developers` if it still exists. The same applies to the MinIO
client secret in the command below.

Note the `/auth/` prefix throughout those URLs — that is the pre-Quarkus layout. On a current
Keycloak the equivalent paths have no `/auth` segment, which is the version trap described
above.

**Test the admin console:** `http://127.0.0.1:8080/auth/admin/Analytics/console/`

**Issue a token for MinIO**, following
`https://min.io/docs/minio/kubernetes/gke/operations/external-iam/configure-keycloak-identity-management.html`
— MinIO's documentation for using Keycloak as an external IAM provider, so that MinIO console
and S3 access are governed by Keycloak identities rather than static access keys:

```bash
curl -d "client_id=minio" \
     -d "client_secret=<redacted — rotate it>" \
     -d "grant_type=password" \
     -d "username=<user>" \
     -d "password=<password>" \
     http://127.0.0.1:8080/auth/realms/Analytics/protocol/openid-connect/token
```

Worth naming what this command is: the **resource owner password credentials grant**. It sends
the user's password directly to the token endpoint, which bypasses the browser, bypasses MFA
and bypasses any authentication flow configured in the realm. It is deprecated in OAuth 2.1 and
should not be used outside a debugging session — which is exactly what this was. For a real
integration MinIO uses the authorization-code flow through the browser.

The `realm-export.json` in the same folder is the realm's exported configuration, which is
Keycloak's configuration-as-code mechanism referred to in [`../README.md`](../README.md) — it
can be re-imported to recreate the realm, clients and identity provider without repeating the
UI steps.

---

[← Identity providers](../README.md)
