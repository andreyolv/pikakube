[← GitHub Actions](../README.md)

# Workflows

Reusable workflows, and recorded experiments on where the secret boundary actually is.

---

## What is here

Four workflow files. Two of them are a working pattern; two are tests whose results are written
down as comments.

| File | What it is |
|---|---|
| `reusable-docker-build-push.yaml` | the **callee** — a complete build, scan, test and push pipeline, declared with `on: workflow_call` |
| `caller-build-image.yaml` | the **caller** — a tag push that invokes the reusable workflow |
| `caller-build-image-test.yaml` | the same caller, plus a deliberate attempt to reach the reusable workflow's secrets from a downstream job |
| `test.yaml` | a demonstration that **log masking is not a security boundary** |

These are reference copies. A reusable workflow can only be called from
`.github/workflows/` in a repository, so these are the sources kept next to the documentation
rather than the live copies.

## The reusable pipeline

`reusable-docker-build-push.yaml` is worth reading as a template, because it does the things a
Docker build pipeline usually skips. In order:

| Step | Purpose |
|---|---|
| `actions/checkout@v4` | fetch the source |
| `docker/setup-buildx-action@v3` | BuildKit, needed for cache export and multi-platform |
| `sigstore/cosign-installer@v3` | installs Cosign — see the gap noted below |
| `hadolint/hadolint-action@v3.1.0` | **lint the Dockerfile** before building, `failure-threshold: info` |
| `docker/metadata-action@v5` | derive tags and OCI labels from the Git ref; `type=semver` with `latest=false` |
| `docker/build-push-action@v5` | build **`push: false`, `load: true`** — into the local daemon, not the registry |
| `goodwithtech/dockle-action` | **image configuration** linting — the CIS-style checks |
| `aquasecurity/trivy-action` | **vulnerability** scan, `CRITICAL,HIGH`, `ignore-unfixed: true` |
| `docker run --rm <tag>` | actually **run the image** as a smoke test |
| `docker/login-action@v3` | authenticate to Docker Hub |
| `docker/build-push-action@v5` | push — a cache hit, so nothing is rebuilt |

The structural decision that makes it good: **build locally, verify, then push.** Splitting the
build into a `load: true` pass and a `push: true` pass means Dockle, Trivy and a real container
run all happen against the exact image *before* it exists in the registry. A pipeline that pushes
first and scans afterwards has already published the vulnerable image.

The build cache is `type=gha` — the Actions cache backend — with `mode=max` on the first pass, so
the second `build-push-action` invocation is a cache hit rather than a rebuild.

`latest=false` in the metadata flavour is deliberate: only the semver tag is produced, so nothing
gets a moving `latest` pointer.

## Notes

The recorded findings, all of them tested rather than read. These are the reason this folder
exists.

### 1. A job that calls a reusable workflow cannot have steps

Recorded in `caller-build-image-test.yaml`:

> **ERROR: you cannot have `steps` inside a job that uses `uses:` — `uses` runs in isolation**

And the consequence, recorded immediately after:

> **ERROR: you cannot have `outputs` inside a job that uses `uses:` either, since it cannot have
> steps to reference outputs from**

This is not a syntax restriction, it is the **isolation property**. A job either *is* a set of
steps or *is* a call to a reusable workflow — never both. The caller therefore cannot inject a
step into the callee's job, which is exactly what makes `secrets: inherit` tolerable: the caller
hands over secrets but cannot add code that runs alongside them. Outputs fall out as collateral:
job-level `outputs` are defined by referencing `steps.<id>.outputs`, and with no steps there is
nothing to reference. A reusable workflow that needs to return a value must declare
`workflow_call.outputs` itself.

The commented-out attack line makes the intent explicit:

```
#- run: echo "Trying to steal secrets: ${{ secrets.REGISTRY_PASSWORD }}"
```

That step cannot exist, which is the finding.

### 2. Secrets do not travel between jobs

The `malicious` job in the same file is a second, separate test. It runs `needs: build`, declares
an output, and then tries to print a secret:

> **ERROR: secrets are not accessible from the previous job because the jobs are isolated**

Two distinct things are being demonstrated here:

- **Job outputs are a data channel, and only that.** The `attack_output` step proves an output can
  be passed downstream. Outputs are not masked and are not intended to carry secrets — the linked
  documentation on masking and passing values between jobs is
  <https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#example-masking-and-passing-a-secret-between-jobs-or-workflows>,
  and it is recorded with the note that **GitHub outputs cannot be secrets, but can be used to
  pass information between jobs**.
- **Secrets are per job.** `secrets.DOCKERHUB_USERNAME` in a downstream job resolves only if that
  job is itself granted it. Inheriting into one job does not leak it into the next. Jobs are
  separate machines with separate environments; that is the boundary.

Also recorded, from the reusable-workflow documentation
(<https://docs.github.com/en/actions/sharing-automations/reusing-workflows#supported-keywords-for-jobs-that-call-a-reusable-workflow>):
the set of keywords a calling job may use is small and explicitly enumerated — which is the same
isolation stated from the other direction.

### 3. Environments do not cross repository boundaries

Recorded at the end of the file:

> **since an environment is created per repository, the project's repository cannot access the
> environment of the reusable-workflows repository**

The reusable workflow declares `environment: docker-build-push`. Environments — with their scoped
secrets, protection rules and required reviewers — are **owned by the repository that defines
them**. When repository A calls a reusable workflow living in repository B, the environment
resolves in **A**, not in B. B's environment secrets are not available.

This is a real constraint on centralising CI, and it is not obvious from the documentation. It
means a shared reusable workflow cannot carry its own credentials: every consuming repository must
define the environment and its secrets itself, or the secrets must be passed in explicitly by the
caller. `secrets: inherit` in `caller-build-image.yaml` is what makes the pattern work here — the
caller's secrets are handed over, because the callee has none of its own.

### 4. Log masking is defeated by transforming the value

`test.yaml` exists for one purpose:

```
echo "HOWIAM=$(echo $SECRET | sed 's/./& /g')"
```

The `sed` inserts a space between every character. GitHub masks **exact matches** of a secret's
value in log output; a transformed value is not an exact match, so it prints in full. The
commented-out alternative in the same file shows the control case — `echo "HOWIAM=${SECRET}"`
prints `***`.

The conclusion to carry: **masking is accident prevention, not a control.** Any workflow step
runs arbitrary code with the secret in its environment and can exfiltrate it trivially. The real
boundaries are the two above — job isolation and environment scoping — plus not putting the secret
in reach in the first place. Prefer OIDC federation and short-lived tokens over stored values.

Also recorded: <https://github.com/cli/cli/discussions/3397> — a `gh` CLI discussion, kept
alongside because secret retrieval through the CLI is the adjacent question.

### 5. Open questions left in the pipeline

Recorded as inline uncertainties, left unresolved on purpose:

- *"does it add `latest` too?"* on the tags line — answered by `flavor: latest=false`, which
  disables it. Worth confirming against the metadata action's own behaviour when the ref is not a
  semver tag.
- *"confirm which labels are being added — is a label or an annotation better?"* — a genuine open
  question. `docker/metadata-action` emits OCI **labels**, baked into the image config. **OCI
  annotations** live on the manifest instead, so they are readable from the registry without
  pulling the image, and they can differ per platform in a multi-arch index. Labels are more
  widely supported; annotations are the more correct place for registry-level metadata.

### 6. The signing gap

The Cosign signing block is written and **entirely commented out**. Cosign is installed by the
pipeline and never used, so nothing produced is signed. The commented code shows keyed signing
against the pushed digest, and the linked pattern for adding provenance annotations
(`repo`, `workflow`, `ref`) to the signature.

The note left beside it — *"aren't these annotations already on the image?"* — is the same
question as the labels one above, and it has the same answer: `docker/metadata-action` puts
`org.opencontainers.image.revision` and `.source` in the image **labels**, so the information is
present, but it is unsigned. Cosign annotations are attached to the **signature**, which makes
them attestable rather than merely present. That is the difference, and it is the reason to add
them even though they look redundant.

**This is the one real gap in an otherwise complete supply-chain pipeline**: it lints, scans,
tests and pushes, but publishes nothing verifiable. Keyless signing with the Actions OIDC token —
no `COSIGN_PRIVATE_KEY` to store — is the smaller change than the commented keyed version
suggests.

Also recorded, for build-time secrets:
<https://docs.docker.com/build/ci/github-actions/secrets/> — the documented way to pass secrets
into a build without baking them into a layer, which is the other place credentials leak from a
Docker pipeline.

---

[← GitHub Actions](../README.md)
