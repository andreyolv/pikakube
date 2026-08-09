[← Web scraping](../README.md)

# Selenium

<https://github.com/SeleniumHQ/selenium>

---

## The problem it solves

**Automating any browser, through a standard.**

Selenium is the oldest and most established browser automation project, and it is not merely legacy
tooling: **WebDriver is a W3C standard**, and Selenium is its reference implementation. Browser
vendors ship drivers that implement it, which is why Selenium reaches browsers nothing else does —
including real Safari.

What it gives you that [Playwright](../playwright/README.md) does not:

| Capability | Detail |
|---|---|
| **Browser reach** | anything with a WebDriver implementation, via the vendor's own driver |
| **Language coverage** | more bindings, and longer-established ones |
| **Selenium Grid** | a mature, well-understood way to run many browsers across many machines |
| **Ecosystem and knowledge** | an enormous body of existing code, tutorials and institutional experience |
| Standardisation | scripts are written against a specification, not a single vendor's tool |

The trade is the waiting model. Selenium's API does not wait for you: elements must be waited on
explicitly, with expected conditions. Done properly that is fine; done the way most codebases do it,
it produces the `sleep()` calls that make browser suites slow and flaky. Playwright's auto-waiting is
the single largest practical difference between the two.

## When to use it

- **an existing Selenium codebase** — it works, it is standard, and rewriting it is rarely worth it
- browsers Playwright does not cover, notably **real Safari** and vendor-specific drivers
- **Selenium Grid** already running, or a requirement for a large distributed browser farm
- a language binding Playwright does not offer
- environments where W3C WebDriver conformance is itself a requirement

## When not to use it

- **new work with no constraint pushing you here** — [Playwright](../playwright/README.md)'s
  auto-waiting and network interception make it the better default
- when you need to intercept or stub network requests — Selenium's support is limited, and this is
  often how you discover the JSON API that removes the need for a browser entirely
- **the data is in the server's HTML, or behind a JSON endpoint** — no browser is needed at all; see
  [`web-scraping/`](../README.md) section 2
- an official API exists
- load testing — [`load/`](../../testing/load/README.md)

## Notes

The recorded note is <https://github.com/SeleniumHQ/selenium> — the umbrella project, covering every
language binding, the Grid and the WebDriver implementation, rather than one language's package. That
is the right link for Selenium and it contrasts with
[Playwright](../playwright/README.md), which was recorded as `playwright-python` specifically. The
difference reflects how the two projects are organised: Selenium is one repository of many bindings;
Playwright is a Node core with separate per-language repositories.

**The same classification note applies as for Playwright.** Selenium is, first and foremost, a
**browser testing framework** — WebDriver exists to automate browsers for tests. It is filed under
`web-scraping/` because that is the use it is here for, following this repository's rule of
classifying by use rather than by full capability. [`web-scraping/`](../README.md) section 1 sets out
the overlap; [`testing/`](../../testing/README.md) covers where an end-to-end layer belongs and why it
should stay small.

Nothing is deployed for it. If Selenium Grid were adopted, it would be the one part of this folder
that becomes a platform service — a hub and a set of browser nodes — which is a real operational
commitment: browser nodes are memory-hungry, crash, and leave zombie processes behind.

The same container caveats as Playwright apply, and they are the reason to use the **official
Selenium images** rather than building your own:

- `/dev/shm` must be enlarged, or Chromium crashes with no useful error
- the **driver and browser versions must match** — the official images handle this, hand-built ones
  drift
- run scrapes as `Job`s, and reap zombie processes

---

[← Web scraping](../README.md)
