[← API security testing](../README.md)

# apisec-scan

<https://github.com/apisec-university/free-API-security-test-action>

---

## The problem it solves

APIsec is a commercial API security testing service. `apisec-scan` is the **GitHub Action front
end** to it: the Action registers or references an API, triggers a scan against a running
deployment, and reports the results back into the workflow.

The model is different from everything else in this folder, and the difference is the point:

| | Self-hosted tools | **apisec-scan** |
|---|---|---|
| What you operate | a CLI, or a platform with a database | nothing — it is a hosted service |
| Where the testing runs | your infrastructure | the vendor's, against your endpoint |
| Test coverage | what you configure | the vendor's test library, maintained by them |
| Authorisation testing | you construct it | included, since it is what the product is for |
| Cost | your time | a subscription, with a limited free tier |

What a managed service buys is the part teams most often fail to build: **authorisation testing
across identities**. As set out in [`../README.md`](../README.md) section 3, BOLA and BFLA are the
top API vulnerability classes and they require replaying requests as different users and reasoning
about what should have been refused. Building that yourself is real work; buying it is a
subscription.

## When to use it

- **You want managed API security testing with no platform to run.** That is the entire
  proposition, and for a small team it is a legitimate one
- **Authorisation testing is the requirement** and there is no appetite to build it
- **A compliance requirement for third-party testing.** A vendor report satisfies an auditor in a
  way a self-run scan sometimes does not
- **Evaluating the category.** The free Action is a low-cost way to see what a commercial API
  scanner finds against your API before committing to anything

## When not to use it

- **You need self-hosted or air-gapped testing.** The service scans from outside; your API must be
  reachable by the vendor. That is disqualifying in many environments, and it is the first thing
  to check
- **The API is internal only.** Same reason — the vendor has to reach it
- **Free-tier limits do not fit.** A free tier is a marketing entry point; the limits (number of
  APIs, scan frequency, feature availability) decide whether it is usable, and they can change
- **You want an open-source path.** [`../akto/README.md`](../akto/README.md) covers similar
  ground with a self-hosted deployment
- **Conformance and robustness are the actual need.** That is
  [`../schemathesis/README.md`](../schemathesis/README.md), free, open source, and running inside
  your own CI
- **Sending real API traffic and credentials to a third party is unacceptable** for the data
  involved. This is a data-handling decision, not a technical one, and it should be made
  deliberately

## Notes

Original note recorded for this tool — note that it was kept in a file named `references.md`
rather than `doc.md`, which is why it reads as a bare pointer:

- <https://github.com/apisec-university/free-API-security-test-action> — the **free** API security
  test GitHub Action, published under the `apisec-university` organisation. Two things are worth
  drawing out of that name:

  - **"free"** signals that this is the no-cost entry point to a commercial product, not an
    open-source tool. The Action is the client; the scanning happens in APIsec's service. Read the
    current terms and limits before designing a pipeline around it.
  - **`apisec-university`** is the vendor's educational arm. Their training material on API
    security — the OWASP API Security Top 10, BOLA and BFLA in particular — is genuinely useful
    independently of the product, and is arguably the more valuable half of the link for anyone
    trying to understand *why* API testing needs multiple identities.

Nothing is deployed for this tool and nothing needs to be: it is a GitHub Action and an account.
The decision it represents is buy-versus-build for authorisation testing, and that decision is
worth taking explicitly rather than by default.

---

[← API security testing](../README.md)
