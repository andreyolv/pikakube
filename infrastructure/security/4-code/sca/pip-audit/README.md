[← SCA](../README.md)

# pip-audit

<https://github.com/pypa/pip-audit>
<https://github.com/pypa/advisory-database>

---

## The problem it solves

pip-audit is the **Python ecosystem's own** vulnerability scanner, maintained by PyPA — the same
group responsible for pip, setuptools and PyPI itself. That provenance is the main reason to use
it: it understands Python packaging as Python packaging actually works, rather than through a
generic model.

```bash
# audit the current environment
pip-audit

# audit a requirements file
pip-audit -r requirements.txt

# apply the fixes it can apply
pip-audit --fix
```

What it gets right that generic tools do not:

| Detail | Why it matters |
|---|---|
| Resolves requirements the way pip does | including extras, markers and version specifiers, so the set audited is the set installed |
| Audits a **live environment**, not just a file | catches what is actually installed, including things installed outside the requirements file |
| Understands the PyPA advisory database natively | curated by the ecosystem's maintainers, with accurate version ranges |
| Queries **OSV** as well | so coverage is not limited to one source |
| `--fix` | it will upgrade the affected packages for the simple cases |
| Reads SBOMs and emits CycloneDX | fits into an SBOM-based workflow |

The complementary link recorded here — the **PyPA advisory database** — is the data behind it: an
open, Git-based repository of Python advisories in OSV format, which is also one of the sources
OSV aggregates. Understanding that the two links are *client* and *data* explains why pip-audit
and [`../osv-scanner/README.md`](../osv-scanner/README.md) largely agree with each other.

## When to use it

- **Python repositories.** It is the native tool, it is fast, and adding it to CI is one line
- **Auditing a live environment**, which is the capability generic lockfile scanners lack — useful
  for a running container, a virtualenv on a build host, or a notebook environment
- **In pre-commit or a local developer workflow**, where `--fix` makes the remediation immediate
- **Alongside Renovate.** pip-audit finds it; [`../../dependency/README.md`](../../dependency/README.md)
  keeps it from happening again
- **When you want the ecosystem's own answer**, e.g. to check a generic scanner's finding

## When not to use it

- **A polyglot repository.** One tool per language does not scale;
  [`../osv-scanner/README.md`](../osv-scanner/README.md) covers Python and everything else with
  one binary and the same underlying data
- **Expecting reachability.** It reports that a vulnerable version is installed, not whether the
  vulnerable code is called
- **Expecting it to find problems in your code.** That is [`../../sast/bandit/README.md`](../../sast/bandit/README.md)
- **Without a pinned dependency set.** Auditing loose requirements with open ranges tells you
  about a resolution that may not be what production installed. Pin, or audit the environment
- **`--fix` unattended.** It upgrades packages; upgrades break things. It is a convenience for a
  developer, not a CI automation — that is Renovate's job, with tests attached

## Notes

Original notes recorded for this tool:

- <https://github.com/pypa/pip-audit> — the tool itself, from PyPA. The repository documents the
  input modes (environment, requirements file, `pyproject.toml`, SBOM), the vulnerability service
  options (`--vulnerability-service osv|pypi`), `--fix` and `--dry-run`, the ignore mechanism
  (`--ignore-vuln`), and output formats including CycloneDX and Markdown.
- <https://github.com/pypa/advisory-database> — the **PyPA Advisory Database**: the curated set of
  Python advisories, stored as OSV-format YAML in Git. This is the data source, and it is worth
  knowing separately for two reasons. First, it is how you check whether a specific package
  version is really affected — the advisory records the exact ranges. Second, it is where you
  contribute a correction if an advisory's range is wrong, which happens and is worth fixing at
  source rather than suppressing locally.

One practical note: pip-audit audits **installed distributions**, so it sees what pip resolved. If
your project uses Poetry or uv with a lockfile, either audit the installed environment or export
to a requirements file first — auditing a `pyproject.toml` with open ranges is the least precise
of the available options.

---

[← SCA](../README.md)
