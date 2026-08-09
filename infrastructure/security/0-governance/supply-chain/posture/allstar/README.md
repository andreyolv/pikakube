[← Posture](../README.md)

# Allstar

<https://github.com/ossf/allstar>

---

## The problem it solves

[Scorecard](../scorecard/README.md) answers "does this repository have good practices?" and produces
a number. It is a report. Somebody has to read it, decide, and go and change a setting — and then
somebody has to notice six weeks later when branch protection is switched off for an afternoon to
land a hotfix and never switched back on.

Allstar closes that loop. It is a **GitHub App from OpenSSF that continuously enforces policy on
repositories**: it watches the settings, and when a repository is out of compliance it acts.

The relationship is worth stating as plainly as possible, because it is the reason this page sits
next to the other one:

> **Scorecard rates. Allstar enforces.**

Same organisation, same body of practice, two halves of one job. Scorecard runs and tells you the
state of things; Allstar watches and does something about it. Adopting the first without the second
is how a repository gets a good score in March and a bad configuration in June, with nothing in
between to say so.

The policies it ships cover repository configuration rather than code:

| Policy | What it is looking for |
|---|---|
| **Branch protection** | required reviews, status checks, no force-push to the default branch |
| **Binary artifacts** | compiled binaries committed to the repository — unreviewable, and a classic malware path |
| **Outside collaborators** | non-members holding admin or push access |
| **Dangerous workflows** | GitHub Actions patterns that let untrusted input reach a privileged context |
| **Security policy** | the presence of a `SECURITY.md` |
| Others, including administrator access and action pinning | the same shape: a setting that should be true, checked continuously |

## When to use it

- when Scorecard findings keep reappearing. Recurring findings are a signal that the problem is
  drift, and drift is an enforcement problem, not a reporting one
- across an **organisation with many repositories**, where the configuration cannot be held in
  anyone's head and per-repository review does not scale
- to hold a baseline after a hardening exercise, so the work does not quietly unwind
- on GitHub, which is the only place it works — it is a GitHub App and it reads and writes GitHub's
  configuration API. See [`version-control/github/`](../../../../../devops/version-control/github/README.md)
- **starting in `issue` mode**, always. See the notes

## When not to use it

- as an artefact control. It never looks inside an image or a package — that is everything else in
  [`supply-chain/`](../../README.md), and Allstar is complementary to all of it rather than
  overlapping any of it
- as a code scanner. It does not read the source for vulnerabilities; the "binary artifacts" policy
  is the closest it comes, and it is checking for a *file type*, not behaviour
- as a substitute for cluster-side enforcement. Nothing it does stops a bad image running — that is
  [`3-container/admission/`](../../../../3-container/admission/README.md)
- in `fix` mode on day one, on repositories whose owners have not agreed to it. A bot that silently
  changes a team's settings buys a political problem that outlives the technical one
- outside GitHub. There is no GitLab or Gitea equivalent in this project

## Notes

**Configuration is opt-in or opt-out, and the choice is organisational, not technical.** Allstar
reads its configuration from a designated repository in the organisation and from per-repository
files. It can be run as **opt-in** — only repositories that explicitly enable it are governed — or as
**opt-out**, where the whole organisation is covered and individual repositories must exclude
themselves. Opt-in is how it gets adopted; opt-out is how it eventually means something. Going
straight to opt-out across an organisation that has not been told is the fastest way to have the App
uninstalled.

**`issue` versus `fix`, and start with `issue`.** Each policy is configured with an action:

| Action | Behaviour | When |
|---|---|---|
| `log` | records the violation only | measuring the size of the problem |
| **`issue`** | opens (and reopens) a GitHub issue on the offending repository | **the default starting point** |
| `fix` | changes the setting itself, where the policy supports it | after the findings are understood and the owners agree |

This is the same argument this repository makes about admission control: **start in audit, learn what
would have been rejected, then enforce.** See
[`3-container/admission/`](../../../../3-container/admission/README.md), where the recommended
sequence begins in warn/audit mode for exactly this reason. Turning on automatic remediation before
anyone has seen the finding list produces surprise configuration changes on repositories whose owners
did not know a bot was watching, and the reaction to that is not "thank you".

The `issue` mode has a second property worth naming: an issue is a **conversation on the repository
that is out of compliance**, addressed to the people who can fix it, rather than a row in a dashboard
that a central security team has to chase. That is usually the difference between findings that get
fixed and findings that get triaged.

**The scope limit, stated honestly: Allstar governs repository settings, not code.** It cannot tell
you what a dependency does, whether an image is signed, or what is in a build. It sits alongside the
rest of [`supply-chain/`](../../README.md) rather than duplicating any of it — and its specific
contribution is the one thing the SBOM-and-signing chain cannot provide, which is that the
*repository producing the artefacts* stays configured the way it was configured.

Two of its policies overlap directly with exposure recorded elsewhere in this repository: **dangerous
workflows** and unpinned actions are the same GitHub Actions failure modes that
[harden-runner](../../../runner-hardening/harden-runner/README.md) contains from the runtime side and
that [Scorecard](../scorecard/README.md) reports on. Allstar is the third angle — it keeps the
setting from regressing in the first place.

Not run here. This is a public repository, so like Scorecard it is available at no cost, and the
honest sequencing is: run Scorecard first, read the failing checks, fix them, then install Allstar in
`issue` mode to keep them fixed.

---

[← Posture](../README.md)
