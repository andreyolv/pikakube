[← Dashboard ingress](../README.md)

# Homepage

<https://github.com/gethomepage/homepage>

---

## The problem it solves

Homepage takes the opposite approach to the discovery-based tools here: the page is **declared** in
YAML rather than derived from the cluster. You write the groups, the services and the links.

In exchange you get things discovery cannot give you: **widgets**. A service entry can carry an API
key and render live data — queue depth, disk usage, download progress, container counts — and health
indicators showing whether each link is actually up. It is closer to a status board than to a
bookmark list.

It can also read from the cluster (`mode: cluster`) to pull in Ingress-annotated services, so the two
models can be mixed.

## When to use it

- You want a curated page with sections, ordering and presentation under your control
- Widgets showing live state from the linked services are the actual goal
- The set of services is stable enough that a config file will not rot
- Bookmarks and a search box belong on the same page as the services

## When not to use it

- The service list changes often — a declared file goes stale and nothing warns you
- You want zero maintenance; that is [Forecastle](../forecastle/README.md) or [Hajimari](../hajimari/README.md)
- Widgets require API keys, and every key in that ConfigMap is a credential in plain text
- Public exposure — it has no authentication of its own

## Notes

**Deployed as plain manifests, not Helm** — `namespace.yaml`, `configmap.yaml`, `deployment.yaml`,
`service.yaml`, `ingress.yaml` and `rbac.yaml`. It is the only tool in this folder without a chart,
which suits a tool whose entire configuration is one ConfigMap anyway.

The ConfigMap carries Homepage's full file set as keys: `settings.yaml`, `services.yaml`,
`bookmarks.yaml`, `widgets.yaml`, `kubernetes.yaml`, `docker.yaml`, `custom.css`, `custom.js`. That
mapping is how Homepage is meant to be run in Kubernetes — the container expects those files, and a
ConfigMap is the natural way to supply them.

What is configured:

- `settings.yaml` — title "PikaKube Platform", the placeholder description, a yellow colour scheme
  and an Unsplash background image
- `kubernetes.yaml` — `mode: cluster`, which is what enables reading Ingress-annotated services from
  the whole cluster rather than only from the local Docker socket
- `widgets.yaml` — a Google search box
- `bookmarks.yaml` — one entry, GitHub
- `services.yaml` — **"My First Group" / "My Second Group" / "My Third Group"**, all pointing at
  `http://localhost/`

Those three service groups are the upstream example content, unedited. Read together with the
branded title, the picture is exact: the deployment works, the page renders, and nothing real has
been put on it.

**`mode: cluster` needs RBAC**, which is what `rbac.yaml` is for. It grants read access to Ingress
objects and related resources cluster-wide. Worth reading before applying, because it is broader than
the Deployment's appearance suggests — a link page with cluster-wide read of ingress configuration.

Also present in the notes for
[`local/linux/onpremise/`](../../../local/linux/onpremise/README.md), under Dashboard, where it is
listed as the homelab option. Same tool, two contexts — and the reason it appears twice is that a
declared page suits a homelab, where the service list is small and rarely changes, far better than it
suits a platform.

---

[← Dashboard ingress](../README.md)
