[← API security testing](../README.md)

# Akto

<https://github.com/akto-api-security/akto>

---

## The problem it solves

Akto starts from the question no specification-driven tool can answer: **which APIs do we
actually have?**

Every real estate has more endpoints than documents. An internal service nobody registered, a v1
that was never decommissioned, a partner integration built in a hurry, an endpoint a team added
last quarter. Testing only the documented surface means testing the part that was already being
looked after.

Akto's model:

| Stage | What it does |
|---|---|
| **Discovery** | ingests real traffic — from a Kubernetes mirror, a service mesh, an eBPF agent, a load balancer, a proxy, or Burp/Postman exports — and **infers the API surface from what is actually called** |
| **Inventory** | builds a catalogue of endpoints, parameters and observed response shapes, and flags **sensitive data** appearing in responses (emails, tokens, card numbers, personal data) |
| **Testing** | runs security tests against the discovered inventory, including the authorisation classes that require multiple identities |
| **CI integration** | tests run on a pull request against the endpoints affected |

The two capabilities that justify a platform rather than a CLI:

- **Traffic-based discovery.** Nothing derived from a repository can tell you about an endpoint
  nobody documented. Only observed traffic can.
- **Authorisation testing across identities.** BOLA and BFLA — the top entries in the OWASP API
  Security Top 10 — are only detectable by replaying a request as a *different* user and seeing
  whether it succeeds. Akto automates exactly that, which is the hard part of API security
  testing.

It is open source with a self-hosted deployment, alongside a commercial cloud offering.

## When to use it

- **You do not have a reliable inventory of your APIs.** This is the primary case and it is a
  genuine problem at any real scale
- **Authorisation testing is the requirement** — BOLA, BFLA, mass assignment. These are the
  vulnerabilities that matter most in APIs and the ones conformance testing cannot see
- **Sensitive data exposure detection.** Knowing which endpoints return personal data is a
  compliance question as much as a security one, and traffic observation is how you answer it
- **A microservice estate** where the API surface is spread across teams and nobody has the whole
  picture
- **You want self-hosted.** The open-source deployment is real, which distinguishes it from most
  API security products

## When not to use it

- **A small number of well-documented services.** [`../schemathesis/README.md`](../schemathesis/README.md)
  in CI covers those with nothing deployed and no traffic plumbing
- **You cannot mirror traffic.** Discovery is the core capability and it depends on getting real
  traffic to the platform. Without that you have a testing tool with an empty inventory
- **You are not prepared to operate a platform.** It is a multi-component application with a
  database and a UI, not a binary in a pipeline
- **Sensitive traffic and unclear data handling.** The platform will see real request and response
  bodies, including personal data. Self-hosted mitigates this; the cloud offering makes it a
  question to answer deliberately
- **As a replacement for conformance testing.** Different question — Akto tests what exists,
  Schemathesis tests whether it matches what was promised

## Notes

Original note recorded for this tool:

- <https://github.com/akto-api-security/akto> — the upstream project. The repository documents the
  traffic connector options (Kubernetes daemonset with eBPF, AWS traffic mirroring, service mesh
  integrations, Burp and Postman imports), the self-hosted deployment, the test library and how to
  write custom tests in its YAML test format, and the CI/CD integration for running tests on a
  pull request.

Worth recording alongside: **its own test format is the extensible part.** The built-in library
covers the OWASP API Security Top 10, but the tests worth adding are organisation-specific — "no
endpoint may return a full card number", "this tenant header must be validated". Those are exactly
the checks a generic tool cannot ship and a traffic-aware platform can enforce across every
endpoint it discovered.

---

[← API security testing](../README.md)
