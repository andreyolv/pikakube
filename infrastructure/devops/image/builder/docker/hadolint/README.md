[← Docker](../README.md)

# hadolint

<https://github.com/hadolint/hadolint>
<https://github.com/hadolint/hadolint-action>

---

## The problem it solves

**A Dockerfile linter.** It parses the Dockerfile into an AST, applies a rule set, and runs the
shell inside every `RUN` instruction through [ShellCheck](https://github.com/koalaman/shellcheck).

That second part is what makes it more than a style checker: a `RUN` line is a shell script that
nobody reviews as one, and ShellCheck finds the unquoted variables, the broken pipelines and the
`cd` that silently fails.

The rules that catch real problems rather than opinions:

| Rule | What it prevents |
|---|---|
| `DL3008` / `DL3018` | unpinned `apt-get` / `apk` package versions — an unreproducible build |
| `DL3009` | `apt-get` lists left in the layer — dead weight in every pull |
| `DL3015` | missing `--no-install-recommends`, which pulls in hundreds of megabytes |
| `DL3020` | `ADD` used where `COPY` belongs — `ADD` also fetches URLs and unpacks archives |
| `DL3002` | the final `USER` is root |
| `DL3007` | `FROM ... :latest` — the base changes underneath you |
| `DL4006` | a pipeline in `RUN` without `pipefail`, so a failing first command is ignored |
| `SC*` | everything ShellCheck finds inside `RUN` |

It is a single static binary with no runtime dependencies, which is why it fits equally well in a
pre-commit hook, in CI and on a laptop.

## When to use it

- **in CI on every change to a Dockerfile** — it is fast enough that there is no argument against
- as a pre-commit hook, so the feedback arrives before the review does
- when standardising Dockerfiles across many repositories: the rule set is the standard, written
  down and enforced
- to catch shell mistakes inside `RUN` that no reviewer reads carefully

## When not to use it

- **as a security scanner** — it reads the Dockerfile, not the image. It cannot tell you that a
  package has a CVE; that is `infrastructure/security/3-container/`
- as the only check — the image can still be wrong in ways the source does not show, which is
  what [dockle](../dockle/README.md) is for
- where there is no Dockerfile: [Buildpacks](../../buildpacks/README.md) generate the image and
  there is nothing to lint
- with every rule enabled and none reviewed — some rules are opinions, and an unconfigured
  linter that fails every build gets disabled rather than fixed

## Notes

Recorded links:

- <https://github.com/hadolint/hadolint> — the linter.
- <https://github.com/hadolint/hadolint-action> — the GitHub Actions wrapper, which is how it
  ends up running on pull requests without anyone installing anything.

Installation, recorded as a sequence — get the current version from
<https://github.com/hadolint/hadolint/releases> first:

```bash
VERSION=v2.12.0
wget -O hadolint https://github.com/hadolint/hadolint/releases/download/${VERSION}/hadolint-Linux-x86_64
sudo mv hadolint /usr/local/bin/hadolint
sudo chmod +x /usr/local/bin/hadolint
```

A single static binary downloaded from a release, which is the whole installation. The `VERSION`
variable is pinned deliberately — the note says to check the releases page for the current one
rather than fetching whatever `latest` resolves to, so the version in CI matches the version on
the laptop and the two do not disagree about what passes.

Running it against a configuration file:

```bash
hadolint --config .hadolint.yaml Dockerfile
```

There is a `.hadolint.yaml` in this folder. That file is the point of the exercise: it is where
rules get ignored deliberately, where trusted base-image registries are listed, and where the
failure threshold is set. Keeping it in the repository means the same rules apply in the hook, in
CI and locally — an unconfigured hadolint fails on almost every real Dockerfile, and the usual
response to that is to stop running it.

## Where it fits here

Paired with [dockle](../dockle/README.md), which checks the built image rather than its source.
They overlap barely and complement each other: hadolint says *"this Dockerfile is written badly"*,
dockle says *"this image is configured badly"*. Both are construction checks, and neither is
vulnerability scanning.

---

[← Docker](../README.md)
