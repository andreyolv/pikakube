[← Auth proxy](../README.md)

# Authelia

<https://github.com/authelia/authelia>
<https://github.com/authelia/chartrepo>

---

## The problem it solves

oauth2-proxy answers "is there a valid session?" and very little else. Authelia answers a
larger question: **"is this subject, on this network, allowed to reach this path — and have
they proved it with a second factor?"**

It is an authentication *portal*, not just a session holder. Three things distinguish it:

- **It can be the user database.** A YAML file of users and groups, or LDAP. That means SSO
  in front of a handful of internal tools with no identity provider deployed at all — the
  smallest complete setup in this folder.
- **It does multi-factor.** TOTP, WebAuthn/FIDO2 hardware keys, and mobile push. Neither
  oauth2-proxy nor Oathkeeper does any of this; they inherit whatever the upstream IdP
  enforces.
- **It has a real rules engine.** Per-domain and per-path policies with four outcomes —
  `bypass`, `one_factor`, `two_factor`, `deny` — matched on domain, path regex, subject
  (user or group) and client network.

That last point is what people actually deploy it for. `bypass` for `/api/health`,
`one_factor` for the read-only UI, `two_factor` for `/admin`, all expressed in one place and
enforced at the ingress. Expressing that with oauth2-proxy means several proxy instances.

It works as a forward-auth service on every mainstream ingress — nginx, Traefik, Caddy,
HAProxy, Envoy — through the same `auth-url` / `auth-signin` mechanism described in
[../README.md](../README.md).

## When to use it

- **You need 2FA in front of internal tools and do not want to run a full IdP.** This is the
  strongest case. Authelia gives you TOTP or WebAuthn with a file backend and no Keycloak.
- **Per-path authorization policy matters.** Different rules for `/admin` and `/`, or rules
  that depend on the client's source network — "no second factor required from the office
  range" is a policy Authelia expresses directly.
- **A homelab or small platform.** It is the standard answer in that space for good reason:
  one binary, a config file, and every dashboard behind a single login portal.
- **You want a real login portal**, with password reset, session management and a consistent
  UI, rather than a bare redirect to an IdP.
- **You already have LDAP** and want it in front of web applications without deploying a
  brokering layer.

## When not to use it

- **You already run an identity provider that does MFA.** Keycloak, Entra ID, Okta and Google
  all enforce MFA at the IdP. Adding Authelia in front means two policy engines and two places
  to look when access is denied. oauth2-proxy is the right proxy in that situation — thinner,
  and it does not duplicate anything.
- **You want Authelia to *be* your organisation's identity provider.** It has an OpenID
  Connect provider, but it is not a general-purpose IdP: no user provisioning API, no SCIM, no
  federation of multiple upstream sources, no realm model. That is
  [`identity-provider/`](../../identity-provider/README.md).
- **The file backend at any real scale.** Users in a YAML file means user management by pull
  request, no self-service, and no integration with joiner/mover/leaver processes. It is fine
  for a handful of engineers and wrong for an organisation.
- **You are protecting APIs, not browsers.** The portal, the session cookie and the redirect
  flow are all browser assumptions. Machine clients want [Oathkeeper](../oathkeeper/README.md)
  or direct token validation.
- **Non-HTTP protocols.** Same limit as every auth proxy — see
  [`privileged-access/`](../../privileged-access/README.md).

Two operational notes worth knowing before committing:

- **Sessions need Redis for more than one replica.** The default file/memory session store
  does not survive a restart and is not shared between pods. A single-replica Authelia is a
  single point of failure for every application behind it.
- **The configuration is one large YAML document** and it is validated strictly. That is a
  feature at review time and an annoyance at 2am.

## Notes

The recorded notes were bare links; everything below explains what they are and what the
staged manifests in this folder actually say.

**`https://github.com/authelia/authelia`** — the project itself. Written in Go, and the
single-binary design is why it is viable in a small cluster.

**`https://github.com/authelia/chartrepo`** — the official Helm chart repository. Worth
knowing that it is distributed as an **OCI artifact** (`oci://ghcr.io/authelia/chartrepo/authelia`)
rather than a classic Helm repository, which is why the staged manifests use Flux's
`OCIRepository` source rather than a `HelmRepository`. The `OCIRepository` here pins both a
tag and a digest, which is the correct way to do it — a tag alone is mutable.

What the staged HelmRelease configures, and what each choice means:

| Setting | What it means |
|---|---|
| `authentication_backend.file.enabled` | users live in a YAML file inside the pod, not in LDAP or an IdP. Fine for a handful of accounts; see the caveat above |
| `storage.local.enabled` | SQLite on local storage. Holds TOTP secrets, WebAuthn devices and identity-verification state — **losing it means every enrolled second factor is gone**. Not survivable across pod rescheduling without a PVC |
| `notifier.filesystem.enabled` | password-reset and enrolment emails are written to a file instead of being sent. This is the development notifier; the file has to be read out of the pod by hand |
| `session.cookies[].domain: foobar.nip.io` with `subdomain: auth` | the session cookie is scoped to a domain, and the portal lives at `auth.<domain>`. `foobar.nip.io` is a placeholder — the real deployment would use the cluster's `nip.io` hostname. Note the blast-radius point from [../README.md](../README.md): one cookie domain means one session across every application under it |
| `pod.kind: Deployment` | not a StatefulSet — consistent with local storage being disposable, and inconsistent with keeping TOTP enrolments |
| `telemetry.metrics.serviceMonitor.enabled` | Prometheus scraping via the Prometheus Operator, so the platform's existing monitoring picks it up with no extra work |

**The `ingress` block carries an explicit `#... completar com o restante` comment** —
Portuguese for *"complete with the rest"*. It is an unfinished note from the author: the
ingress section is a stub, and the manifest as staged would not produce a working ingress.
This is the honest status of the folder — a starting point, not a deployment.

---

[← Auth proxy](../README.md)
