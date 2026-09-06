[← Admission policies](../README.md)

# Regal

<https://github.com/open-policy-agent/regal>

---

## The problem it solves

[The language question](../README.md#5-the-language-question) in this folder makes the honest
point about Rego: it is powerful and it is a learning curve. It is a declarative logic language,
and the mistakes people make while learning it are not syntax errors — they are rules that
compile, run, and quietly never match.

Regal is a **linter for Rego**. It catches the class of bug that the compiler cannot:

| Category | Example of what it flags |
|---|---|
| Bugs | a rule that can never evaluate to true; a variable assigned and never used |
| Idiomatic | `count(x) == 0` where `x == set()` says it better |
| Style | naming, imports, unused arguments, file organisation |
| Performance | patterns that force full iteration where indexing was possible |
| Testing | test files without assertions, or policies with no tests at all |

Its own rules are written in Rego, which is the detail that makes custom rules practical: an
organisation's Rego conventions become lint rules in the same language the policies are written
in, not a plugin in another one.

## The other half: the language server

Less advertised and arguably more valuable day to day. Regal ships a **language server**, which
is what provides Rego completion, hover documentation, go-to-definition and inline diagnostics
in editors.

That changes who can write policy. The argument against Rego in
[`../README.md`](../README.md#5-the-language-question) is that whoever cannot write a policy will
not own one — and a large part of "cannot write" is writing it in a plain text editor with no
feedback until evaluation. Diagnostics as you type is a real answer to that.

## Where it fits in the policy story

[`conftest/`](../conftest/README.md) makes the case for running the same Rego in CI that
[Gatekeeper](../gatekeeper/README.md) enforces at admission. Regal is the step before that one:

```
write Rego → regal lint (editor + CI) → conftest test (CI) → Gatekeeper (admission)
```

Each stage catches something the next cannot. Regal never evaluates a policy against a manifest —
it reads the policy itself — so it finds the rule that is wrong regardless of input, which is
exactly the failure that testing against sample manifests misses.

```bash
regal lint policy/
regal lint --format github policy/       # annotations on a pull request
regal test policy/                        # wraps `opa test` with the same config
```

Configuration lives in `.regal/config.yaml`: rule levels per category, ignore patterns, and
custom rules. Inline `# regal ignore:rule-name` handles the one-off exception.

## When to use it

- **Rego is written here at all** — Gatekeeper `ConstraintTemplate`s, conftest policies, or OPA
  outside the cluster. The cost of adopting it is a CI step and an editor extension
- the team is learning Rego, which is when the idiomatic and bug rules pay the most
- policy is shared across repositories and needs conventions somebody enforces

## When not to use it

- **there is no Rego.** On a platform standardised on [Kyverno](../kyverno/README.md) the policies
  are YAML, and this tool has nothing to read
- policy is a handful of copy-pasted `ConstraintTemplate`s that nobody edits — the linter's value
  scales with how much Rego is actually authored

## Notes

An Open Policy Agent project (originally from Styra), Apache 2.0, and the de facto linter for the
language. Nothing to deploy — it is a CLI and a language server, not a cluster component. It sits
in this folder for the same reason [conftest](../conftest/README.md) does: its relationship to the
Rego half of the policy story.

**Where this lands for pikakube.** Kyverno is what is wired up here, and Kyverno policies are
YAML — so Regal has nothing to lint today. It becomes relevant in the one case the
[Gatekeeper folder](../gatekeeper/README.md) is being kept for: if Rego ever enters the picture,
whether through Gatekeeper, conftest over Terraform and Dockerfiles, or OPA outside Kubernetes.

Worth recording now for a specific reason. The recurring argument against Rego in this repository
is the learning curve, and the two things that most reduce it — a linter that explains idiomatic
form, and editor diagnostics — are both this tool. That is a fact worth having on hand when the
Kyverno-versus-Gatekeeper question is reopened, rather than discovered afterwards.

---

[← Admission policies](../README.md)
