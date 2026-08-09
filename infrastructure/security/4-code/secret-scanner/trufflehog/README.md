[← Secret scanning](../README.md)

# TruffleHog

<https://github.com/trufflesecurity/trufflehog>

---

## The problem it solves

Every secret scanner produces candidates. TruffleHog's distinguishing feature is that it then
**checks whether they work**.

For hundreds of providers it has a *detector* that knows both the credential's shape and the API
call that validates it. A candidate AWS key is used against STS; a candidate GitHub token against
the GitHub API; a candidate Slack token against Slack. The result splits the output into two
categories that require completely different responses:

| Result | Meaning | Response |
|---|---|---|
| **Verified** | the credential is live, right now | an incident. Rotate immediately |
| Unverified | it matched a pattern but did not authenticate | triage — expired, revoked, a test fixture, or a false positive |

This changes the economics of a first scan entirely. Without verification, a full-history scan of
an old repository returns hundreds of candidates and someone has to guess. With it, you get a
short list of things that are genuinely on fire.

```bash
# scan a whole repository's history, reporting only live credentials
trufflehog git file://. --only-verified

# scan a GitHub organisation, including all repositories
trufflehog github --org=myorg --only-verified
```

It also scans far more than Git: filesystems, S3 buckets, GCS, container images, Docker, Postman
collections, Jira, Slack, CI logs. Secrets do not only live in repositories, and this is one of
the few tools that acts on that.

## When to use it

- **The initial full-history audit.** This is the strongest case in the whole folder: run it once
  across every repository, with `--only-verified`, and rotate what it finds. That single exercise
  usually finds the material that matters
- **Incident response.** A credential has been found somewhere — is it still valid, and where else
  does it appear
- **Scanning beyond Git** — buckets, images, logs, chat exports. The credential leaked into a CI
  log is invisible to a repository scanner
- **Organisation-wide sweeps**, including repositories nobody has looked at in years
- **Deciding what to prioritise.** Verification is the only triage mechanism that is not a guess

## When not to use it

- **Where candidate secrets must not leave the network.** Verification means **sending the
  candidate credential to a third-party API**. In most cases this is benign — the credential
  either works or it does not, and if it works you had a much bigger problem already. In a
  regulated or air-gapped environment it may be unacceptable. `--no-verification` disables it, at
  which point [`../gitleaks/README.md`](../gitleaks/README.md) is the simpler choice
- **As the fast pre-commit hook.** It is heavier than gitleaks and verification needs network
  access; blocking a commit on a network round-trip is not a good developer experience
- **When network access is unavailable in CI** — verification silently degrades to pattern
  matching, and you have the heavier tool without its advantage
- **Expecting it to prevent anything.** Like every scanner, it finds what has already happened.
  Prevention is [`../README.md`](../README.md) section 5

## Notes

Original note recorded for this tool:

- <https://github.com/trufflesecurity/trufflehog> — the upstream project from Truffle Security.
  The repository documents the sources it can scan (`git`, `github`, `gitlab`, `filesystem`, `s3`,
  `gcs`, `docker`, `postman`, and more), the detector list, `--only-verified`,
  `--no-verification`, the `--since-commit` flag for incremental scanning, the pre-commit hook and
  the GitHub Action.

Two points worth recording:

- **v3 was a rewrite.** Older documentation and blog posts describe the original Python tool,
  which was entropy-based and had no verification. The current tool is Go and detector-based.
  Check which version an article refers to before following it.
- **Verification is the whole argument for choosing it**, so be deliberate about the trade-off it
  implies. Running it means candidate credentials are transmitted to the providers they appear to
  belong to. That is usually the right call, and it is a decision someone should make knowingly
  rather than discover afterwards.

The natural pairing, from [`../README.md`](../README.md): **TruffleHog for the one-off audit and
for verification, gitleaks for the continuous pre-commit and CI scanning.**

---

[← Secret scanning](../README.md)
