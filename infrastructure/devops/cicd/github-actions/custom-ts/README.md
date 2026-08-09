[← GitHub Actions](../README.md)

# Custom actions — TypeScript

<https://github.com/actions/toolkit>
<https://github.com/actions/typescript-action>
<https://github.com/github/local-action>

---

## The problem it solves

Once the same twenty lines of `run:` appear in five workflows, they should be an action. GitHub
supports three kinds, and the choice is not stylistic:

| Kind | How it runs | Start-up | Platform |
|---|---|---|---|
| **JavaScript / TypeScript** | directly on the runner, in the runner's Node | **fast** — no image to pull | Linux, Windows, macOS |
| **Docker container** | in a container the runner builds or pulls | slow — build or pull every time | **Linux only** |
| **Composite** | a bundle of steps in the caller's job | none | wherever the steps run |

TypeScript is the mainstream path because it is the only one that is both fast and
cross-platform, and because it is the only one with a **real API**: `@actions/core` for
inputs, outputs, secret masking, logging and job summaries; `@actions/github` for a pre-authenticated
Octokit client; `@actions/exec`, `@actions/io`, `@actions/cache`, `@actions/artifact` for the rest.
Every first-party action is written this way.

The trade that comes with it: a JavaScript action is executed from **committed, compiled
JavaScript**, not from source. The build output has to be bundled and checked in, because the
runner does not run `npm install` for you.

## When to use it

- Logic reused across **several repositories**, where a composite action's step-only model is not
  enough
- Anything that talks to the **GitHub API** — `@actions/github` gives you an authenticated Octokit
  with retries, which is far better than hand-rolled `curl`
- You need **structured outputs, secret masking or job summaries** — the `@actions/core` API is
  the supported way to do all three
- The action must run on **Windows or macOS runners**, which rules out container actions entirely
- Start-up latency matters, because the action is called in many jobs

## When not to use it

- The logic is a handful of steps used in one repository. A **composite action** is simpler and
  needs no build step
- The tool is already a container, or needs a specific runtime. Then a **container action** is
  the honest packaging — see [`custom-py`](../custom-py/README.md)
- The team does not write TypeScript. A container action in a language they know is better than a
  badly maintained one in a language they do not
- The whole pipeline could be a program instead. If you are writing enough logic that packaging it
  as an action feels like the answer, [Dagger](../../dagger/README.md) is the larger version of the
  same idea — and it is not GitHub-specific
- You are unwilling to commit build artifacts. There are ways around it, all of them worse than
  accepting a `dist/` directory in the repository

## Notes

The three recorded links are the complete toolchain, and each one covers a distinct stage.

**<https://github.com/actions/toolkit>** — the official packages. This is a monorepo, and the
useful thing about it is that each package documents a piece of the runner contract that is
otherwise invisible:

- `@actions/core` — inputs, outputs, `setSecret` for masking, `setFailed`, grouped logging, job
  summaries. Note that masking here is the *same* best-effort mechanism described in
  [GitHub Actions §5](../README.md#5-secrets-and-what-is-actually-a-boundary): useful, not a
  boundary
- `@actions/github` — an Octokit client already authenticated with the job's `GITHUB_TOKEN` and
  already carrying the event payload
- `@actions/exec` — running commands with captured output, which is the part everyone otherwise
  writes badly
- `@actions/cache`, `@actions/artifact` — the same backends the first-party actions use

**<https://github.com/actions/typescript-action>** — the official **template repository**. Start
from it rather than assembling a project by hand: it comes with the `action.yml` metadata, the
TypeScript config, the bundler wiring, tests, and the CI that verifies the committed bundle is in
sync with the source. That last check is the one that matters — the most common failure in a
TypeScript action is editing `src/` and forgetting to rebuild `dist/`, which produces an action
that silently runs the old code.

**<https://github.com/github/local-action>** — runs an action **locally, in a debugger**, without
pushing and without Docker. This is the piece that makes the whole approach workable: it fills in
the runner's environment variables and inputs so the action's entry point can be executed and
stepped through from an editor.

The distinction from [`act`](../act/README.md) is worth being precise about, since both are
"local":

| | `local-action` | `act` |
|---|---|---|
| Runs | **one action**, in Node, in your debugger | a **whole workflow**, in Docker |
| For | developing the action | testing the workflow that calls it |

They compose: `local-action` while writing the action, `act` once it is wired into a workflow.

**Nothing is built in this folder** — no `action.yml`, no `src/`. It is a mapped path with the
reference implementations recorded, not an action this repository ships.

---

[← GitHub Actions](../README.md)
