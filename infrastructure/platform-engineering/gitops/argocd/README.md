[← GitOps](../README.md)

# Argo CD

<https://github.com/argoproj/argo-cd>
<https://github.com/argoproj/argo-helm>

---

## The problem it solves

Argo CD is a reconciliation controller with a **UI at its centre**. It watches a repository, renders
what it finds, diffs it against the cluster and shows you the result as a tree of resources with
health and sync status on each node.

That last part is the product. Flux does the same reconciliation and gives you nothing to look at;
Argo CD gives a developer who has never used `kubectl` a page where they can see that their service
is `Synced` and `Healthy`, and a button that syncs it again. For organisations where the people
deploying are not the people running the cluster, that is worth a lot.

The unit is the `Application` — a repository, a revision, a path, a destination cluster and
namespace, and a sync policy. Everything else, including the app-of-apps pattern
where one `Application` contains a directory of further `Application`s, is built out of that one
object.

## When to use it

- non-platform teams need to **see** deployment state without cluster access or CLI tooling
- the estate is already invested in the Argo ecosystem — Rollouts, Workflows, Events
- multi-cluster from a single control plane, with a UI that shows all of them at once
- a sync-on-demand or manual-approval workflow is genuinely wanted, rather than continuous
  reconciliation
- Argo CD is already running and working; migrating a functioning reconciliation loop is rarely
  justified on architecture alone

## When not to use it

- the deployment model is **Helm-heavy with secrets in values** — this is where the recorded
  experience below is most negative
- a chart source needs to be a first-class, reusable object; there is no `HelmRepository` equivalent
- you want reconciliation to be non-negotiable; `selfHeal` being a per-`Application` flag means it
  can be off somewhere and nobody knows
- installing without Helm matters — Argo CD **core** has no chart, only manifest apply
- fine-grained restriction of which cluster-scoped resources a Project may manage is a requirement;
  `clusterResourceWhitelist` matches on kinds, not names

## Notes

Every note below is from the original file, translated. They were written after running Argo CD, and
the conclusion they add up to is the reason [Flux](../flux/README.md) is what this platform uses.

### The verdict, stated plainly

Four opinions were recorded, and each one is a structural complaint rather than a missing feature:

> **"Argo CD has no `HelmRepository` object like Flux does."**

In Flux, a chart repository is a cluster object with its own interval, credentials and status. Ten
`HelmRelease`s referencing one `HelmRepository` share one source, and you can look at that source
and see whether it is reachable. In Argo CD the repository is server configuration and the chart
reference lives inside each `Application`. The dependency between "where charts come from" and
"what is deployed" exists, but there is no object representing it.

> **"`selfHeal: true` in Argo — seriously?"**

The objection is that self-healing is opt-in per `Application`. Continuous reconciliation is the
fourth GitOps principle; making it a flag means a cluster can contain applications that reconcile
and applications that merely synced once, and telling them apart means reading every `Application`.
The checked-in `app-of-apps/app-of-apps.yaml` sets `prune`, `allowEmpty` and
`selfHeal` all to `true` — which is the correct setting and also demonstrates that all three had to
be asked for.

> **"Flux's component architecture is better — components distributed by function."**

Flux is source-controller, kustomize-controller, helm-controller, notification-controller,
image-reflector-controller and image-automation-controller. Each is a separate deployment with a
separate CRD, can be omitted, scaled or debugged independently, and fails independently. Argo CD is
one system: repo-server, application-controller, API server and UI, coupled by design. The practical
difference shows up when something is slow — with Flux you know which controller, because there is
one per concern.

> **"Passing secrets through Flux's values is better."**

A Flux `HelmRelease` can reference a `Secret` in `valuesFrom`, so a chart value that must not be in
Git simply is not in Git. Argo CD has no equivalent that does not involve a config-management plugin
or a separate templating step. For a platform repository full of charts that need credentials, this
is a daily difference rather than an edge case.

### Recorded issues

> **"No Helm chart for Argo CD core — only a manual apply, which is rubbish, and the community does
> not care."**
> <https://github.com/argoproj/argo-helm/issues/1823>

Argo CD **core** is the reduced installation: controllers only, no API server, no UI, no RBAC —
intended for GitOps without the multi-tenancy layer, which is exactly the shape a platform team
would want. The `argo-cd` chart does not install it, so the only supported path is applying a
manifest by hand. In a GitOps repository, "apply this YAML by hand" is precisely the thing being
eliminated, so a component with no chart is a component that cannot be managed the same way as
everything else. The linked issue is the request for it, and the complaint is that it has sat there.

> **"No limiting `clusterResourceWhitelist` to specific resource names."**
> <https://github.com/argoproj/argo-cd/issues/12208>

An Argo CD `AppProject` restricts which cluster-scoped resources its Applications may manage, but
the whitelist matches on **group and kind**, not on the name of an individual object. Allowing a
tenant to manage one specific `ClusterRole` therefore means allowing them to manage every
`ClusterRole`. For multi-tenant clusters this is the difference between delegating a resource and
delegating a category.

> **"Far too ridiculous."**
> <https://github.com/argoproj/argo-cd/issues/5202>
> <https://github.com/argoproj/argo-cd/issues/7437>

Two further issues filed immediately after the whitelist one and grouped with it under a single
dismissive comment. The note records the reaction, not the detail — read as a judgement about how
long these have stayed open rather than as a description of any specific bug.

### Working commands

Reaching the UI on a fresh install. The server serves TLS on 443, hence the port mapping:

```sh
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

The initial credentials — user `admin`, password generated into a Secret at install time:

```sh
kubectl get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
```

That Secret is meant to be deleted once a real password or SSO is configured; it is not rotated and
it is not a long-term credential.

CLI installation: <https://argo-cd.readthedocs.io/en/stable/cli_installation/#download-with-curl>

### Repository access via a GitHub App

Documented here rather than as SSH deploy keys, and the reason is worth stating: a GitHub App has
**scoped, revocable, org-level** permissions and its token rotates automatically, where a deploy key
is a static credential per repository.

Reference: <https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/#github-app-credential>

The two pages needed to collect the identifiers — the App itself, and the installation of that App
on the account or organisation:

- <https://github.com/settings/apps/argocd-app-of-apps>
- `https://github.com/settings/installations/<github-app-installation-id>`

Registering the repository with those credentials:

```sh
argocd repo add https://github.com/andreyolv/pikakube.git \
 --github-app-id xxxx \
 --github-app-installation-id xxxxx \
 --github-app-private-key-path argocd-app-of-apps.private-key.pem
```

The same three values can be supplied declaratively instead, as a `Secret` labelled
`argocd.argoproj.io/secret-type: repository` — which is what
`app-of-apps/repo-k8s-platform.yaml` is: the template for that Secret, with the
`data` fields deliberately left empty.

The four commands used to confirm the install is wired up — accounts, connected clusters, registered
repositories, and what is actually deployed:

```sh
argocd account list
argocd cluster list
argocd repo list
argocd app list
```

### Two things to know before reusing what is checked in

- `app-of-apps/app-of-apps.yaml` still points at
  `github.com/andreyolv/mount-of-olives-platform` and a path
  `infrastructure/platform-engineering/gitops/argocd/apps` that does not exist in this repository.
  It is a preserved example from an earlier platform, not a working root application.
- `ssh-gen.sh` is the SSH-deploy-key alternative to the GitHub App flow: it generates
  a keypair, tells you where to paste the public half, and ends with the `argocd repo add
  --ssh-private-key-path` form. Use one approach or the other, not both.

---

[← GitOps](../README.md)
