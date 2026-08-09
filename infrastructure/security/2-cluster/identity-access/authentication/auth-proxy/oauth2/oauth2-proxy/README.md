[← OAuth2 Proxy](../README.md)

# oauth2-proxy — raw manifests

<https://github.com/oauth2-proxy/oauth2-proxy>

---

## The problem it solves

This folder is the **worked example**: oauth2-proxy deployed by hand, in-path, in front of
MLflow, gating on GitHub org and team membership.

MLflow is the archetype for this whole pattern. It exposes a tracking UI, an artifact browser
and a registry over HTTP; the open-source server has no authentication worth the name; and the
moment it is put behind an Ingress it is fully open to anyone who can reach the cluster. The
requirement — "people in my GitHub organisation's `mlflow` team, nobody else" — is not
expressible anywhere in MLflow.

The solution here is the **in-path** shape from [../../README.md](../../README.md): the proxy
is the thing the Ingress routes to, and the proxy forwards upstream to MLflow's Service.
Nothing reaches MLflow that has not already been through GitHub.

| Object | Role |
|---|---|
| `Deployment` `oauth-pusher` | one replica, `quay.io/pusher/oauth2_proxy:v6.1.1`, configured entirely by environment variables, in the `mlflow` namespace |
| `Service` `oauth-pusher` | port `4180`, the port the Ingress targets instead of MLflow's |

The environment variables are the entire configuration, and they read as a complete summary of
the pattern:

| Variable | Value | What it does |
|---|---|---|
| `OAUTH2_PROXY_PROVIDER` | `github` | use GitHub's API rather than generic OIDC |
| `OAUTH2_PROXY_GITHUB_ORG` | `andreyolv` | membership of this organisation is required |
| `OAUTH2_PROXY_GITHUB_TEAM` | `mlflow` | **and** membership of this team — the actual access control |
| `OAUTH2_PROXY_EMAIL_DOMAINS` | `*` | accept any email. Safe **only** because org and team do the gating |
| `OAUTH2_PROXY_UPSTREAMS` | `http://mlflow-server:5000` | in-path: the proxy forwards here after authenticating |
| `OAUTH2_PROXY_HTTP_ADDRESS` | `:4180` | the port the Ingress routes to |
| `OAUTH2_PROXY_REDIRECT_URL` | `https://<ingressurl>/oauth2/callback` | must match the GitHub OAuth App exactly; the placeholder is filled in per environment |
| `OAUTH2_PROXY_COOKIE_SECRET` | *(empty)* | the session encryption key — 16, 24 or 32 bytes |
| `OAUTH2_PROXY_CLIENT_ID` / `_SECRET` | *(empty)* | the GitHub OAuth App credentials |

The three empty values are deliberate: they are the secrets, and they were never committed.
That is the right instinct, and it is also the manifest's main defect — as written they are
plain `value:` fields, so filling them in means putting secrets in the manifest. A
`valueFrom.secretKeyRef` is the fix.

## When to use it

- **As a reference.** If you need to protect one application quickly and want to see every
  moving part in twenty lines, this is it.
- **When the ingress controller cannot do forward-auth.** The in-path shape needs no
  `auth-url` support at all — the proxy is simply the upstream.
- **For a single application** whose access rule is exactly one group. Standing up a central
  forward-auth deployment for one app is more machinery than the problem needs.

## When not to use it

- **As the deployment mechanism for anything new.** Use
  [`oauth2-proxy-chart/`](../oauth2-proxy-chart/README.md) — Flux-managed, current chart,
  current image.
- **The image is obsolete.** `quay.io/pusher/oauth2_proxy:v6.1.1` is from the abandoned Pusher
  fork. It is unmaintained and unpatched, and it sits in the request path. The current images
  are `quay.io/oauth2-proxy/oauth2-proxy`.
- **For more than one application.** N applications means N deployments, N OAuth Apps and N
  redirect URLs. Central forward-auth is one of each.
- **Without a NetworkPolicy.** In-path deployment means MLflow's Service is still directly
  reachable from every pod in the cluster; the proxy only guards the ingress route. Anything
  inside the cluster can bypass it entirely by calling `mlflow-server:5000` directly.

## Notes

The recorded notes for this folder were a set of reference links about Entra ID group
handling, kept in `references.md` alongside these manifests. Preserved and explained:

**`SSO Azure Entra ID Groups - helm chart`** — the heading the author gave the group. It names
the actual problem: not signing in with Entra ID, but getting **groups** out of it in a form
the proxy can filter on.

**`https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/azure/`** — the official
Azure/Entra ID provider documentation. The relevant part is that the provider needs the tenant
ID and the right scopes, and that group information does not simply arrive.

**`https://github.com/oauth2-proxy/oauth2-proxy/issues/2125`** and
**`https://github.com/oauth2-proxy/oauth2-proxy/issues/1363`** — two upstream issues, both
about group claims with Azure/Entra ID. That both recorded issues are about the same thing is
the finding worth keeping: **authenticating against Entra ID is easy; mapping its groups onto
`--allowed-group` is where the work is.** The underlying causes are described in
[../README.md](../README.md) §2 — Entra ID emits group **object IDs** rather than names by
default, and it omits the claim entirely once a user belongs to more groups than the token can
carry, which affects administrators first.

The practical takeaway recorded by those links: decide the group strategy *before* deploying —
restrict the emitted claim to groups actually assigned to the application, or accept matching
on object IDs and document what each one means.

---

[← OAuth2 Proxy](../README.md)
