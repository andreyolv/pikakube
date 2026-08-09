[← SAST](../README.md)

# Bandit

<https://github.com/PyCQA/bandit>

---

## The problem it solves

Bandit is a SAST tool that does one thing: find common security problems in **Python**. It parses
each file to an AST and runs a set of plugins against it, each corresponding to a numbered check
(`B101`, `B602`, …).

What it knows about is specifically Python's set of footguns:

| Check family | Examples |
|---|---|
| `B1xx` — general | `assert` used for validation (stripped under `python -O`), `exec`, bad exception handling |
| `B2xx` — application | Flask running with `debug=True` |
| `B3xx` — blacklisted calls | `pickle`, `marshal`, `yaml.load` without a safe loader, `hashlib.md5`, `random` for security, `xml` parsers vulnerable to XXE |
| `B4xx` — imports | importing known-dangerous modules — `telnetlib`, `ftplib`, `subprocess` |
| `B5xx` — crypto and TLS | weak key sizes, `verify=False` in requests, weak ciphers |
| `B6xx` — injection | `subprocess` with `shell=True`, `os.system`, SQL built by string formatting |
| `B7xx` — templates | Jinja2 with autoescape disabled |

Its virtues are the ones you want from a linter: it is fast, needs no build, has no services, and
drops into an existing Python tooling setup in one line. It is maintained by **PyCQA**, the same
group behind flake8, pylint and isort — so it belongs to the ecosystem rather than sitting
alongside it, and it is available as a pre-commit hook and as a `ruff` rule set (`ruff`
reimplements many bandit checks under the `S` prefix).

## When to use it

- **A Python codebase.** If the repository is mostly Python, this is the cheapest security check
  available and there is little reason not to run it
- **In pre-commit, next to the formatters and linters.** Findings arrive at the moment they are
  cheapest to fix, and it is the same place developers already see lint output
- **Alongside a general tool rather than instead of it.** Bandit's checks are idiomatic Python
  knowledge; Semgrep's are broader and customisable. Running both is normal and cheap
- **When `ruff` is already in use** — its `S` rules are bandit's checks, so you may already have
  most of this without a second tool. Worth checking before adding one

## When not to use it

- **A polyglot repository.** One tool per language does not scale; Semgrep covers all of them
  with one configuration — [`../semgrep/README.md`](../semgrep/README.md)
- **Expecting dataflow analysis.** Bandit is AST pattern matching per file. It flags
  `subprocess(..., shell=True)` whether or not the argument is attacker-controlled, and it cannot
  tell you the difference
- **Expecting it to cover dependencies.** Bandit reads your Python; a vulnerable version of
  `requests` is invisible to it. That is [`../../sca/pip-audit/README.md`](../../sca/pip-audit/README.md)
- **Without tuning.** `B101` (`assert` used) fires on every test file and is the classic reason
  teams abandon it on day one. Exclude test directories, or skip the check, immediately

## Notes

Original note recorded for this tool:

- <https://github.com/PyCQA/bandit> — the upstream project, under the Python Code Quality
  Authority. The repository documents every numbered check with an explanation of the risk and
  the recommended alternative, plus the configuration surface: `.bandit` / `pyproject.toml`
  settings, `--skip` and `--exclude`, severity and confidence filtering (`-ll`, `-ii`), the
  `# nosec` inline suppression comment, and the pre-commit hook.

Two configuration points that decide whether it is kept:

- **Exclude tests.** `assert` is correct in a test and a finding everywhere else. Without
  `--exclude tests/` or skipping `B101`, the first run is almost entirely noise from test files.
- **Filter by confidence as well as severity.** Bandit reports both, and filtering on
  `--severity-level medium --confidence-level medium` is a far better starting point than taking
  everything.

`# nosec` suppressions should carry the check id and a reason (`# nosec B602 — argument is a
fixed constant`); a bare `# nosec` is unreviewable and permanent.

---

[← SAST](../README.md)
