[← GitHub Actions](../README.md)

# actionlint

<https://github.com/rhysd/actionlint>

---

## The problem it solves

GitHub Actions YAML is **interpreted by a server you do not control**, and it is never validated
until a runner picks the job up. A misspelled context field, an invalid `runs-on`, a type error in
an expression — all of them are discovered after a commit, a push, a queue wait and a runner
start. The workflow file is the one part of the repository with no compiler.

`actionlint` is that compiler. It is a single Go binary that reads workflow files and reports what
is wrong before anything is pushed:

| Check | What it catches |
|---|---|
| Workflow schema | keys that do not exist, values of the wrong type |
| `${{ }}` expressions | undefined contexts, wrong property names, type mismatches |
| `runs-on` labels | runner labels GitHub does not know about |
| Action inputs | required inputs missing, unknown inputs passed |
| **Shell scripts** in `run:` | delegates to **shellcheck** — quoting bugs, unset variables |
| **Embedded Python** | delegates to **pyflakes** |
| `needs:` graph | references to jobs that do not exist, and cycles |
| Glob and cron syntax | patterns that never match, invalid schedules |
| Security-adjacent | untrusted input interpolated directly into `run:` — script injection |

The two delegated checks are the part people underestimate. Most real CI bugs are not in the YAML,
they are in the shell inside the YAML — an unquoted variable, a pipeline whose exit status is
silently discarded. `actionlint` finds those because it hands the script to shellcheck.

## When to use it

- **Always, on any repository with workflows.** It is one binary, no configuration, and there is
  no argument against it
- In **pre-commit**, so the error appears before the commit rather than after the push
- In CI itself, as a gate on changes under `.github/workflows/`
- In the editor, via its language-server integrations, for immediate feedback
- Especially with **matrices and expressions**, where a wrong context property is easy to write
  and invisible until runtime

## When not to use it

- As a substitute for actually running the workflow. It validates **structure and expressions**,
  not behaviour — a workflow can be perfectly valid and completely wrong. That is
  [`act`](../act/README.md)'s job
- As a security scanner. It flags obvious script-injection shapes; it is not a supply-chain tool
  and will not tell you a pinned action is malicious
- On workflow *generators*. If the YAML is produced by another tool, lint the output, not the
  source
- If the pipeline is not GitHub Actions YAML at all. With [Dagger](../../dagger/README.md) the
  pipeline is a program and the language's own type checker replaces this entirely

## Notes

<https://github.com/rhysd/actionlint> — a single recorded link, and the tool needs no more than
that. It is a self-contained Go binary with no runtime dependencies, distributed as a release
binary, a Docker image, a pre-commit hook and a GitHub Action.

The point worth extracting, given how minimal the note is: **`actionlint` and
[`act`](../act/README.md) are two halves of the same fix.** GitHub Actions' central weakness is
that the only way to test a workflow is to push it. `actionlint` removes the class of failures
that are statically detectable — the typos, the wrong contexts, the bad expressions — which is
most of them. `act` removes the class that requires execution. Running both locally turns a
push-and-wait loop into a local one, and the combined cost is two binaries.

Its highest-value single feature in this repository's context is the **shellcheck delegation**.
The reusable workflow in [`workflows/`](../workflows/README.md) contains `run:` blocks, and any
`run:` block is a shell script that nothing else in the toolchain examines. Every quoting and
exit-status bug in CI lives there.

The practical placement: as a **pre-commit hook**, so a broken expression never reaches a branch.
Running it only in CI means it still costs a push to find out — which is the exact problem it
exists to solve.

---

[← GitHub Actions](../README.md)
