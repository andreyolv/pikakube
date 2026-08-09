[← GitOps](../README.md)

# Multi-repo tenancy

Giving a team their own repository without giving them the cluster.

---

## The problem it solves

A single GitOps repository is the easiest thing to set up and the hardest thing to share. Every
team commits to it, every team's manifests are reconciled by the same controller with the same
service account, and one malformed file can stall reconciliation for everyone.

The multi-repo pattern splits it: **one source object and one service account per tenant**. Team 1
gets a `GitRepository` pointing at their own repo, and a `Kustomization` that reconciles it — but
that `Kustomization` runs as `serviceAccountName: multi-tenancy-gitrepositories`, so what it is
allowed to create is decided by RBAC on the platform side, not by what the team writes in their repo.

This is the piece most multi-repo setups omit. Without `serviceAccountName`, a tenant
`Kustomization` is applied with the kustomize-controller's own permissions, which are
cluster-admin-equivalent. A team that can commit to their own repository can then create a
`ClusterRoleBinding`. With the service account set, they get exactly the verbs the platform granted.

This is not a tool. It is the arrangement of Flux objects that makes tenant isolation real, kept
here as a reference implementation.

## When to use it

- more than one team deploys to the same cluster and they should not be able to affect each other
- teams want their manifests to live beside their code rather than in a platform repository
- the platform team needs to bound what a tenant can create, per tenant, in a way the tenant cannot
  edit
- a single repository has grown to the point where one bad commit is a shared outage

## When not to use it

- one team, one repository — the isolation machinery buys nothing and every tenant is another
  source, another credential and another service account to maintain
- tenants need genuinely separate control planes rather than separate namespaces; that is a
  virtual-cluster or separate-cluster question, not a repository-layout one
- the teams are trusted with cluster-wide permissions anyway, in which case the RBAC is decoration

## Notes

### What is checked in

Four objects, and they only make sense read together:

| File | What it does |
|---|---|
| `namespace.yaml` | the tenant namespace — `team1` |
| `helm/gitrepository2.yaml` | the tenant's `GitRepository`, over SSH, with a `secretRef` |
| `kustomization.yaml` | reconciles that source into `targetNamespace: team1` **as the tenant service account** |
| `rbac.yaml` | the `ServiceAccount`, `ClusterRole` and `ClusterRoleBinding` that bound what the tenant can create |

The `ClusterRole` grants `*` on Deployments and Services and nothing else. That is deliberately
narrow: a tenant repository containing anything other than those two kinds will fail to reconcile,
visibly, rather than succeed quietly.

One thing to notice about the file layout: `gitrepository2.yaml` lives in a folder called `helm/`
and contains no Helm at all. That is a misfiled path, not a pattern to copy.

### The recorded gotcha

A comment left at the bottom of the `GitRepository`, translated:

> **"If you specify only the files you want, Kustomize errors trying to find files in `resources`
> that do not exist."**

The context is the `ignore` block, which uses the exclude-everything-then-re-include form:

```yaml
ignore: |
  # exclude all
  /*
  # include only specific files
  !/kubernetes2/base/
  !/kubernetes2/prd/
```

This is a real trap and it is worth understanding rather than working around. Flux's `ignore` filters
what the **source controller** puts into the artefact. Kustomize then runs against that filtered
tree, and if a `kustomization.yaml` in it lists a resource that was filtered out, the build fails
with a missing-file error — pointing at a path that exists perfectly well in the repository.

The symptom is confusing precisely because the file is there when you look. The fix is to keep the
`ignore` patterns and the `resources` lists consistent: exclude a directory only if nothing inside
the included set references it.

### Generating the SSH credential

The tenant `GitRepository` authenticates with a deploy key, via `secretRef:
github-repository-ssh-team1`. The original tutorial for producing that Secret, translated:

```sh
# identity
cd ~/.ssh
mkdir key1
ssh-keygen -f key1/id_rsa
```

- Add the **public** key (`cat ~/.ssh/id_rsa.pub`) to the repository's deploy keys, under
  `Settings → Deploy keys` on the tenant repository.
- Add the **private** key, base64-encoded (`cat ~/.ssh/id_rsa | base64`), as the `identity` field of
  the Secret.

The third field is `known_hosts`, and it is the one people skip. Without it the SSH connection has
nothing to verify the server against, so the source will not reconcile. Two ways to get it:

- GitHub's published fingerprints:
  <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints>
- or the local file: `cat ~/.ssh/known_hosts` — the line beginning
  `github.com ecdsa-sha2-nistp256 AAAA...`

`flux create secret git` produces all three fields in one command and is the shorter path; the manual
version is recorded here because it is what you need when the Secret is created by something other
than the CLI.

A deploy key is a **static per-repository credential**. It does not rotate and it is not scoped
beyond that one repository. The GitHub App alternative is described in
[`argocd/`](../argocd/README.md) — the same trade-off applies to Flux sources.

The tenant repository referenced by the checked-in example is
`ssh://git@github.com/andreyolv/team1`, which is an illustration rather than a live source.

---

[← GitOps](../README.md)
