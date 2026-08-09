[← DAST](../README.md)

# ZAP

<https://github.com/zaproxy/zaproxy>
<https://github.com/zaproxy/action-baseline>
<https://github.com/zaproxy/action-api-scan>
<https://github.com/zaproxy/action-full-scan>

---

## The problem it solves

ZAP is the reference open-source web application security scanner. At its core it is an
**intercepting proxy**: every request between a client and the application passes through it, so
it can observe, modify and replay traffic. Everything else is built on that.

The capabilities that matter:

| Capability | What it does |
|---|---|
| **Passive scanning** | analyses traffic that passes through without sending anything extra — headers, cookie flags, information disclosure, TLS. **Safe by construction** |
| **Active scanning** | sends crafted attack payloads — injection, XSS, path traversal, command injection. Thorough, slow, and destructive if pointed at the wrong place |
| Spider and AJAX spider | discovers the application surface; the AJAX spider drives a real browser for JavaScript-rendered applications |
| **Import an API definition** | OpenAPI, SOAP or GraphQL. This is the single biggest coverage improvement available |
| Authentication and session handling | scripted logins, session management, and — critically — exclusion rules |
| Manual testing tools | request editor, fuzzer, breakpoints. It is also a hands-on tool for someone testing deliberately |
| Automation Framework | a YAML plan describing the whole scan, which is how it belongs in CI rather than as a GUI |

Governance note worth knowing: ZAP was an OWASP flagship project for many years and moved to the
**Software Security Project** in 2023. Older documentation still says "OWASP ZAP", and the name
appears both ways in the wild. The tool is the same.

## When to use it

- **A web application you own, tested in depth.** This is what ZAP is for, and nothing
  open-source does it better
- **Driven by an API definition.** Importing an OpenAPI specification skips the discovery problem
  entirely and is the difference between testing 5% and 90% of the surface —
  see [`../../api/README.md`](../../api/README.md)
- **Baseline scanning in CI**, on every build. Passive only, fast, safe, and it catches missing
  headers, cookie flags and TLS misconfiguration — cheap, real findings
- **Manual security testing.** As a proxy and request editor it is the tool a person uses to
  examine an application by hand
- **Replaying functional test traffic through it**, which inherits your test suite's coverage for
  free — the highest-value trick in this page

## When not to use it

- **Against production.** An active scan sends real attack payloads to a live system. It will
  create records, trigger workflows, send email and can cause an outage. Baseline (passive) scans
  are the only safe production-adjacent mode
- **As a per-commit gate.** A full scan takes a long time and its findings need interpretation.
  Baseline in CI, full scan on a schedule
- **On a JavaScript-heavy SPA without an API definition.** The spider will find very little, and
  a clean report will mean nothing
- **Against systems you do not own.** That is an attack, whatever the intent
- **When you want broad known-CVE coverage across many hosts.** That is
  [`../nuclei/README.md`](../nuclei/README.md); ZAP goes deep on one application, not wide across
  many
- **Without excluding logout and destructive endpoints.** Not a preference — an unexcluded
  `/logout` silently invalidates the rest of the scan

## Notes

Original notes recorded for this tool. The three Actions are the important part, because they are
not variants of one thing — **they are the three scan depths**, and choosing between them is the
main decision when putting ZAP into CI:

- <https://github.com/zaproxy/zaproxy> — the scanner itself: the proxy, the scan rules, the
  desktop application, the Automation Framework YAML format and the API. The add-on marketplace
  is also here, and several important capabilities (the AJAX spider, some scan rules) are add-ons
  rather than core.

- <https://github.com/zaproxy/action-baseline> — the **baseline scan** Action. Spiders the target
  for a short, bounded time and runs **passive** rules only. It sends no attack payloads, so it is
  safe to run against almost anything, and it is fast enough for every pull request. What it
  catches: missing security headers, cookie flags, information disclosure, mixed content, TLS
  problems. **This is the one to start with**, and for many teams it is the only one they ever
  need in CI.

- <https://github.com/zaproxy/action-api-scan> — the **API scan** Action. Takes an OpenAPI, SOAP
  or GraphQL definition and scans the endpoints it describes, rather than crawling. This solves
  the coverage problem described in [`../README.md`](../README.md) section 2 and is the right
  choice for any service with a contract. It performs active scanning against those endpoints, so
  it belongs against staging, not production. Its natural companion is
  [`../../api/schemathesis/README.md`](../../api/schemathesis/README.md), which attacks the same
  specification from a different angle — property-based conformance rather than attack payloads.

- <https://github.com/zaproxy/action-full-scan> — the **full scan** Action. Spider plus AJAX
  spider plus **active** scanning with no time limit. The most thorough and by far the most
  dangerous: it sends real payloads and can take hours. Run it on a schedule against a disposable
  environment, never per commit and never against production.

All three Actions can fail the build on findings and can be configured with a rules file that
downgrades specific alerts to warnings — which is how you keep a baseline scan useful without it
blocking on the same three known-accepted findings forever.

---

[← DAST](../README.md)
