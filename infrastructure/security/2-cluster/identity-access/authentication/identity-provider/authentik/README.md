[← Identity providers](../README.md)

# Authentik

<https://github.com/goauthentik/authentik>
<https://github.com/goauthentik/helm>

---

## The problem it solves

Authentik is the modern alternative to Keycloak: Python and Django, a considerably better
administrative experience, and one architectural idea that sets it apart.

**The flow and stage model.** In most identity providers, an authentication journey is a set of
configuration checkboxes whose interaction you infer. In Authentik it is an explicit object: a
**flow** is an ordered list of **stages** — identification, password, TOTP validation, consent,
user write — with **policies** deciding which stages apply to which users. Login, enrolment,
password recovery and invalidation are all flows, editable in the same way.

The practical result is that "what happens when this user signs in" is something you can read
off a screen rather than reconstruct. For anything beyond a default password login, that is a
large quality-of-life difference.

The second distinguishing feature is directly relevant to this repository:

**Authentik is also an auth proxy.** Its Proxy Provider runs as an outpost — a small deployment
that integrates with ingress-nginx, Traefik and Envoy as a forward-auth endpoint. So the
[`auth-proxy/`](../../auth-proxy/README.md) layer and the identity-provider layer collapse into
one product. Where oauth2-proxy plus Dex is two components, Authentik is one, and the SSO
session is genuinely shared between "log into the IdP" and "reach a protected dashboard".

Beyond that it covers the expected ground: OIDC, OAuth2, SAML, an LDAP outpost for legacy
applications, RADIUS, social and enterprise identity brokering, TOTP, WebAuthn, Duo, and SCIM
provisioning outward to other systems.

## When to use it

- **You want the IdP and the ingress auth proxy to be one component.** This is the strongest
  reason, and it is the one most relevant to a Kubernetes platform.
- **Authentication journeys are non-trivial.** Conditional MFA, enrolment, invitations,
  recovery — the flow model makes these tractable in a way Keycloak's flow builder does not.
- **You want a good admin UI and readable configuration.** Blueprints (YAML) are a nicer
  configuration-as-code story than realm JSON.
- **Homelab through to mid-size platform.** It has become the default recommendation in that
  range, and the ecosystem is growing quickly.
- **You need an LDAP endpoint for old applications** without running a separate directory.

## When not to use it

- **Heavy SAML or Kerberos requirements.** Authentik's SAML works; Keycloak's is more battle-
  tested, and Keycloak's Kerberos/SPNEGO desktop SSO has no equivalent here.
- **You expected it to be lightweight.** It is not. A working deployment is Postgres **and**
  Redis **and** a server deployment **and** a worker deployment, plus outposts for proxy or LDAP
  providers. That is more moving parts than Keycloak's single application plus database.
- **You need long-term stability over features.** The release cadence is fast and the version
  scheme is date-based; upgrades arrive frequently and occasionally require attention. That is
  the cost of the pace.
- **Regulated environments wanting a supportable, long-established product.** Keycloak has a Red
  Hat commercial build; Authentik's commercial offering is younger.
- **You only need to broker an existing IdP.** [Dex](../../federation/dex/README.md) again — no
  user store, no database, one binary.

## Notes

**`https://github.com/goauthentik/authentik`** — the project. The organisation is `goauthentik`
despite the software being Python; the name is not a language indicator.

The Helm chart lives at `https://github.com/goauthentik/helm` and is published as an **OCI
artifact** (`oci://ghcr.io/goauthentik/helm-charts/authentik`), which is why the staged
manifests use a Flux `OCIRepository` rather than a `HelmRepository`.

What is staged, and what to be aware of:

**`OCIRepository`** named `authentik` in the `authentik` namespace, pinned to tag `2026.5.6`
with a digest. The date-based tag is Authentik's versioning scheme — year, month, patch.

**`HelmRelease`** named `authentik` in the `authentik` namespace. And here there is a **real
bug worth recording**:

> The `HelmRelease` references `chartRef: { kind: OCIRepository, name: authelia }` — but the
> `OCIRepository` in this namespace is named **`authentik`**. This is a copy-paste from the
> [Authelia](../../auth-proxy/authelia/README.md) manifests, which use the same
> `OCIRepository` pattern. As written, Flux would fail to resolve the source and the release
> would never reconcile.

That is the kind of defect that only surfaces on the first `flux reconcile`, and it is the main
reason to record it here rather than leave it to be rediscovered.

The values, and what each means:

| Setting | What it means |
|---|---|
| `authentik.secret_key: "PleaseGenerateASecureKey"` | the Django secret key — it signs sessions and tokens. The chart's literal placeholder. **Must** be replaced with a generated value from a Secret; leaving it means anyone who knows the default can forge sessions |
| `authentik.error_reporting.enabled: true` | sends errors to the project's Sentry. A deliberate decision rather than a default — it transmits data outside the cluster, and in most corporate environments the answer is no |
| `authentik.postgresql.password: "ThisIsNotASecurePassword"` | the placeholder again, this time for the database. The chart's own value is honest about what it is |
| `postgresql.enabled: true` with the same placeholder password | the bundled Postgres subchart. Convenient for a demo; for anything real, the platform already runs CloudNativePG, and [Keycloak](../keycloak/README.md) shows the better pattern |
| `server.ingress.enabled: true`, `hosts: [authentik.domain.tld]` | placeholder hostname — would need the cluster's actual `nip.io` name |
| `server.ingress.ingressClassName: "nginx \| traefik \| kong"` | **not a valid value.** This is the chart documentation's list of options pasted in verbatim rather than a choice. It must be a single class name — `nginx`, for this platform |

Two things absent from the staged values that a working deployment needs: **Redis**, which
Authentik requires for its task queue and caching, and the **worker** deployment, which the
chart enables by default but which is worth confirming. Without the worker, background tasks —
including outpost management and email — silently do not run.

Taken together, the staged manifests here are the least finished of the three identity
providers in this folder: a broken chart reference, placeholder secrets, and an invalid ingress
class. They record intent, not a deployment.

---

[← Identity providers](../README.md)
