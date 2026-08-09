[← Image update automation](../README.md)

# Flux image update automation

<https://github.com/fluxcd/image-reflector-controller>
<https://github.com/fluxcd/image-automation-controller>

---

## The problem it solves

**A new image tag appears in the registry, and the change reaches the cluster as a Git commit.**
Flux's two image controllers close the loop between the registry and the repository without a
pipeline holding cluster credentials and without anything mutating the cluster directly.

| Resource | Controller | What it does |
|---|---|---|
| **`ImageRepository`** | image-reflector | polls a registry repository and records the tags it finds |
| **`ImagePolicy`** | image-reflector | filters and orders those tags, and names one as selected |
| **`ImageUpdateAutomation`** | image-automation | writes the selected image into the manifests and **commits to Git** |

The order matters and so does the separation: scanning is one controller's job, and writing to Git
is another's. An `ImagePolicy` can be created and inspected — `kubectl get imagepolicy` shows the
tag it has selected — **without** anything being committed, which makes the policy debuggable
before it is given the ability to change the cluster.

The property this preserves is the important one: **the deployment happens because Git changed.**
The repository remains a complete description of what is running, a `git revert` remains a
rollback, and nothing outside the cluster needs credentials to it.

## When to use it

- **Flux is already the reconciliation engine** — this is the native answer, maintained as part of
  the toolkit
- images built by anything at all should be picked up, without the builder knowing the deployment
  repository's layout
- development and staging environments where new builds should deploy themselves
- production, **with the automation opening a pull request** rather than committing to the
  reconciled branch

## When not to use it

- where Argo CD is the engine — [Argo CD Image Updater](../argo-image-updater/README.md) is the
  equivalent
- where CI already commits the new tag reliably and adding a controller gains nothing
- with tags that cannot be ordered — chasing `:latest` is not a policy, it is a hope
- where a release must be a deliberate human act and no amount of pull-request gating satisfies
  that

## Notes

The two controllers:

- <https://github.com/fluxcd/image-reflector-controller> — scans registries and maintains
  `ImageRepository` and `ImagePolicy`.
- <https://github.com/fluxcd/image-automation-controller> — applies the policies to manifests and
  commits.

Both are optional Flux components: `flux bootstrap` does not install them unless they are named,
which is worth knowing when the resources apply cleanly and nothing ever happens.

**What is set up here** — a complete worked example, not a mapping:

| Path | What it is |
|---|---|
| `flask-flux/` | the application: a `Dockerfile`, `requirements.txt` and `app/app.py` |
| `flask/` | its Kubernetes manifests — namespace, `Deployment`, `Service` |
| `flux-image/` | the three automation resources |

The `ImageRepository` polls Docker Hub every minute:

```yaml
spec:
  image: andreyolv/flask-flux
  interval: 1m0s
```

The `ImagePolicy` is the piece worth studying, because it is the part that is usually got wrong:

```yaml
spec:
  imageRepositoryRef:
    name: flask-flux
  filterTags:
    pattern: '^main-[a-f0-9]+-(?P<ts>[0-9-T]+)'
    extract: '$ts'
  policy:
    alphabetical:
      order: asc
```

Read it in three parts. **The pattern anchors to `main-`**, so only tags built from the `main`
branch are candidates — a feature-branch build can never be selected, no matter how new it is.
**The named capture group `ts` isolates the timestamp**, and `extract: '$ts'` says to order by
that fragment rather than by the whole tag; without it, the commit hash in the middle of the tag
would dominate the sort and the selection would be effectively random. **`alphabetical` with
`order: asc` selects the last in ascending order**, which is the newest — and that only works
because the timestamp is zero-padded and written largest unit first, so lexical order and
chronological order agree. That is the whole trick described in
[§5 of the parent](../README.md#5-tag-policies-and-how-they-go-wrong), implemented correctly.

The `ImageUpdateAutomation` does the writing:

```yaml
spec:
  interval: 1m0s
  sourceRef:
    kind: GitRepository
    name: flux-system
  git:
    checkout: { ref: { branch: main } }
    commit:
      author: { name: fluxcdbot, email: fluxcdbot@users.noreply.github.com }
      messageTemplate: '{{range .Updated.Images}}{{println .}}{{end}}'
    push: { branch: main }
  update:
    path: ./kubernetes
    strategy: Setters
```

Three details worth naming. It reuses the **`flux-system` `GitRepository`** — the same source Flux
bootstrapped with — so the credential already exists and has write access. **`strategy: Setters`**
means it edits only values marked with an `$imagepolicy` comment in the YAML, which is what makes
a controller with commit access acceptable: it cannot rewrite anything it was not pointed at.
And **`path: ./kubernetes`** scopes it to one directory, so nothing outside it can be touched.

For the automation to do anything, the `Deployment` must carry the marker:

```yaml
image: andreyolv/flask-flux:main-abc1234-... # {"$imagepolicy": "flux-system:flask-flux"}
```

Without that comment the resources reconcile happily and nothing is ever updated — the most common
reason this setup appears to be broken.

**The one thing to change before this shape is used for anything that matters**: it commits
straight to `main`, the branch Flux reconciles, so a new image deploys itself with no review. That
is correct for a demonstration and is the pattern
[§6 of the parent](../README.md#6-when-not-to-automate) argues against for production. Committing
to a separate branch and opening a pull request keeps the automation and restores the decision.

## Where it fits here

**The right answer for this repository**, because Flux is already the reconciliation engine and
this keeps every change to the cluster visible as a commit — the same mechanism as everything
else.

[Argo CD Image Updater](../argo-image-updater/README.md) is the Argo-side equivalent, and
[Watchtower](../watchtower/README.md) is the model to avoid on Kubernetes: it changes running
state without touching Git at all.

---

[← Image update automation](../README.md)
