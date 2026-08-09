[← Manifest templating](../README.md)

# kpt

<https://github.com/kptdev/kpt>

---

## The problem it solves

kpt starts from a rejection of templating altogether. A kpt package is a directory of **ordinary,
valid Kubernetes manifests** — no placeholders, no template markers, no values file. What you
read is what applies, and `kubectl apply -f` on the package works before kpt has touched it.

Customisation happens by **transformation, not substitution**. Functions — containers implementing
a defined interface — read the package's resources, mutate or validate them, and write them back
**in place**. Setting a namespace, injecting labels, applying policy: each is a function run over
the package, and the result is committed as normal YAML.

The consequences are the interesting part:

| Property | Effect |
|---|---|
| Package is real YAML | reviewable, lintable and appliable at every stage |
| Transformation is in place | the diff in Git shows the actual change to the actual resources |
| Upstream updates are merges | `kpt pkg update` performs a three-way merge against the upstream package, keeping local edits |
| Functions are containers | validation and mutation are the same mechanism, in any language |

That last row about updates is what the model buys you: forking a package is expected, and
pulling upstream changes into a fork is a supported operation rather than a manual reconciliation.

## When to use it

- **When packages must be forked and kept in sync with upstream.** No other tool here treats that
  as the normal case.
- **When policy is enforced as a pipeline stage** — validation functions in the same mechanism as
  mutation functions.
- **In Google Cloud's Config Sync / Config Controller world**, where the model is native.

## When not to use it

- **Almost everywhere else.** See below.
- **When you need a package ecosystem.** There is essentially none.

## Notes

The recorded link is [kptdev/kpt](https://github.com/kptdev/kpt).

kpt is from Google, and it is the tool in this folder with the clearest gap between design and
uptake: **it has struggled for adoption**. That is not a detail to be polite about. For a
configuration tool, community size *is* a technical property — it determines how many packages
and functions exist, how many examples you can copy, how quickly a question gets answered, and
how likely it is that the next person on the team has seen it before.

The tooling itself is reasonable. The in-place transformation model genuinely solves the "package
you read is not the package that applies" problem that templating creates, and the three-way
merge on update is better than what Helm offers for a modified chart. But the counterfactual is
what decides it: nobody publishes kpt packages, so the packages are yours to write, and at that
point the model's advantage over a directory of manifests plus Kustomize is thin.

Documented here for completeness and as a warning: evaluate a configuration tool on its ecosystem
before its design, because the design is what you enjoy in week one and the ecosystem is what you
live with afterwards.

---

[← Manifest templating](../README.md)
