[← Flux UIs](../README.md)

# Weave GitOps

<https://github.com/weaveworks/weave-gitops>

---

## The problem it solves

Weave GitOps is the dashboard built by Weaveworks — the company that created Flux and coined the term
GitOps. It is the more product-shaped of the two options here: as well as rendering Flux objects, it
has its own user model (a local admin account or **OIDC**), a resource-detail view with dependency
graphs, and support for surfacing custom metadata from annotations so a team's own links and owner
information appear beside each application.

That last feature is the one that distinguishes it from a plain viewer. A `Kustomization` annotated
with a runbook URL and an owning team shows those in the UI, which turns the dashboard into
something a developer can be pointed at rather than a status page a platform engineer reads.

## When to use it

- developers need Flux visibility **without kubeconfigs**, and there is an identity provider to
  authenticate them against
- per-application ownership, documentation links or runbooks should appear alongside reconciliation
  state
- the platform wants a single URL to hand to teams rather than a CLI onboarding exercise

## When not to use it

- **the maintenance question is unresolved.** Weaveworks ceased operations in 2024. Adopting a
  cluster-privileged web application whose vendor no longer exists is a decision to make with open
  eyes; check the repository's current activity before committing to it
- the only users are platform engineers with cluster access — see [`flux-ui/`](../README.md)
- it will be reached by port-forward, which defeats the purpose
- you want something minimal; this is heavier than [Capacitor](../capacitor/README.md) in every
  dimension

## Notes

### Recorded issues

- <https://github.com/weaveworks/weave-gitops/issues/3702>
- <https://github.com/weaveworks/weave-gitops/issues/3485>

Two issue links kept without commentary. They were recorded during evaluation, which places them as
things encountered rather than things read about — but the note does not say what they were, and
inventing detail would be worse than leaving the gap. Read them before deploying; given the vendor's
status, assume open issues stay open.

### Guides that were followed

- <https://gitops.weave.works/docs/guides/displaying-custom-metadata/> — how annotations on Flux
  objects become fields in the UI. This is the feature that makes the dashboard worth more than
  `flux get all`, because it shows information that exists nowhere in the CRD status: who owns this,
  where the runbook is, which ticket introduced it.
- <https://gitops.weave.works/docs/guides/oidc/> — configuring OIDC instead of the local admin
  account. This is the setting that makes the deployment defensible: it is what turns "a dashboard
  behind a port-forward" into "a dashboard developers can actually reach", and it replaces the
  shared admin password.
- <https://developers.google.com/identity/openid-connect/openid-connect> — Google's OIDC
  documentation, recorded alongside the guide above, so the intended identity provider was Google.
  Useful for the concrete values: issuer URL, the client ID and secret, and which scopes have to be
  requested for the claims Weave GitOps maps to users and groups.

The presence of both OIDC links and the absence of any OIDC configuration in the checked-in values
tells the story: the right approach was researched and the deployment stopped at the admin account.

### What is checked in, and the credential in it

An `OCIRepository` at `oci://ghcr.io/weaveworks/charts/weave-gitops` pinned to **4.0.36**, and a
`HelmRelease` consuming it with two values set:

- `metrics.enabled: true`
- `adminUser` — created, username `admin`, with a **bcrypt hash committed in the values**, and a
  comment recording that the plaintext password is `pikakube` and that new hashes can be generated at
  `https://bcrypt.online`

That hash is a credential in Git, and the comment beside it removes even the small protection bcrypt
would have offered. For a lab cluster with no ingress it is a deliberate convenience, and it should
not survive contact with anything real. Two ways out, in order of preference:

1. **OIDC**, per the guide above — no local account, no shared password.
2. `valuesFrom` a `Secret` — the hash leaves Git and the `HelmRelease` references it, which is the
   Flux capability described in [`flux/`](../../README.md) and one of the recorded reasons for
   preferring Flux to Argo CD.

`metrics.enabled: true` is the better-aged decision here: it exposes Prometheus metrics from the
dashboard itself, which is consistent with the `serviceMonitor` intent recorded in
[`flux-operator/`](../../flux-operator/README.md) — also not yet enabled.

---

[← Flux UIs](../README.md)
