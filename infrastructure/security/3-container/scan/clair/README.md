[← Image scanning](../README.md)

# Clair

<https://github.com/quay/clair>

---

## The problem it solves

Clair is the original open-source container vulnerability scanner — it predates Trivy and Grype
and was built for a different shape of problem. It is **a service, not a command**.

The model: a registry (or anything else) submits an image manifest to Clair over its API; Clair
indexes the layers into a database, stores the resulting inventory, and answers vulnerability
queries against it. When new vulnerability data arrives, previously indexed images can be
re-evaluated **without re-fetching them**, and the registry is notified about what changed.

| Property | Consequence |
|---|---|
| Persistent index in PostgreSQL | layers are indexed once; images sharing a base share the work |
| Re-evaluation on database update | an image scanned in January is re-assessed automatically when March's CVE lands |
| Notification model | the registry learns that an existing image became vulnerable, rather than someone re-running a scan |
| API-first | designed to be driven by a registry, not by a developer at a terminal |

It is the engine behind **Quay** and **Red Hat Quay** security scanning.

## When to use it

- **You run Quay or Red Hat Quay.** Clair is the built-in scanner; using anything else means
  running a second thing alongside it for no benefit
- **You want registry-side scanning as a service**, with layer-level caching and automatic
  re-evaluation, rather than a scan invoked per build
- **Large registries with heavy layer sharing.** Indexing base layers once and reusing them
  across hundreds of images is a real efficiency argument at that scale
- **You want notifications when an existing image becomes vulnerable** — this is Clair's native
  model, whereas with a CLI scanner you have to build the re-scanning loop yourself

## When not to use it

- **As a CLI in CI.** Clair is a service with a PostgreSQL database. `clairctl` exists, but if
  what you want is "scan this image in a workflow and fail the job", Trivy or Grype is a single
  binary and this is a deployment
- **You do not run Quay.** Harbor embeds Trivy; most other registries have their own. Standing
  up Clair to scan images for a registry that does not integrate with it means writing the
  integration yourself
- **You want IaC, Kubernetes, secret or licence scanning.** Clair does container image
  vulnerabilities and nothing else
- **Small setups.** The operational footprint — indexer, matcher, notifier and a database — is
  disproportionate for a handful of images

## Notes

Original note recorded for this tool:

- <https://github.com/quay/clair> — the upstream project, maintained under the Quay
  organisation (Red Hat). The repository documents the component split (indexer, matcher,
  notifier — which can run combined or separately), the `clairctl` CLI, and the "updaters" that
  pull vulnerability data from the distribution trackers.

Historical note worth carrying: Clair v4 was a substantial rewrite of v2/v3. Documentation and
blog posts found online frequently describe the older architecture, which no longer matches the
current one. Check which major version an article refers to before following it.

---

[← Image scanning](../README.md)
