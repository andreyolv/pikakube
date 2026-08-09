[← Test doubles](../README.md)

# Mailpit

<https://github.com/axllent/mailpit>

---

## The problem it solves

**A fake SMTP server that catches every email an application sends and shows it in a web inbox — and
that is still actively developed.**

Point the application's SMTP configuration at Mailpit and it accepts everything, delivers nothing,
and stores the messages. A web UI lists them; an HTTP API lets tests read and assert on them.

Two distinct problems, solved by one service:

| Problem | Answer |
|---|---|
| Test environments sending real mail to real people | it delivers nothing, ever |
| Nobody can see whether the email is actually correct | a web inbox, with the rendered message |

It goes further than simply capturing mail. Mailpit checks the HTML for client compatibility, tests
links, produces a spam score, and can **release** a captured message to a real server when someone
genuinely needs it delivered. Storage is SQLite-backed with retention limits, so it survives a
restart and does not grow without bound.

The general argument for using it instead of mocking the mailer is in
[`test-double/`](../README.md) section 3: a mock asserts that you called your own function; a real
SMTP server exercises the connection, the credentials, the TLS handshake, the MIME structure and the
rendered template.

## When to use it

- **any non-production environment** where the application sends email — development, CI, staging
- integration tests that assert on the actual message: recipients, subject, body, attachments
- letting a designer, QA engineer or product owner read the real rendered email
- **new work** — this is the one to choose over [MailHog](../mailhog/README.md)
- debugging mail configuration, where the failure is in the connection rather than the code

## When not to use it

- **production** — it swallows every message; pointing production at it is silent, total mail loss
- as a real mail relay: it does not deliver (the release feature is manual and deliberate)
- to test deliverability, SPF, DKIM or inbox placement — none of that is reachable from a fake
- for dependencies that are not SMTP — see [`test-double/`](../README.md) section 4
- as a substitute for running a real dependency that is cheap to run — Postgres, Redis and brokers
  should be real, via [testcontainers](../../unit/testcontainers/README.md)

## Notes

The recorded note is <https://github.com/axllent/mailpit>.

**Mailpit is the actively developed successor to [MailHog](../mailhog/README.md).** That is the
finding to carry forward from this folder. Both are deployed in this repository and they do the same
job; MailHog has seen essentially no development for years, and Mailpit is where the work happens.
New work should use this one, and the MailHog release should be treated as the one to retire.

**What is deployed here:**

| Manifest | Detail |
|---|---|
| `namespace.yaml` | namespace `mailpit` |
| `helm/helmrepository.yaml` | Flux `HelmRepository` for `jouve`, in `flux-system` |
| `helm/helmrelease.yaml` | chart `mailpit`, **version 0.21.0**, 5m reconcile interval |

The chart is `jouve/mailpit`, a community chart rather than an official one — worth noting, because
in a GitOps repository the chart's maintenance is half the evaluation of a tool. The `values` block
in the `HelmRelease` is empty, with the upstream `values.yaml` and Artifact Hub page recorded as
comments, so the release currently runs on chart defaults.

Two things to set before this is more than a default install:

- **Authentication on the ingress.** An unauthenticated Mailpit is a searchable archive of every
  message the platform sends — password resets, invitations, tokens.
- **Retention.** The store is capped by configuration; without a cap it grows for as long as the
  environment sends mail.

---

[← Test doubles](../README.md)
