[← Secret scanning](../README.md)

# git-secrets

<https://github.com/awslabs/git-secrets>

---

## The problem it solves

git-secrets is where this whole category started. It is a set of shell scripts from AWS Labs that
installs Git hooks — `pre-commit`, `commit-msg` and `prepare-commit-msg` — and refuses the commit
when a configured pattern matches:

```bash
# install the hooks into the current repository
git secrets --install

# add the AWS credential patterns
git secrets --register-aws

# scan the existing history
git secrets --scan-history
```

Its focus is **AWS**: `--register-aws` adds patterns for access key ids, secret access keys and
account identifiers. Custom patterns can be added, but the AWS case is what it was built for and
what it does well.

The idea it established remains the correct one, and it is why the tool is still worth
understanding: **the only place a secret can still be un-leaked is before the commit exists.**
Everything else in [`../README.md`](../README.md) is detection after the fact.

Its virtues are simplicity — shell scripts, no runtime, no dependencies, works anywhere Git and
bash work.

## When to use it

- **An AWS-centric environment where the simplest possible thing is wanted**, and the toolchain
  cannot install a Go binary
- **As a historical reference.** Understanding the pre-commit hook pattern is easier from a
  hundred lines of shell than from a modern scanner
- **A legacy setup that already uses it.** If it is installed and working, there is no urgency to
  replace it — but do not extend it

## When not to use it

- **New adoptions, essentially.** This is the honest recommendation. Take the limitations
  together:

  | Limitation | Consequence |
  |---|---|
  | **Effectively unmaintained** | the repository has seen very little activity for years. New credential formats — GitHub's `ghp_`/`gho_` prefixes, modern cloud tokens, provider-specific keys — are not covered unless you write the patterns yourself |
  | AWS-focused by design | it covers one provider well and everything else not at all |
  | Regex only | no entropy detection, no verification |
  | Shell scripts | slower than a compiled scanner on large repositories, and portability quirks on macOS vs Linux `grep` are a recurring annoyance |
  | Hooks only, locally | trivially bypassed with `--no-verify`, and no CI story of its own |

- **As your only control.** It is a local hook. It stops nothing that arrives by any other route
- **When you want a maintained rule set.** [`../gitleaks/README.md`](../gitleaks/README.md) has
  150+ maintained patterns and the same pre-commit placement, in a single binary
- **When you need to know whether a finding is live** — [`../trufflehog/README.md`](../trufflehog/README.md)

## Notes

Original note recorded for this tool:

- <https://github.com/awslabs/git-secrets> — the upstream project under the `awslabs`
  organisation. The repository documents `--install`, `--register-aws`, `--add` for custom
  patterns, `--add-allowed` for allowlist patterns, `--scan` and `--scan-history`, and the
  installation of hooks into `git init` templates so that new repositories get them
  automatically.

Two things worth recording explicitly, because they are the reason this page ends where it does:

- **Check the repository's activity before adopting it.** As an `awslabs` project it is
  demonstration-quality code that was widely adopted; it has not kept pace with the credential
  formats that have appeared since. An unmaintained pattern list is a scanner that quietly stops
  covering new things.
- **The idea outlived the implementation.** The `git init` template trick — installing hooks so
  every newly created repository has them by default — is genuinely good and worth reproducing
  with a modern scanner. `pre-commit` with gitleaks does the same job with a maintained rule set.

---

[← Secret scanning](../README.md)
