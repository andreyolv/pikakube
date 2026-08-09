[← Manifest scanners](../README.md)

# yamllint

<https://github.com/adrienverge/yamllint>

---

## The problem it solves

Before a manifest can be wrong about Kubernetes, it can be wrong about YAML — and YAML has more ways
to be quietly wrong than any other configuration format in common use:

| Trap | What actually happens |
|---|---|
| **Duplicate keys** | the last one silently wins; the first is discarded without a warning |
| **The Norway problem** | `no`, `on`, `off`, `yes` parse as booleans, not strings |
| **Version numbers** | `1.10` is a float and becomes `1.1` |
| **Mixed indentation** | a block ends up nested somewhere unintended, and is still valid |
| **Tabs** | not permitted in YAML indentation, and the error message is unhelpful |
| **Trailing whitespace, missing newlines** | harmless, but noise in every diff forever |

yamllint is a pure YAML linter. It knows nothing about Kubernetes and does not need to — it checks
syntax, indentation, key duplication, line length, quoting, truthy values and document structure,
with every rule individually configurable through `.yamllint`.

Duplicate keys are the one that justifies it on its own. A ConfigMap with the same key twice applies
cleanly, runs with the wrong value, and looks correct in the file to anyone reading quickly.

## When to use it

- **on every YAML file in the repository, in CI** — manifests, CI definitions, Helm values,
  Ansible playbooks, anything
- as the **first** check in a validation chain, because a YAML parse error makes every subsequent
  tool produce a confusing message about something unrelated
- to settle formatting arguments mechanically: line length, quoting style and indentation become a
  configuration file rather than review comments

## When not to use it

- **as evidence that a manifest is correct.** yamllint's approval means the file is well-formed
  YAML, nothing more. `kind: Deploymnet` passes cleanly
- on Helm templates, which are Go templates and not YAML until rendered. Lint the values files and
  the rendered output; linting the templates produces nonsense
- with the default rule set, unquestioned. The default 80-character line limit fails on almost every
  real manifest — the first thing to do is configure it rather than let the tool be dismissed as
  noisy

## Notes

The only recorded reference is the repository: <https://github.com/adrienverge/yamllint>.

Nothing is deployed for it; it is a CLI, and it also has a pre-commit hook, which is where it gives
the fastest feedback — a formatting complaint is much better received before the commit than in a
pipeline.

It is **layer one** of the three described in [`../README.md`](../README.md), and the layer people
skip because it feels trivial. The order matters more than it looks: an unparseable file makes
[kubeconform](../kubeconform/README.md) and [kube-score](../kube-score/README.md) report something
misleading about the wrong part of the document, and the ten minutes lost to that is exactly what
running yamllint first prevents.

---

[← Manifest scanners](../README.md)
