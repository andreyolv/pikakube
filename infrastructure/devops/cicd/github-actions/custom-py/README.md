[← GitHub Actions](../README.md)

# Custom actions — Python

<https://github.com/actions/container-action>
<https://jacobtomlinson.dev/posts/2019/creating-github-actions-in-python/>

---

## The problem it solves

GitHub Actions runs JavaScript actions natively. **It does not run Python actions natively** — there
is no `runs.using: python`. The only supported way to ship an action written in Python is to
package it as a **container action**: a `Dockerfile`, an image, and an `action.yml` that declares
`runs.using: docker`.

That is the whole point of this folder — the mechanics of doing it, and the costs that come with
it:

| | Container action (Python) | JavaScript action |
|---|---|---|
| Start-up | **slow** — the runner builds or pulls the image on every job | fast |
| Platforms | **Linux runners only** | Linux, Windows, macOS |
| Dependencies | fully controlled, baked into the image | whatever Node the runner has |
| Inputs | environment variables `INPUT_<NAME>`, uppercased, spaces to underscores | `@actions/core.getInput()` |
| Outputs | append to the `$GITHUB_OUTPUT` file | `core.setOutput()` |
| Distribution | an image, or a `Dockerfile` built per run | committed compiled JavaScript |

The contract is a **file and environment protocol**, not an API — which is why a Python action is
possible at all, and why it is more fiddly than the TypeScript path.

## When to use it

- The logic **is already Python** — a script the team maintains, using libraries that exist only
  in Python
- The action needs a **specific, controlled runtime**: pinned interpreter version, system packages,
  compiled dependencies. The image guarantees it in a way `setup-python` plus `pip install` does
  not
- The tool being wrapped is a CLI that already ships as a container
- Reproducibility matters more than latency, and the image can be **prebuilt and pinned by digest**
  rather than built on every run

## When not to use it

- It is a few lines of Python. A `run:` step with `setup-python` is faster to write, faster to
  start, and works on every runner OS
- **Start-up time matters.** Building the image on every job, or pulling it, dominates a short
  action's runtime. This is the single biggest reason to avoid container actions
- The action must run on **Windows or macOS** runners. Container actions cannot
- It is a general reuse problem rather than a Python problem — then
  [`custom-ts`](../custom-ts/README.md) is the mainstream path with a real API behind it
- You are wrapping a whole pipeline rather than one step. [Dagger](../../dagger/README.md) has a
  Python SDK and expresses exactly this — containerised logic written in Python — without the
  action packaging or the GitHub coupling

## Notes

**<https://github.com/actions/container-action>** — GitHub's official **container action template**.
This is the authoritative starting point and the one that keeps up with the runner contract: the
`Dockerfile`, the `action.yml` with `runs.using: docker`, and the input/output handling done the
current way. Use it rather than assembling the pieces yourself, because the parts that change over
time — how outputs are written, how paths are mounted — are exactly the parts that break silently.

**<https://jacobtomlinson.dev/posts/2019/creating-github-actions-in-python/>** — the blog post that
was for years the reference on this, and still the clearest explanation of *why* the shape is what
it is. Two caveats on reading it: it is **from 2019**, so the output mechanism it describes is the
deprecated `::set-output::` workflow command, replaced by appending to the `$GITHUB_OUTPUT` file —
`::set-output::` no longer works. Take the concepts from the post and the mechanics from the
official template.

The two mechanics worth internalising, because they are the whole interface:

- **Inputs arrive as environment variables.** An input named `my-input` in `action.yml` becomes
  `INPUT_MY-INPUT` — uppercased, with spaces converted to underscores. Python reads it with
  `os.environ`. There is no library involved.
- **Outputs are written to a file.** Append `name=value` to the path in `$GITHUB_OUTPUT`. Multiline
  values need the heredoc delimiter syntax, which is the usual place this goes wrong.

The recurring failure with container actions is the one to plan for up front: **if `action.yml`
points at a local `Dockerfile`, the runner builds the image on every single job.** For anything
called more than occasionally, publish the image to a registry, reference it as
`docker://ghcr.io/org/image@sha256:...`, and pin it by digest. That converts a per-job build into a
per-job pull, and pins what actually runs.

**Nothing is built in this folder** — no `action.yml`, no `Dockerfile`. It is a mapped path with
the reference implementations recorded.

---

[← GitHub Actions](../README.md)
