[← Version control](../README.md)

# Git

<https://github.com/git/git>
<https://github.com/cli/cli>
<https://github.com/github/docs>

---

## The problem it solves

**The protocol and the tool everything else in this folder is built around.** Git is not really a
choice — every repository is a Git repository, and the forges in
[`../`](../README.md) are servers wrapped around it.

So this folder is not about deciding to use Git. It is about the **conventions** that decide
whether a repository's history is useful or noise:

| Concern | Answer |
|---|---|
| How commits are written | Conventional Commits, enforced by commitlint |
| How versions are derived | SemVer, generated from commit types |
| How the changelog is produced | generated, not written by hand |
| What must never enter history | secrets — caught before the commit, not after |
| What runs before every commit | pre-commit hooks: formatting, linting, scanning |
| How work is branched | see [§5 of the parent](../README.md#5-branching-strategies) |

The property that makes conventions worth enforcing is that **Git history is permanent and
replicated**. A bad commit message is a small annoyance forever; a committed credential is a
compromised credential in every clone, immediately.

## When to use it

Always. The interesting question is which conventions to adopt alongside it, and the answer
follows from what you want to automate:

- **automatic versioning and changelogs** → Conventional Commits plus semantic-release
- **no secrets in history** → `git-secrets` or an equivalent, in a pre-commit hook
- **consistent code before review** → pre-commit with formatters and linters
- **a readable history** → a merge policy chosen deliberately, and applied by the forge

## When not to use it

There is no alternative worth documenting. What is worth avoiding is Git used as a **file store**:
large binaries, datasets and build artefacts bloat every clone forever, because history is
replicated in full. Git LFS exists for that and is itself a commitment; object storage is usually
the better answer.

## Notes

Everything below was recorded here, grouped by what it is for.

**The everyday commands**

```bash
git fetch origin main
git merge origin/main
git status
git push
```

Recorded as the working loop. The `fetch` and `merge` pair is worth noting as deliberate rather
than sloppy: it is `git pull` split into its two halves, which lets you see what arrived before
integrating it. The habit is a good one on a shared branch, where a `pull` that quietly merges — or
rebases, depending on configuration — is how surprises happen.

**Learning and certification**

- <https://github.com/FidelusAleksander/ghcertified/tree/master/content/questions> — practice
  questions for the GitHub certifications. Recorded as study material.

**Branching and commit conventions**

- <https://github.com/nvie/gitflow> — the git-flow branching model and its helper scripts:
  `develop`, `release/*`, `hotfix/*`, `feature/*` alongside `main`. Worth knowing and, for a
  continuously deployed service, worth **not** adopting — its author has said much the same. See
  [§5 of the parent](../README.md#5-branching-strategies).
- <https://www.conventionalcommits.org/en/v1.0.0/> and
  <https://github.com/conventional-commits/conventionalcommits.org> — the Conventional Commits
  specification. `feat:`, `fix:`, `chore:`, and `BREAKING CHANGE:` in the footer. The point is not
  tidiness: it makes the commit message **machine-readable**, which is what everything in the
  next two groups depends on.
- <https://github.com/semver/semver> — Semantic Versioning. The contract that `MAJOR.MINOR.PATCH`
  actually means something, and the target that Conventional Commits feed into: `fix:` produces a
  patch, `feat:` a minor, a breaking change a major.

**Automating versions and changelogs**

- <https://github.com/conventional-changelog/commitlint> — validates that commit messages match
  the convention. **This is the enforcement step**, and without it the convention is a suggestion
  that decays within weeks. Run it in a hook and in CI.
- <https://github.com/conventional-changelog/conventional-changelog> — generates a changelog from
  conventional commits.
- <https://github.com/conventional-changelog/standard-version> — bumps the version, generates the
  changelog and tags, in one command. Now largely superseded; the project recommends alternatives.
- <https://github.com/semantic-release/semantic-release> — the fuller version of the same idea:
  determines the next version from the commits, generates release notes, tags and publishes,
  entirely from CI. Fully automated releases, with the trade-off that a mistyped commit type
  publishes the wrong version number.
- <https://github.com/commitizen-tools/commitizen> — a prompt-driven commit tool that produces
  conventional messages, plus its own version bumping. The friendlier entry point when a team is
  adopting the convention and nobody remembers the prefixes.
- <https://github.com/orhun/git-cliff> — a fast changelog generator in Rust, highly configurable
  through templates. The modern alternative to `conventional-changelog`.
- <https://common-changelog.org/> — a specification for changelogs written **for humans**, and a
  deliberate counterpoint to generated ones: it argues that a changelog is curated, not derived.
- <https://github.com/olivierlacan/keep-a-changelog> — the widely used `CHANGELOG.md` convention
  with `Added` / `Changed` / `Fixed` / `Removed` sections. The format most tooling emits.
- <https://github.com/release-drafter/release-drafter> — drafts GitHub release notes from merged
  pull requests as they land, so the notes exist before the release does. Labels on the PRs decide
  the categories.
- <https://github.com/twisted/towncrier> — news-fragment based changelogs: each change adds a small
  file, and the files are assembled at release time. It solves the merge-conflict problem that a
  single shared `CHANGELOG.md` always creates.

The whole chain, in one line:

```
Conventional Commits → commitlint → semantic-release → SemVer tag → CHANGELOG
```

**Hooks and preventing mistakes**

- <https://github.com/pre-commit/pre-commit> — the hook framework. Hooks are declared in
  `.pre-commit-config.yaml`, so everyone on the repository runs the same checks, and CI can run
  the identical set.
- <https://github.com/pre-commit/pre-commit-hooks> — the standard hook collection: trailing
  whitespace, end-of-file, YAML and JSON validity, large files, merge-conflict markers, private
  keys. The `check-added-large-files` and `detect-private-key` hooks are the two that prevent
  permanent damage.
- <https://github.com/awslabs/git-secrets> — scans commits for credential patterns and **refuses
  the commit**. The emphasis matters: a secret caught at commit time is a non-event, and a secret
  caught after a push is a rotation. Removing it from history does not undo the exposure, because
  history is already replicated to every clone and, on a public repository, to scrapers.

**Ignoring what should never be committed**

- <https://github.com/github/gitignore> — GitHub's collection of `.gitignore` templates per
  language and toolchain.
- <https://www.toptal.com/developers/gitignore/> — a generator that composes several templates,
  which is what a real project needs: a language, an editor and an operating system at once.

**GitHub-specific automation**

- <https://github.com/PyGithub/PyGithub> — the Python client for the GitHub API. The tool for
  auditing and bulk-changing repository settings across an organisation.
- <https://github.com/probot/probot> — a framework for building GitHub Apps in Node.js, for
  automation that reacts to webhooks rather than running in a pipeline.
- <https://github.com/marketplace/actions/delete-merged-branch> — deletes a branch after its pull
  request is merged. Small, and it is the difference between a branch list that is useful and one
  nobody reads.
- <https://github.com/actions/labeler> — labels pull requests automatically from the paths they
  touch. Feeds directly into `release-drafter`, which categorises release notes by label.
- <https://github.com/gitbutlerapp/gitbutler> — a Git client built around working on several
  branches simultaneously in one working directory. An alternative model to stashing and switching.
- <https://github.com/star-history/star-history> — charts a repository's star history over time.
  Recorded as an evaluation aid: for judging whether a project is growing, plateaued or abandoned,
  a star curve is a rough but fast signal — and this repository's documentation makes that
  judgement about projects repeatedly.

**Tag pattern enforcement**

- <https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository>
  — recorded under the heading *"define tag pattern semver with github ruleset"*. GitHub rulesets
  can target **tags** as well as branches, so a rule can require every tag to match a SemVer
  pattern and forbid tags being deleted or moved. That is the enforcement side of
  <https://github.com/semver/semver>: the convention becomes a rule the forge applies rather than
  one people remember. The exported rulesets in [`../github/`](../github/README.md) are the same
  mechanism applied to branches.

**Repository tagging convention** (recorded in Portuguese, translated):

> **Tags**
>
> The repository must have a tag containing the application's APPID. In the image below you can
> see the application's tag in the repository's *about* section.
>
> Other tags denoting the business area, or even the application's context, are very welcome,
> since they make the repository easier to find in searches.

"Tags" here means **GitHub repository topics** — the labels in a repository's *About* panel — not
Git tags, which is worth stating because the same word is used for two different things three
paragraphs apart. The convention is that every repository carries its application identifier as a
topic, which makes the link from a service in a catalogue to the repository that builds it
mechanical rather than a matter of guessing the name. Extra topics for business area or context
are encouraged for discoverability. GitHub's search supports `topic:` queries, so this is also the
cheapest possible service catalogue when there is no real one. The `git.PNG` file in this folder
is the referenced screenshot.

**SSH setup** (recorded in Portuguese as `tutorial-ssh`, translated):

> **Tutorial: adding an SSH key to Git**
>
> In the terminal, run the commands one at a time:
>
> ```bash
> ssh-keygen -t ed25519 -C "your_email@example.com"
> eval "$(ssh-agent -s)"
> ssh-add ~/.ssh/id_ed25519
> cat ~/.ssh/id_ed25519.pub
> ```
>
> Copy the text that appears on screen.
>
> Then, if this is the first time you are using Git, configure it — again one command at a time:
>
> ```bash
> git config --global user.name "Your name here"
> git config --global user.email your_email@example.com
> ```
>
> Then go to <https://github.com/settings/keys>, click **New SSH Key**, and paste the key you
> copied. Under **Configure SSO**, click **Authorize** for the repository to authorise it.
>
> That is it — `git clone` will now work.

Three things in that worth drawing out. **`ed25519` rather than RSA** is the current
recommendation — shorter keys, better security, and universally supported now. **The `Configure
SSO` step is not optional** in an organisation with SAML single sign-on: the key works everywhere
else and is silently rejected for that organisation's repositories until it is authorised, which
produces a permission error that looks like a missing key rather than an unauthorised one. And
`user.email` should match a verified address on the account, or commits will not be attributed
and will not appear in the contribution history.

## Driving Git from Python

<https://github.com/gitpython-developers/GitPython>

Anything that automates a repository — a bot that commits a version bump, a script that reads
history to build a changelog — otherwise assembles `git` invocations with string concatenation and
parses the output with regular expressions. That works and it breaks on the first filename with a
space in it. **GitPython** gives objects instead: `Repo`, `Commit`, `Blob`, `Diff`, `Remote`.

Two facts from its own README decide most of the evaluation, and neither is a footnote:

**It is in maintenance mode.** The maintainers state it plainly — *"there will be no feature
development, unless these are contributed"*, and *"no bug fixes, unless they are relevant to the
safety of users, or contributed."* The original author's focus moved to
[Gitoxide](https://github.com/Byron/gitoxide), a Rust implementation of Git. A stable library doing
a well-defined job in maintenance mode is a reasonable dependency; it does mean a bug you hit is a
bug you fix.

**It leaks resources in long-running processes.** Also stated directly: *"GitPython is not suited
for long-running processes (like daemons) as it tends to leak system resources"* — the cause is
reliance on destructors, which no longer run deterministically in modern Python.

That second point is the one that matters in a Kubernetes repository, and it is a neat trap: the
obvious use for such a library is a **controller** that watches something and commits back to Git,
and that is exactly the shape it is documented not to suit. Keep it inside short-lived processes — a
`Job`, a CI step, a CLI. `repo.close()` or the context manager mitigates it; it does not make a
daemon a good idea.

It also **invokes the `git` binary** rather than implementing Git, so it needs Git 1.7+ on `PATH` —
and a slim Python base image usually does not have it, with the failure appearing at runtime.

| Option | When it wins |
|---|---|
| **`subprocess`** | one or two commands — no dependency, no surprises |
| **GitPython** | the object model genuinely saves work, in a short-lived process |
| **pygit2** | libgit2 bindings: faster, no subprocess, safe for long-running — at the cost of a native dependency |
| **dulwich** | pure Python, no `git` binary needed — useful in constrained images |

For this platform the plausible use is GitOps automation — writing back to the repository Flux
reconciles from. Worth noting that the purpose-built answers already exist:
[Flux's image automation](../../image/update/README.md) writes new tags back to Git with no custom
code, and [release-please](../../cicd/release-please/README.md) generates versions and changelogs
from commit history. Reaching for a library means the requirement is genuinely bespoke — and if that
bespoke thing is a controller, this is the wrong library for it.

## Where it fits here

Not something to deploy — this folder is the **conventions layer**, and it applies to every
repository regardless of which forge from [`../`](../README.md) hosts it.

The highest-value items, in order: `git-secrets` or an equivalent in a pre-commit hook, because it
prevents the only mistake here that cannot be undone; pre-commit for everything else, because it
moves the feedback earlier than review; and Conventional Commits with commitlint, because
everything about automated versioning and changelogs depends on the format actually being
followed.

---

[← Version control](../README.md)
