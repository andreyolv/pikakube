[← OAuth2 Proxy](../README.md)

# oauth2-proxy — Helm chart

<https://github.com/oauth2-proxy/oauth2-proxy>
<https://github.com/oauth2-proxy/manifests>

---

## The problem it solves

The same component as [`oauth2-proxy/`](../oauth2-proxy/README.md), deployed the way anything
in this repository should be: a Flux `HelmRelease` against the official chart, in its own
namespace, at a pinned version.

What the chart adds over the hand-written manifests is not features — it is the operational
surface that hand-written manifests always end up needing anyway:

| Chart provides | Why it matters |
|---|---|
| `existingSecret` for client ID, secret and cookie secret | secrets stop being plain `value:` fields in a manifest |
| Ingress template with the right paths | `/oauth2/*` routed to the proxy, which is the step everyone forgets |
| Optional Redis subchart | the session store you need once group lists exceed the 4 KB cookie limit |
| `ServiceMonitor` | Prometheus scraping with no extra objects |
| HPA, PDB, topology spread | it is in the request path of every protected app, so it should not be a single replica |
| `alphaConfig` | the structured configuration format, which is the only way to express multiple upstreams or per-route rules cleanly |

The deployment shape also changes with it. The raw manifests are **in-path** — one proxy per
application. The chart is normally deployed once as a **central forward-auth** service, and
each protected application only gains two ingress annotations:

- `nginx.ingress.kubernetes.io/auth-url` — where the subrequest goes
- `nginx.ingress.kubernetes.io/auth-signin` — where to redirect on `401`

Adding a new protected application then costs two lines on its Ingress and nothing else. That
is the difference that matters at more than one application.

## When to use it

- **Always, for new deployments.** There is no argument for hand-written manifests here.
- **When more than one application needs protecting.** One release, many Ingresses.
- **When the proxy must be highly available.** It is in the path of every protected
  application; a single replica makes it a single point of failure for all of them. The chart
  has the primitives.
- **When secrets must come from a secret store.** `existingSecret` composes directly with
  External Secrets or a sealed-secret mechanism.

## When not to use it

- **When you want to read exactly what is configured.** A chart hides the rendered result
  behind values; for understanding the pattern, the raw manifests are clearer. That is why
  both folders exist.
- **When the ingress controller has no forward-auth support.** Then you are back to the
  in-path shape — which the chart supports through `upstreams`, but the annotation-driven
  simplicity is gone.
- **For a single application you will never grow past.** The raw shape is genuinely smaller.

Two things worth checking before this goes into production, because the chart does not decide
them for you:

- **Session store.** The default cookie store is stateless and fine — until a user's group
  list pushes the cookie past 4 KB. Enable Redis before that happens rather than after.
- **The allow-list.** The chart will happily deploy a proxy that authenticates every account
  at the provider. `--email-domain=*` with no org, team or group restriction is not access
  control.

## Notes

The staged Flux resources in this folder, and what each one says:

| Resource | Content |
|---|---|
| `Namespace` | `oauth2-proxy` — the proxy is a platform component, deployed centrally rather than into an application namespace. This is the deliberate contrast with the raw manifests, which live in `mlflow` |
| `HelmRepository` | the chart source, referenced from `flux-system` |
| `HelmRelease` | chart `oauth2-proxy` version `7.7.12`, five-minute reconcile interval |

The `values` block contains only two reference comments and no configuration:

- `https://artifacthub.io/packages/helm/oauth2-proxy/oauth2-proxy` — the ArtifactHub page,
  which is where the values documentation is rendered
- `https://github.com/oauth2-proxy/manifests/blob/main/helm/oauth2-proxy/values.yaml` — the
  authoritative `values.yaml`. Note the repository: the chart lives in `oauth2-proxy/manifests`,
  **not** in the main `oauth2-proxy/oauth2-proxy` repository, which is a common thing to get
  lost looking for

So as staged this is a placeholder: it pins a version and creates a namespace, and configures
no provider, no client, no cookie secret and no upstream. It would start and do nothing
useful. Filling it in means, at minimum: a provider, an `existingSecret` holding the client ID,
client secret and cookie secret, a redirect URL matching the IdP registration, and an
allow-list that is narrower than "every account at the provider".

The historical configuration to port across is recorded in
[`oauth2-proxy/`](../oauth2-proxy/README.md) — GitHub provider, org `andreyolv`, team
`mlflow` — along with the Entra ID group-claim caveats that apply if the provider changes.

---

[← OAuth2 Proxy](../README.md)
