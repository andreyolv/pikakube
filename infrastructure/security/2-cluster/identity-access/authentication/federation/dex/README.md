[← Federation](../README.md)

# Dex

<https://github.com/dexidp/dex>
<https://github.com/dexidp/helm-charts>

---

## The problem it solves

The Kubernetes API server authenticates humans in exactly one federated way: **OIDC**. Your
users are in GitHub, or LDAP, or a corporate SAML IdP. None of those is OIDC.

Dex closes that gap and nothing else. It is a **thin identity broker**: it authenticates
against an upstream connector, then issues an OIDC ID token signed by itself.

```
GitHub / LDAP / SAML / Google / Entra ID  ──►  Dex  ──►  OIDC  ──►  kube-apiserver
                                                            └────►  oauth2-proxy, ArgoCD, Grafana
```

What makes it worth choosing is what it refuses to do:

| Dex has | Dex does not have |
|---|---|
| connectors for GitHub, GitLab, LDAP, SAML, OIDC, Google, Microsoft, and more | a user database |
| a standards-correct OIDC provider with discovery and JWKS | a registration or password-reset flow |
| claim and group mapping | MFA of its own |
| a `kubectl`-oriented flow, including a static example client | an admin UI — configuration is a YAML file |
| storage backends: Postgres, MySQL, etcd, Kubernetes CRDs, SQLite, memory | anything resembling a realm model |

It is one small Go binary with a config file. That is the entire product, and for the
Kubernetes-API-authentication problem it is the correct amount of software. Running Keycloak
to do the same job means a JVM, a database, realm configuration and an upgrade treadmill in
exchange for capabilities you are not using.

Its lineage is CoreOS, which is why the Kubernetes integration is unusually direct: the
**Kubernetes CRD storage backend** stores Dex's own state as custom resources, so it can run
with no database at all, and the `example-app` and `static client` conventions exist
specifically for the `kubectl` login flow.

## When to use it

- **Kubernetes API authentication for humans.** This is the canonical use, and the one this
  folder is really about.
- **A source of truth already exists and you must not copy it.** GitHub, LDAP or corporate
  SAML stays authoritative; Dex translates.
- **Registering clients upstream is a ticket.** Register Dex once with the corporate IdP, then
  add downstream clients yourself in a config file.
- **Several upstreams, one issuer.** Employees on SAML and contractors on GitHub, with
  consumers unaware of the difference.
- **You want the issuer to be a replaceable abstraction.** Consumers trust Dex's URL;
  swapping the upstream touches one component.
- **Paired with an auth proxy.** Dex plus [oauth2-proxy](../../auth-proxy/oauth2/README.md) is
  the cheapest complete SSO story on Kubernetes — two small components covering both the API
  and every web dashboard.

## When not to use it

- **You need to own the users.** No local accounts, no registration, no password reset, no
  self-service. That is [`identity-provider/`](../../identity-provider/README.md).
- **You need MFA that the upstream does not provide.** Dex delegates entirely. If GitHub
  enforces 2FA you inherit it; if nothing upstream enforces it, Dex will not add it. Keycloak,
  Authentik and [Authelia](../../auth-proxy/authelia/README.md) all can.
- **You want an admin UI.** Configuration is a file, changed by pull request. That is a feature
  for a platform team and a blocker for a help desk.
- **You need a full OAuth2 authorization server for third-party API clients** — dynamic client
  registration, consent screens, scope management. Dex issues tokens for *your* applications,
  not as a general-purpose authorization server. That is
  [Hydra](../../oauth-oidc-server/hydra/README.md).
- **The upstream already speaks OIDC and you can register clients freely.** Then Dex is an
  extra hop with little benefit — point consumers at the upstream directly.
- **Single replica, in-memory storage, in production.** Dex is on the login path for the whole
  platform. In-memory storage means every restart invalidates every refresh token, and one
  replica means one restart logs everybody out.

## Notes

**`https://github.com/dexidp/dex`** — the project. Go, Apache-2.0, a CNCF sandbox project, and
originally from CoreOS, which explains the depth of the Kubernetes integration.

**`https://github.com/dexidp/helm-charts`** — the official chart repository, which is what the
staged `HelmRepository` points at.

The staged manifests are the most complete design in this folder, and each decision in them is
worth reading:

**`HelmRelease`, chart version `0.19.0`, namespace `dex`.**

| Configuration | What it means |
|---|---|
| `issuer: https://dex.example.com:32000/dex` | the issuer URL. This value is load-bearing: it goes into every token's `iss` claim, it is what the API server is configured to trust, and it must be reachable *and* exactly matching from every consumer. `dex.example.com` is a placeholder — the real deployment needs a resolvable name. The `:32000` port is the convention from Dex's own example app, typically a NodePort |
| `web.https: 0.0.0.0:5556` with `tlsCert` / `tlsKey` from `/etc/dex/tls/` | TLS terminated by Dex itself rather than at an ingress. The API server validates the JWKS endpoint over TLS, so the certificate must be signed by a CA the API server trusts — see [`certificates/README.md`](../../../../certificates/README.md) |
| `storage.type: postgres` | **the right call.** The alternatives are memory (refresh tokens die on restart) and SQLite (single replica only). Postgres allows more than one replica, which matters because Dex is on the login path for everything |
| `valuesFrom` a `Secret` named `postgres`, injected at `config.storage.config.password` | the database password comes from a Secret rather than the manifest. This is the pattern the rest of this folder mostly fails to follow |
| `connectors: [github]`, `orgs: [andreyolv]`, `teams: [admin]` | the upstream. Access requires membership of the `andreyolv` organisation **and** its `admin` team. Team membership becomes the `groups` claim, which is what RBAC binds to |
| `clientID`/`clientSecret` as `$GITHUB_CLIENT_ID` / `$GITHUB_CLIENT_SECRET` | Dex expands environment variables in its config, so the GitHub OAuth App credentials are injected rather than committed. Correct |
| `redirectURI: http://127.0.0.1:5556/dex/callback` | **inconsistent with the issuer above** — plain HTTP on localhost while the issuer is HTTPS on `dex.example.com:32000`. GitHub matches the redirect URI exactly, so this pairing would fail. It is a leftover from local testing, and it is the first thing to fix |

A `postgres/` subfolder alongside it holds a Deployment, Service, PVC and Secret — a plain
single-instance Postgres for Dex's storage. Note that the platform runs CloudNativePG
elsewhere; a `Cluster` resource would be the more consistent choice, as
[Keycloak](../../identity-provider/keycloak/README.md) already does.

**The `example/authconfig.yaml`** is the other half, and the more instructive one. It is an
`AuthenticationConfiguration` (`apiserver.config.k8s.io/v1beta1`) — the structured replacement
for the old `--oidc-*` flags, described in [../README.md](../README.md) §3. It is **not** a
resource you apply to the cluster: it is a file placed on the control-plane node and referenced
by `--authentication-config`. What it says:

| Field | Meaning |
|---|---|
| `issuer.url: https://dex.example.com:32000` | the issuer to trust. Note it lacks the `/dex` path suffix present in the HelmRelease's issuer — these must match exactly, so one of the two is wrong |
| `audiences: [example-app]` | only tokens whose `aud` is `example-app` are accepted. This is the check that stops a token minted for another client being replayed against the API |
| `certificateAuthority` | the PEM CA bundle for validating Dex's TLS. The comment above it, `cat /etc/ssl/certs/openid-ca.pem \| base64 -w0`, records how to produce it; the committed value is placeholder alphabet, not a real certificate |
| `claimMappings.username.claim: email` | the username comes from the email claim. Workable, but `sub` is the safer identifier — emails change and can be reassigned to a different person, and RBAC bindings would silently follow |
| `claimMappings.groups.claim: groups` | GitHub team membership becomes Kubernetes groups. This is what RBAC binds to |
| `userValidationRules` — `!user.username.startsWith('system:')` with the message *"username cannot use reserved system: prefix"* | **the important line.** It blocks an upstream identity from claiming a reserved Kubernetes name. Without it, someone who can control an upstream username or group could assert `system:masters` and become cluster-admin. This is the CEL-based equivalent of setting `--oidc-username-prefix`, and it is the single most valuable line in the file |

Neither the username claim nor the groups claim is prefixed here, which is why that validation
rule is carrying the whole defence. Adding a prefix as well would be belt and braces, and cheap.

---

[← Federation](../README.md)
