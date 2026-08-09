[← OAuth2 and OIDC server](../README.md)

# Ory Hydra

<https://github.com/ory/hydra>
<https://github.com/ory/k8s>

---

## The problem it solves

Hydra is a certified OAuth2 and OpenID Connect **authorization server** — and it is defined
much more by what it refuses to do than by what it does.

> **Hydra does not manage users.** No user table, no passwords, no login page, no registration,
> no password reset, no MFA. By design, permanently.

When a client begins an authorization flow, Hydra generates a **login challenge** and redirects
the browser to a URL you configured. Your application authenticates the user however it likes,
then calls Hydra's admin API to *accept* the challenge, saying "this is subject `alice`". Hydra
then does the same for **consent**, and only afterwards issues tokens.

```
client ──► Hydra /oauth2/auth
              │  redirect with ?login_challenge=…
              ▼
        YOUR login app  ── authenticate however you like ──┐
              │  PUT /admin/oauth2/auth/requests/login/accept
              ▼                                            │
        Hydra ──► redirect with ?consent_challenge=…       │
              ▼                                            │
        YOUR consent app                                   │
              │  PUT /admin/oauth2/auth/requests/consent/accept
              ▼
        Hydra ──► authorization code ──► tokens ───────────┘
```

This trips people up constantly, and the reason it is the right design is worth stating:

| Property | Why it follows |
|---|---|
| **Your existing user database stays authoritative** | nothing is migrated, nothing is synchronised, and there is no second copy to diverge |
| **Authentication can be literally anything** | LDAP bind, an upstream IdP, a hardware token, a bank's step-up flow, a legacy system — Hydra never sees it |
| **The hard, specialist part is separated** | OAuth2/OIDC specification compliance is genuinely difficult and worth having a dedicated implementation; user management is your domain and nobody else's |
| **It scales as a stateless service** | tokens can be JWTs or opaque; the only state is in the database |

What Hydra brings on its own terms is real: OpenID Certified, all the current grants
(authorization code with PKCE, client credentials, device code, refresh with rotation), token
introspection and revocation, dynamic client registration, JWT or opaque access tokens, and a
single Go binary with a Postgres or MySQL store.

## When to use it

- **You already have users somewhere and it must stay the source of truth.** This is the case
  Hydra was built for — an existing product with an existing account system that now needs to
  issue OAuth2 tokens to third parties.
- **Third parties call your API on your users' behalf**, and each grant must be individually
  scoped, consented to and revocable.
- **You are running the Ory stack.** Hydra issues tokens, Kratos handles identity and login,
  Keto answers permission questions, and [Oathkeeper](../../auth-proxy/oathkeeper/README.md)
  enforces at the edge. Each is small because the split is intentional.
- **Certification matters.** If an auditor or a partner requires OpenID Certified, that is a
  short list and Hydra is on it.
- **You want the token issuer replaceable independently of authentication**, which is the
  architectural payoff of the separation.

## When not to use it

- **You expected an identity provider.** It is not one and will not become one. If what you
  want is "users, login page, MFA, admin UI", that is
  [`identity-provider/`](../../identity-provider/README.md) — and every option there includes an
  OAuth2 server, so you get Hydra's function as well.
- **You are not prepared to build a login and consent application.** This is the whole cost, and
  it is not small: two web applications handling authentication and consent, calling the admin
  API correctly, and getting session handling, CSRF and challenge validation right. Underestimating
  this is the standard way a Hydra deployment stalls.
- **All your clients are your own applications.** Then there is no third party, no delegated
  access, and no consent to manage — see [`../README.md`](../README.md) §1.
- **You want SSO in front of dashboards.** [`auth-proxy/`](../../auth-proxy/README.md).
- **You want humans on the Kubernetes API.** [`federation/dex`](../../federation/dex/README.md).
  Dex and Hydra are often compared and they solve opposite halves: Dex *consumes* upstream
  identity and issues OIDC tokens for your infrastructure; Hydra *issues* OAuth2 tokens to
  third-party clients and consumes login decisions from you.

## Notes

**`https://github.com/ory/hydra`** — the project. Go, Apache-2.0.

**`https://github.com/ory/k8s`** — the repository holding Ory's Helm charts. The same source is
used by the [Oathkeeper](../../auth-proxy/oathkeeper/README.md) manifests in this folder, which
is why both reference an `ory` `HelmRepository`.

The wider Ory stack, since the split is the main thing to understand about any of these
components:

| Component | Job |
|---|---|
| **Hydra** | OAuth2 / OIDC authorization server — tokens, no users |
| **Kratos** | identity and user management — accounts, login, registration, recovery, MFA. The natural other half of Hydra |
| **Keto** | permissions, Zanzibar-style — the same family as [OpenFGA](../../../authorization/application/openfga/README.md) |
| **Oathkeeper** | identity and access proxy — enforcement at the edge |

What is staged: a `HelmRepository` named `ory` in `flux-system`, a `Namespace` `hydra`, and a
`HelmRelease` at chart version `0.50.6`.

The entire values block is:

```
hydra:
  dev: true
```

Two things to say about that.

**`dev: true` is not a production setting.** It puts Hydra into development mode, which relaxes
security checks — most importantly it permits insecure (non-TLS) transports and loosens
validation that would otherwise reject a misconfigured client. It exists so the server starts
without a full TLS and database setup. It must be off anywhere real, and turning it off is what
surfaces the configuration that has not been done yet: a database (`DSN`), a public URL, a
`SECRETS_SYSTEM` value for encrypting data at rest, and the login and consent URLs.

**The login and consent application is absent.** This is the important observation, and it is
architectural rather than a missing value. Without `urls.login` and `urls.consent` pointing at
an application that accepts challenges through the admin API, Hydra cannot complete a single
authorization flow — a client that starts one gets redirected nowhere. As staged this deploys a
token server that structurally cannot issue a token to a user.

That is not a defect in the manifest so much as a demonstration of the point in §1: choosing
Hydra means committing to building the half it does not ship.

---

[← OAuth2 and OIDC server](../README.md)
