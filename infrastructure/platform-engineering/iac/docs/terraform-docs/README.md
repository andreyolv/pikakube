[← IaC documentation](../README.md)

# terraform-docs

<https://github.com/terraform-docs/terraform-docs>
<https://github.com/terraform-docs/gh-actions>

---

## The problem it solves

A Terraform module already declares everything mechanical about itself: `variable` blocks with
types, defaults and descriptions, `output` blocks, `required_version`, `required_providers`, and the
resources it creates. A README that restates all of that by hand is a manual copy of a
machine-readable source, and it is wrong the first time somebody adds a variable.

terraform-docs parses the module and generates that section: **inputs, outputs, providers,
requirements, resources and nested modules**. It runs against a directory of `.tf` files, needs no
credentials, no state and no initialised backend.

The feature that matters most is **injection**. Given marker comments in an existing README,
terraform-docs replaces only the text between them and leaves the rest of the file alone. That is
what stops this being a trade between "documentation that explains the module" and "documentation
that is accurate" — the explanation is written by a person above the markers, the interface table is
rewritten by the tool between them, and both are in one file.

It emits several formats from the same parse, which is what makes it useful beyond a README:

| Format | Used for |
|---|---|
| Markdown table | the common case — a compact inputs/outputs table injected into a README |
| Markdown document | longer prose-style sections rather than a table, for modules with many inputs |
| **JSON / YAML** | machine consumption — a module catalogue, a docs site, a self-service portal |
| Others, including plaintext and tfvars output | pipelines that want the interface in some other shape |

Behaviour is configured through a **`.terraform-docs.yml`** checked into the repository, so the same
output is produced by a laptop, a pre-commit hook and CI. Passing the options as CLI flags in CI only
is the usual reason a repository ends up with a check that fails on formatting nobody can reproduce.

## When to use it

- **any Terraform or OpenTofu module intended to be consumed by someone else** — that is the whole
  case, and it applies from the first shared module
- in a **pre-commit hook**, so the file is regenerated as part of the change that made it stale
- in **CI, as a check that fails when the committed documentation differs from a fresh
  generation**. This is the step that converts a habit into a guarantee: stale docs stop being
  something to notice and become something that cannot merge
- in a monorepo of many modules, where hand-maintaining N interface tables is not a task anyone will
  keep doing
- when the module interface needs to feed something other than a README — the JSON and YAML output
  makes a module catalogue possible without a second parser

## When not to use it

- as the whole documentation. It produces the interface; the reason the module exists is still prose
  somebody has to write. See [`../README.md`](../README.md#the-intent-is-not)
- as a substitute for writing `description` on every variable and output. The generator copies those
  fields; if they are empty, the result is a table of names and types that answers nothing
- as a correctness or policy check — it parses and prints, it does not validate. That is
  [`lint/`](../../lint/README.md), and security scanning is a different discipline again
- on Pulumi or CDK — this is an HCL tool, the same scope boundary
  [TFLint](../../lint/tflint/README.md) has
- in a CI job that regenerates and **commits** the result. That makes the pull request contain
  changes its author did not write, and review happens against a file that moves under it. Fail the
  build and let the author regenerate

## Notes

Three things decide whether this works in practice, and none of them is the tool itself.

**Commit the configuration.** `.terraform-docs.yml` fixes the format, the sections, the sort order
and the output file. Without it, everyone's local run produces a slightly different file and the CI
check becomes noise that gets disabled.

**Choose the mode deliberately.** Injecting into an existing README preserves human prose; replacing
the file does not. For a module README the answer is nearly always injection. For a generated
artefact consumed by another system — a catalogue, a docs site — writing the whole file in JSON or
YAML is the right call, and there is no prose to lose.

**Run it in two places.** The pre-commit hook is for speed of feedback and is trivially skippable;
the CI check is the enforcement. This is the same split
[`lint/`](../../lint/README.md) makes about linters, and for the same reason — only the CI run
cannot be bypassed by someone in a hurry.

**The official action is `terraform-docs/gh-actions`, and its default mode is the one this page
argues against.** It can run in two shapes, and the choice is the whole decision:

| Mode | What happens | Verdict |
|---|---|---|
| `git-push: true` | it regenerates and **commits back** to the branch | this is the pattern rejected in [*When not to use it*](#when-not-to-use-it) — the pull request gains changes its author did not write, and review happens against a file that moves |
| `fail-on-diff: true` | it regenerates in place and **fails if the result differs** from what is committed | the enforcement this page asks for: the author regenerates, the diff stays theirs |

Both exist because both are wanted by somebody, and the auto-commit path is genuinely convenient on
a repository nobody reviews closely. It is still the wrong default: a bot commit on a branch
invalidates approvals, races with the author's own pushes, and needs write permission on a workflow
that otherwise needs none. Prefer `fail-on-diff`, keep the action's own `working-dir`,
`config-file` and `recursive` inputs aligned with the committed `.terraform-docs.yml` so a local run
produces the same bytes, and pin the action to a commit SHA like any third-party action
([GitHub Actions §8](../../../../devops/cicd/github-actions/README.md#8-anti-patterns)).

The honest limitation, stated plainly because it is the one that gets misunderstood: **terraform-docs
documents the interface, not the intent.** It can tell a reader that an input is called
`enable_private_endpoint`, that it is a `bool`, and that it defaults to `false`. It can never tell
them why the module exists, which of the twenty inputs are the three that matter, what must already
exist before it is called, or when to use a different module entirely. That prose is still yours to
write — and the generated table belongs inside it, not instead of it.

For this repository there is currently nothing to run it against:
[`engine/`](../../engine/README.md) contains no HCL and the only `.tf` file is the empty
`tf-codes/main.tf` under [tf-controller](../../../gitops/flux/tf-controller/README.md). Recorded as
the tool to adopt with the first module, rather than after several of them have grown README tables
nobody trusts.

---

[← IaC documentation](../README.md)
