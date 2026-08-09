[← Test doubles](../README.md)

# MailHog

<https://github.com/mailhog/MailHog>
<https://github.com/codecentric/helm-charts>

---

## The problem it solves

**The original fake SMTP server: catch every email a non-production environment sends, and show it
in a web inbox.**

MailHog is a single Go binary that listens on SMTP, accepts everything, delivers nothing, and
exposes what it caught through a web UI and an HTTP API. It is the tool most people mean when they
say "catch-all mail server", and its name appears in a very large number of `docker-compose.yml`
files and tutorials.

It solves the same two problems as [Mailpit](../mailpit/README.md) — no mail reaching real people,
and a human-readable view of what the application actually sent — and it does them adequately.

**It is also effectively unmaintained.** Its repository has seen essentially no development for
years. The binary still works, because it is small software doing a simple job, but issues go
unfixed, dependencies age, and nothing about it is better than its successor.

## When to use it

- **an existing MailHog deployment** that works and that nobody has time to migrate
- reproducing a setup — a tutorial, an inherited `docker-compose.yml`, a legacy environment — where
  MailHog is what is specified
- recognising it: knowing what it is, and that it has a successor, is most of the value here

## When not to use it

- **new work** — use [Mailpit](../mailpit/README.md), which is actively developed and does more
- when the extra features matter: link checking, HTML compatibility checks, spam scoring, message
  release, SQLite-backed retention
- **production** — like any fake, it discards every message it accepts
- for deliverability, SPF or DKIM testing — a fake cannot answer those
- as the only fake for non-SMTP dependencies — see [`test-double/`](../README.md) section 4

## Notes

Two links were recorded, and the second one is the interesting one:

**<https://github.com/mailhog/MailHog>** — the tool. Open source, Go, and the original of this
category.

**<https://github.com/codecentric/helm-charts>** — the **Helm chart**, which is not maintained by the
MailHog project. That separation is worth recording explicitly: in a GitOps repository the chart is
half of what you are adopting, and here the tool and the chart have different maintainers and
different levels of activity. MailHog being stagnant upstream says nothing directly about the
chart's state, and vice versa — both need checking.

**What is deployed here:**

| Manifest | Detail |
|---|---|
| `namespace.yaml` | namespace `mailhog` |
| `helm/helmrepository.yaml` | Flux `HelmRepository` for `codecentric`, in `flux-system` |
| `helm/helmrelease.yaml` | chart `mailhog`, **version 5.5.0**, 5m reconcile interval |

The `values` block is empty, with the Artifact Hub page and the upstream `values.yaml` recorded as
comments, so it runs on chart defaults.

**The recommendation for pikakube is to retire this release.** [Mailpit](../mailpit/README.md) is
deployed alongside it, does the same job, is actively developed, and offers more. Running both means
two SMTP endpoints in the cluster that applications can be pointed at by accident, and two charts to
track for one capability.

The same operational cautions apply while it is running: **put authentication in front of the UI** —
it is an archive of every message the platform sends — and be certain nothing in production has its
SMTP host pointed at it, because the failure mode is total, silent mail loss.

---

[← Test doubles](../README.md)
