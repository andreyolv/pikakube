[← Dashboards](../README.md)

# kubewall

<https://github.com/kubewall/kubewall>

---

## The problem it solves

A single binary that serves a cluster UI. No backend to deploy, no database, no build step — run it
and open a browser, or run it in the cluster if you prefer. It handles **multiple clusters** from one
interface by reading the kubeconfigs you give it.

The pitch is minimalism: everything a general dashboard does — browse resources, view and edit YAML,
read logs, exec — with the smallest possible footprint and no setup.

## When to use it

- You want a UI right now, with no installation ceremony
- Switching between several clusters in one window
- A local tool for an individual engineer rather than a shared service
- Constrained environments where a multi-component dashboard is too much

## When not to use it

- Shared, multi-user access with per-user identity; a single-binary tool is not where that lives
- Where project maturity matters — the version here is `0.0.11`
- If you need CRD-heavy views or plugins; [Headlamp](../headlamp/README.md) is stronger
- Exposed on an Ingress without something authenticating in front of it

## Notes

**Installed from an `OCIRepository`** — `oci://ghcr.io/kubewall/charts/kubewall`, tag `0.0.11`, with
an `ingress.yaml` and `namespace.yaml`. No notes were recorded beyond the project link.

Three observations that follow from those facts.

**The OCI distribution is the modern pattern.** Helm charts pushed to a container registry as OCI
artifacts need no chart repository, no index file and no static hosting. Flux's `OCIRepository`
consumes them directly. This folder contains three distribution mechanisms side by side —
[KubeView](../kubeview/README.md) from Git, most tools from a Helm repository, and this from OCI —
which is an accidental but useful comparison of how charts are shipped in practice.

**Version `0.0.11` is the headline.** Not a criticism, a fact worth stating plainly: this is an early
project. Running it on a laptop against a kubeconfig costs nothing if it breaks. Putting it on an
Ingress in a cluster other people use is a different proposition, and the version number is the
argument.

**It handles multiple clusters from the kubeconfig**, which is the feature that distinguishes it from
the other lightweight options here. That works well as a desktop tool and awkwardly as an in-cluster
deployment, where the kubeconfigs would have to be mounted in — and a Secret containing credentials
for several clusters is a concentrated target.

---

[← Dashboards](../README.md)
