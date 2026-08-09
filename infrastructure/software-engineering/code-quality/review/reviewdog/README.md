[← Review](../README.md)

# reviewdog

<https://github.com/reviewdog/reviewdog>

---

## The problem it solves

A linter in CI produces a log. The log lists findings by file and line. The pull request being
reviewed is somewhere else entirely, and connecting one to the other means opening the job output,
reading a path, and scrolling to it.

reviewdog is the pipe between the two. It reads the output of **any** linter — through
`errorformat`, checkstyle XML, SARIF or its own `rdjson` — and posts the findings as review
comments on the pull request, on the exact lines they concern.

The second thing it does is the more valuable one: **it filters findings to the diff.** Only
problems on lines the change actually touched are reported. That single behaviour is what makes it
possible to introduce a linter to an existing codebase, because the alternative — a first run
reporting four thousand pre-existing findings — is the reason most such attempts are abandoned.

It runs no analysis itself. It has no rules, no language support and no opinions; it is plumbing
for tools that do.

## When to use it

- **As soon as there is any linter in CI.** The cost of adding it is one step; the benefit is that
  findings appear where the code is being read.
- When introducing a linter or a stricter rule set to a codebase that predates it. Report on new
  code only, and the backlog stops being a blocker.
- To surface findings from tools that have no forge integration of their own — shell linters,
  `yamllint`, custom scripts, anything that emits file, line and message.
- When an LLM reviewer is not acceptable — no model, no data leaving the network, no per-review
  cost.

Reporter modes worth knowing before wiring it up:

| Reporter | Behaviour |
|---|---|
| `github-pr-review` | comments on the diff; needs a token with write access |
| `github-pr-check` | a check run with annotations; does not clutter the comment thread |
| `local` | prints filtered findings; useful for testing the setup |

`github-pr-check` is the better default for a noisy linter: annotations do not send notifications
and do not accumulate in the conversation.

## When not to use it

- As a **substitute for failing the build**. Comments are advisory by design. If a finding must
  block, the linter's own exit code has to gate the pipeline; reviewdog changes where findings are
  displayed, not whether they matter.
- As a **replacement for a linter**. It analyses nothing. Without a tool feeding it, it does
  nothing at all.
- Where a hosted forge integration already does the same job better — SonarQube's pull request
  decoration, for example, already annotates the diff, and running both produces duplicate
  comments.
- With an unfiltered, very noisy tool. Diff filtering helps, but a rule set that fires on every
  third line will still bury the review.

## Notes

The original note for this folder records only the upstream repository:

- <https://github.com/reviewdog/reviewdog>

Nothing is deployed and nothing is configured. reviewdog is a CI concern — a binary or a GitHub
Action in a pipeline — and has no Kubernetes surface.

Two points to carry into the eventual setup:

| Point | Detail |
|---|---|
| It needs a linter first | there is currently none in this repository's CI — see [`../../lint/`](../../lint/README.md); the two are one piece of work |
| Token permissions | posting review comments requires write access to pull requests, which is a deliberate grant, not a default |

---

[← Review](../README.md)
