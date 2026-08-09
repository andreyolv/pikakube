[← SAST](../README.md)

# CodeQL

<https://github.com/github/codeql>
<https://github.com/github/codeql-action>

---

## The problem it solves

CodeQL is not a pattern matcher. It **compiles your code into a relational database** and lets
you write queries against it. The database contains the abstract syntax tree, the control-flow
graph, the data-flow graph and the type information — so a query can ask questions no pattern
matcher can answer:

> "Is there a path along which data from an HTTP request parameter reaches a SQL execution call,
> through any number of function calls, across files, without passing through a sanitiser?"

That is **taint tracking**, and it is the reason CodeQL findings have a materially lower false
positive rate than pattern-based SAST. The tool has computed reachability rather than guessing at
it.

The queries are written in QL, a declarative logic language:

| Component | Role |
|---|---|
| Sources | where untrusted data enters — request parameters, file reads, environment |
| Sinks | dangerous operations — SQL execution, command execution, file paths |
| Sanitisers | operations that make tainted data safe |
| The query | asks whether a path exists from source to sink avoiding sanitisers |

Delivery: `codeql` CLI for local and self-hosted use, and `codeql-action` for GitHub Actions,
which uploads results to GitHub code scanning where they appear in the security tab and on pull
requests.

The cost is real and unavoidable: **it must build your code** (for compiled languages) and then
analyse the database. Minutes at best, tens of minutes on a large repository.

## When to use it

- **Security-critical services** where a missed injection matters more than an hour of CI time
- **Public repositories on GitHub**, where it is free and fully integrated — one workflow file,
  results in the security tab, no new system to operate. If the repository is public this is
  close to a free win
- **Scheduled scans**, nightly or weekly, rather than on every commit. This is the placement that
  makes the runtime acceptable
- **Compiled languages** — Java, C#, C/C++, Go. The database model is strongest where type
  information is richest
- **Deep, specific questions.** If you need to ask "does any code path let a tenant id from the
  request reach a query without the tenant filter", QL can express that and nothing else in this
  folder can
- **Variant analysis after an incident.** Given one known vulnerability, write a query for its
  shape and find every other instance in the codebase. This is arguably CodeQL's best use and it
  is under-exploited

## When not to use it

- **As a per-commit gate.** Build plus analysis is too slow; developers will route around it
- **Interpreted, dynamically typed code at scale.** Python, JavaScript and Ruby are supported, but
  the analysis is weaker where types are not available, and the runtime cost stays high
- **Outside GitHub, without checking the licence.** The CodeQL CLI and queries are free for
  analysing open-source code, and for private code the terms are tied to GitHub Advanced
  Security. Using it against a private codebase in non-GitHub CI is a licensing question before
  it is a technical one
- **When you need custom rules quickly.** Writing QL is a genuine skill; writing a Semgrep rule
  is an afternoon. If custom rules are the requirement, [`../semgrep/README.md`](../semgrep/README.md)
- **On a small repository with little first-party code.** The setup and runtime are
  disproportionate to what there is to find

## Notes

Original notes recorded for this tool:

- <https://github.com/github/codeql> — the open-source QL standard libraries and the query packs.
  This is where the actual security queries live, per language, along with their documentation
  and the `qhelp` files explaining what each query looks for and why. Reading the query pack for
  your language tells you exactly what coverage you are getting — far more informative than a
  marketing list of CWE numbers.
- <https://github.com/github/codeql-action> — the GitHub Action. Handles database creation
  (`init`), the build (`autobuild` or your own build steps), and `analyze`, which uploads SARIF
  into GitHub code scanning. The autobuild step is where most setup failures happen on compiled
  languages; supplying explicit build commands is the usual fix.

Two things worth recording alongside:

- **The engine itself is not open source**, even though the queries and libraries are. That is a
  meaningful distinction if the requirement is a fully auditable toolchain.
- **Variant analysis is the underused capability.** After any security incident, the highest-value
  follow-up is a query that finds every other occurrence of the same mistake. That is a task
  CodeQL is uniquely good at and it is rarely done.

---

[← SAST](../README.md)
