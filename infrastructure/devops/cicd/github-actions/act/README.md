[← GitHub Actions](../README.md)

# act

<https://github.com/nektos/act>
<https://github.com/cplee/github-actions-demo/tree/master>

---

## The problem it solves

A GitHub Actions workflow can only be tested by committing it, pushing it, waiting for a runner,
and reading the log. A typo in an expression costs a commit and several minutes. Debugging a
twelve-step pipeline produces a commit history of `fix ci`, `fix ci again`, `really fix ci`.

`act` runs the workflow **locally**, in Docker. It reads `.github/workflows/`, builds the job
graph, and executes each step in a container that approximates a GitHub-hosted runner. The
feedback loop goes from *push and wait* to *run and see*.

It is also the fastest way to answer "what does this action actually do?" — you can put a
breakpoint-equivalent in front of it and inspect the filesystem.

## When to use it

- **Iterating on a workflow.** This is the main case: any change to CI YAML that you would
  otherwise test by pushing
- Debugging a step that fails only in CI, where you want a shell in something close to the runner
  environment
- Onboarding to an unfamiliar repository — running the CI locally shows what the project actually
  requires
- Verifying a **reusable workflow or composite action** behaves as expected before other
  repositories depend on it
- Running a subset: `act -j <job>` executes one job instead of the whole graph

## When not to use it

- **As proof that CI will pass.** `act`'s runner images are approximations of
  `actions/runner-images`; preinstalled tools, versions and paths differ. A workflow that passes
  under `act` can still fail on GitHub, and the reverse
- For anything needing **real GitHub context** — `GITHUB_TOKEN` permissions, OIDC federation,
  environments with approval gates, the Actions cache backend, artifact upload/download. These
  either do not work or work only with a token you supply by hand
- Self-hosted-runner-specific behaviour. `act` does not reproduce your ARC pods
- Very large images. The full `catthehacker/ubuntu:full` image is tens of gigabytes; the smaller
  images are faster but preinstall much less
- If you need the pipeline to genuinely run identically everywhere, `act` is a debugging aid, not
  the answer. [Dagger](../../dagger/README.md) is — it makes local and CI execution the *same*
  execution rather than a similar one

## Notes

The recorded links and commands.

**Installation**, recorded exactly as used:

```
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
sudo mv ./bin/act /usr/local/bin/
```

The install script drops the binary into `./bin/` in the current directory, which is why the
second line exists — the script does not put it on the `PATH` for you. Piping a script into `sudo
bash` is worth noting for what it is: convenient, and a supply-chain decision. A package-manager
install or a release binary with a verified checksum is the more careful path.

**Usage**, the two forms recorded:

```
act
act -W '.github/workflows/main.yml'
```

- `act` with no arguments simulates a **`push` event** and runs every job triggered by it. That
  default is worth knowing — running `act` in a repository with several workflows starts more than
  you probably intended.
- `act -W <file>` restricts execution to a single workflow file, which is what you want while
  iterating. `-j <job>` narrows it further to one job.

A mismatch worth pointing out in the recorded command: it references
`.github/workflows/main.yml`, while the workflow committed here is `main.yaml`. `act` will not
find a file that does not exist, and `.yml` versus `.yaml` is the classic cause. The file in this
folder is `main.yaml`.

**The demo repository**: <https://github.com/cplee/github-actions-demo/tree/master> — the sample
project `act`'s own documentation uses. The workflow committed here is that demo's: a `CI`
workflow on `push`, running `actions/checkout@v2`, `actions/setup-node@v1`, `npm install` and
`npm test` on `ubuntu-latest`. It is deliberately trivial — four steps, no secrets, no matrix —
because its job is to verify that `act` itself works before pointing it at anything real. Note the
action versions are `v2` and `v1`, which are the demo's originals and long out of date; do not
copy them into a real workflow.

The `.github/workflows/` path inside this folder is intentional: `act` discovers workflows
relative to the working directory, so the demo has to live in a directory that looks like a
repository root.

---

[← GitHub Actions](../README.md)
