[← Dashboards](../README.md)

# Skooner

<https://github.com/skooner-k8s/skooner>
<https://github.com/skooner-k8s/skooner/blob/master/kubernetes-skooner.yaml>

---

## The problem it solves

A deliberately simple cluster UI — formerly k8dash — that renders the things you look at most
(nodes, workloads, namespaces, storage) with live-updating charts and no configuration. It supports
OIDC and ServiceAccount tokens, and it installs from a single YAML file.

Its selling point is speed of both kinds: quick to deploy, and quick to read. Where the official
dashboard is several components and a login flow, Skooner is one Deployment and a Service.

## When to use it

- You want a working UI in one `kubectl apply`
- A live at-a-glance view of node and workload health
- Small clusters and homelabs
- A lightweight alternative when the official dashboard's setup is disproportionate

## When not to use it

- CRD-heavy clusters; the resource coverage is narrower than [Headlamp's](../headlamp/README.md)
- Where project activity matters — check the repository before adopting it
- Multi-tenant access with per-user scoping
- As a long-term platform component without confirming it is still maintained

## Notes

**Deployed as plain manifests** — `deployment.yaml` and `service.yaml` — derived from the upstream
single-file install:

- <https://github.com/skooner-k8s/skooner/blob/master/kubernetes-skooner.yaml>

Recording that upstream URL alongside the local copies is the right instinct, and it is the thing
that makes plain-manifest installs maintainable at all: without it, nobody can tell whether the YAML
in the repository is current, modified, or simply old. With it, a diff answers the question.

No further notes were recorded.

Two things to be aware of before it goes anywhere shared:

- **Upstream's single-file manifest includes a `cluster-admin` binding.** That is how it manages to
  be a one-command install. The copy here is split into a Deployment and a Service with no RBAC file,
  so whatever ServiceAccount it runs as needs checking rather than assuming — either it has no
  permissions and shows nothing, or it inherited something broad.
- **The project renamed from k8dash and has been quiet.** Search results and blog posts still use the
  old name. Confirm the repository is active before making it a dependency; a dashboard is an easy
  thing to replace, which is the mitigating factor.

---

[← Dashboards](../README.md)
