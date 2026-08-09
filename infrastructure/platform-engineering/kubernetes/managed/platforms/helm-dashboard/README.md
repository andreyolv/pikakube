[← Platforms](../README.md)

# Helm Dashboard

<https://github.com/komodorio/helm-dashboard>

---

## The problem it solves

Helm's CLI can tell you what is installed, but answering "what changed between revision 7 and
revision 8, and which manifests does that translate to" means `helm get manifest` twice and a diff.
Helm Dashboard puts that in a UI: installed releases, their revision history, a **diff between
revisions**, the rendered manifests, and one-click rollback.

Unlike [Kubeapps](../kubeapps/README.md), it is not a catalog for installing new things. It is a
window onto releases that already exist, which makes it much smaller and much less invasive.

## When to use it

- Debugging a Helm release: what is actually deployed, and what changed
- Comparing revisions before deciding whether to roll back
- Understanding a cluster you inherited that was installed with Helm
- A lightweight tool run locally rather than a platform component

## When not to use it

- Self-service installation from a catalog — that is Kubeapps
- On a GitOps cluster, if the rollback button will be used; rollbacks are drift
- Where releases are managed by Flux `HelmRelease` objects — see the note below
- As a permanently exposed service; it does not need to be

## Notes

**Chart** `helm-dashboard` version `2.0.3` from `https://helm-charts.komodor.io`, with a namespace
manifest and empty values. Recorded as a link only.

**The Flux interaction is the thing to understand before installing it here.** Flux's Helm controller
does install genuine Helm releases, and their state lives in Secrets exactly as Helm expects — so
Helm Dashboard *will* see releases created by Flux and can show their history and diffs. That is
useful.

What it must not do is act on them. Rolling back a Flux-managed release through the UI changes the
cluster while Git still says something else; the Helm controller reconciles and undoes it, usually
within minutes. The rollback appears to work and then silently reverses, which is a worse experience
than it failing outright.

Used read-only — inspect, diff, understand — it is a genuinely good companion to a Flux setup, and it
answers the question `flux get helmreleases` cannot: what do the rendered manifests actually look
like, and what changed.

**It can run locally** against your kubeconfig as a CLI-launched web UI, which is the lowest-risk way
to use it: no in-cluster deployment, no exposure, no permissions beyond your own. The chart is for
when a team wants it shared.

Komodor maintain it as an open-source companion to their commercial product.

---

[← Platforms](../README.md)
