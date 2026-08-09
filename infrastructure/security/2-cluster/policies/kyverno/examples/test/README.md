[← Kyverno examples](../README.md)

# Testing Kyverno policies

<https://kyverno.io/docs/kyverno-cli/usage/test/>
<https://github.com/kyverno/kyverno/tree/main/cmd/cli/kubectl-kyverno>

A worked example of the Kyverno CLI's test harness: a policy, a resource, and a declaration of what
the result should be.

---

## The problem it solves

A policy is code that runs on the write path of every request to the API server. Deploying an
untested one has two failure modes and both are bad: it blocks something it should not, and every
deployment in the cluster starts failing; or it silently matches nothing, and everyone believes a
control exists when it does not.

The second is worse, because there is no signal. A policy with a typo in `match.resources.kinds`
never fires, produces no error, and reports green.

`kyverno test` runs policies against fixture resources **without a cluster** — no API server, no
webhook, no namespace. That makes it fast enough to run in CI on every pull request that touches a
policy.

The three files here:

| File | Role |
|---|---|
| `clusterpolicy.yaml` | the policy under test — `disallow-latest-tag`, in `Audit` mode, with rules `require-image-tag` and `validate-image-tag` |
| `resource.yaml` | the fixture — a Pod named `myapp-pod` running `nginx:1.12` |
| `kyverno-test.yaml` | a `Test` resource declaring which policy, which resources, and the **expected result** for each rule |

The `Test` object is the interesting one. It names each policy/rule/resource combination and asserts
`result: pass`. Since `nginx:1.12` has a tag and it is not `latest`, both rules should pass — and if
someone edits the policy so that a valid image starts failing, the test says so.

Expected results are not limited to `pass`: `fail`, `skip` (the rule did not apply), `warn` and
`error` are all assertable, which is how you prove a policy rejects what it is supposed to reject.

## When to use it

- **Every policy, before it reaches a cluster.** This is the cheapest possible check and it catches
  the two failure modes above.
- **In CI.** No cluster is required, so it runs in a container with the CLI installed and nothing
  else. A pull request touching `policies/` should not merge without it.
- **When tuning a policy on an existing cluster.** Copy real manifests that currently break into
  fixtures, assert `pass`, and change the policy until they do — that is the audit-to-enforce loop
  ([`../../../README.md`](../../../README.md#4-audit-vs-enforce)) done offline instead of by
  redeploying and watching.
- **To prove a rule actually matches.** Assert `fail` on a resource you know is bad. A rule with a
  wrong `kinds` list produces `skip`, which is the signal that the policy is inert.
- **Alongside `kyverno apply`.** The related command runs a policy against a directory of manifests
  and prints results without asserting anything — useful for a one-off sweep, and the natural
  companion for the first pass over an existing repository.

## When not to use it

- **As the only check.** It evaluates the policy engine's logic, not the cluster. It cannot tell you
  whether the webhook is registered, whether `failurePolicy` is right, whether Kyverno has the RBAC
  it needs, or whether the admission controller can be reached.
- **For `generate` and `mutate-existing` rules.** Those depend on the background controller and on
  cluster state — other namespaces, source objects, RBAC. The CLI covers them only partially, and
  the interesting failures (missing permissions, `generateExisting` not set) are precisely the
  cluster-side ones. See [`../../policies/sync-secret/`](../../policies/sync-secret/README.md).
- **For policies that call out to a registry.** `block-large-images.yaml` in the parent folder
  fetches an image manifest during evaluation; a test for it needs network access and the results
  change when the image does.
- **As a substitute for audit mode.** A test proves the policy behaves as written on the fixtures
  you thought of. Running it in `Audit` against real traffic tells you what you did not think of.

## Notes

The original note from `doc.md`, translated and explained.

### The command

> ```
> kyverno test .
> ```

Run from this directory. The CLI walks the path recursively, finds every `kyverno-test.yaml`,
resolves the `policies` and `resources` paths listed inside it relative to that file, evaluates
them, and compares against the declared `results`.

Two consequences of "recursively": pointing it at the repository root runs every test in the
repository, which is what a CI job should do; and the paths inside a `Test` are relative to the test
file, not to the working directory, so a test folder is self-contained and can be moved.

The CLI is `kyverno`, installable standalone or as the `kubectl kyverno` plugin. It is versioned
alongside the controller, and the version matters — policies using a newer `apiVersion` (several in
the parent folder use `kyverno.io/v2beta1`) need a CLI new enough to parse them.

---

[← Kyverno examples](../README.md)
