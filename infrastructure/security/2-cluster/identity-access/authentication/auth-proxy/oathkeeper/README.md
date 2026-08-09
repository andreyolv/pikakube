[← Auth proxy](../README.md)

# Ory Oathkeeper

<https://github.com/ory/oathkeeper>

---

## The problem it solves

Oathkeeper is grouped with the auth proxies because it can sit at the same place in the
request path, but it is a different kind of tool and treating it as "oauth2-proxy with more
features" leads straight into frustration.

It is an **identity and access proxy built around access rules**, and its real job is the
three-stage pipeline it runs on every request:

| Stage | What it does | Examples |
|---|---|---|
| **Authenticator** | extracts and verifies a credential, producing a subject | `jwt` (validate against JWKS), `oauth2_introspection`, `cookie_session`, `anonymous`, `noop` |
| **Authorizer** | decides whether that subject may perform this request | `allow`, `deny`, `remote_json` (ask an external service, e.g. Ory Keto or OPA) |
| **Mutator** | rewrites the credential for the upstream service | `id_token` (mint a **fresh signed JWT**), `header`, `cookie`, `hydrator` (enrich from an API) |

The mutator stage is the part with no equivalent in oauth2-proxy, and it is the reason to
choose Oathkeeper. Credential **transformation** means the outside world presents one kind of
token and your internal services receive another — a small, uniform, Oathkeeper-signed JWT.
Internal services then validate one issuer and one key, regardless of whether the caller
arrived with an opaque OAuth2 token, a session cookie, or an API key.

That directly fixes the header-trust problem described in [../README.md](../README.md): the
upstream verifies a **signature** rather than trusting a plaintext header that anything on the
network could have set.

Rules are declarative — a JSON or YAML list matching on URL and method — and
**Oathkeeper Maester** is the companion operator that turns Kubernetes `Rule` custom resources
into that list, so rules live next to the services they protect instead of in one central
file.

## When to use it

- **You are protecting APIs and service-to-service traffic**, not browser sessions. This is
  the case it was designed for.
- **Callers arrive with heterogeneous credentials** — opaque OAuth2 tokens, JWTs from
  different issuers, API keys, session cookies — and you want internal services to see exactly
  one uniform, verifiable identity.
- **You already run the Ory stack.** With [Hydra](../../oauth-oidc-server/hydra/README.md)
  issuing tokens and Keto answering permission questions, Oathkeeper is the enforcement point
  that ties them together. As a standalone piece it is much harder to justify.
- **Authorization decisions must be delegated to an external service.** The `remote_json`
  authorizer calls out per request, which is how you plug in OPA, Keto, or an
  [OpenFGA](../../../authorization/application/openfga/README.md)-style relationship engine.
- **You need per-route policy expressed as Kubernetes resources**, owned by the teams that own
  the services — Maester's `Rule` CRD.

## When not to use it

- **You just want a login in front of a dashboard.** Oathkeeper does not have a login UI, does
  not manage sessions well, and does not run the OIDC authorization-code flow on the user's
  behalf. [oauth2-proxy](../oauth2/README.md) does exactly this and does it in one component.
  Using Oathkeeper here is the classic mistake.
- **You need MFA or a policy engine with a portal.** That is [Authelia](../authelia/README.md).
- **You are not otherwise using Ory.** The concepts (authenticator/authorizer/mutator, the
  rule format, Maester) are a real learning cost, and outside the Ory stack you are paying it
  for capabilities a service mesh or an ingress plugin may already give you.
- **A service mesh already does this.** Istio's `RequestAuthentication` and
  `AuthorizationPolicy` cover JWT validation and per-route authorization at the sidecar, with
  no extra hop. If a mesh is already deployed, adding Oathkeeper duplicates it.
- **Latency is critical and you configured introspection.** The `oauth2_introspection`
  authenticator makes a network call per request and turns the token server into a synchronous
  dependency of everything. Prefer the `jwt` authenticator with local JWKS validation.

## Notes

**`https://github.com/ory/oathkeeper`** — the project. Go, Apache-2.0, part of the Ory stack
alongside Hydra (OAuth2 server), Kratos (identity and user management) and Keto (permissions).
Understanding that split is the key to the whole ecosystem: Ory deliberately ships four small
servers instead of one Keycloak, and each is useless-looking in isolation because each is
genuinely only one piece.

The Helm charts referenced by the staged manifests come from `https://github.com/ory/k8s`,
which is the same repository used by [Hydra](../../oauth-oidc-server/hydra/README.md).

Two HelmReleases are staged in this folder, both at chart version `0.47.0` in the `oathkeeper`
namespace, and the pairing is deliberate:

| Release | What it is |
|---|---|
| `oathkeeper` | the proxy itself — runs the authenticator/authorizer/mutator pipeline |
| `oathkeeper-maester` | the controller that watches `Rule` custom resources and compiles them into Oathkeeper's rules file |

Maester is optional in principle. In practice, without it the rules are a single ConfigMap
that every team has to edit, which is precisely the bottleneck the CRD removes.

Both releases have **empty `values`** — only the ArtifactHub and upstream `values.yaml`
reference links are recorded as comments. Nothing is configured: no access rules, no
authenticators, no issuer. As staged this deploys a proxy that has no idea what to protect.

---

[← Auth proxy](../README.md)
