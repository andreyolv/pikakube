[← Web scraping](../README.md)

# Playwright

<https://github.com/microsoft/playwright-python>

---

## The problem it solves

**Driving a browser without the waiting problem.**

Almost all flakiness in browser automation comes from acting before the page is ready. The usual
patch is a `sleep(2)`, which is slow when it works and still wrong when it does not.

Playwright makes waiting implicit: **every action waits for the element to be attached, visible,
stable and able to receive the event** before it acts, and times out with a useful message if it
never gets there. That single design decision removes the largest source of flaky browser code, in
scraping and in testing alike.

Three other things make it the better default for new work:

| Feature | Why it matters here |
|---|---|
| **Network interception** | see and modify every request the page makes — which is usually how you find the JSON API that makes the browser unnecessary — and block images, fonts and analytics for a large speed-up |
| **Browser contexts** | an isolated cookie/storage profile inside one browser process; parallelism without one browser per worker |
| **Bundled browsers** | Chromium, Firefox and WebKit, versioned with the library — no driver-to-browser mismatch |

It also ships tracing, video and screenshot capture, which are debugging tools for a scraper as much
as for a test: when a run fails at 3am, the trace shows what the page looked like.

## When to use it

- **new browser automation of any kind** — this is the default choice over
  [Selenium](../selenium/README.md)
- content that only exists after JavaScript runs, with no reachable API
- scrapes that benefit from blocking assets or capturing the page's own network calls
- multi-step interactions: login, forms, navigation flows
- end-to-end testing of your own application — see the note below

## When not to use it

- **the data is in the server's HTML** — an HTTP client and a parser are orders of magnitude cheaper;
  see [`web-scraping/`](../README.md) section 2
- **the page fetches JSON** — call that endpoint directly instead
- an official API exists
- a browser that only WebDriver reaches, such as real Safari — [Selenium](../selenium/README.md)
- an existing, working Selenium suite; rewriting it buys less than it costs
- load testing — [`load/`](../../testing/load/README.md)

## Notes

The recorded note is <https://github.com/microsoft/playwright-python> — **the Python binding
specifically**, not the Node original. That is consistent with
[`language/python/`](../../language/python/README.md) being the primary language in this repository,
and it is worth being precise about: the Node package is where features land first, and the Python
binding follows. Most Playwright documentation and examples online are JavaScript, and translating
them is usually mechanical but not always.

**The honest classification note.** Playwright is, arguably primarily, an **end-to-end testing
framework**. It ships a test runner, assertions, fixtures, retries, tracing and visual comparison,
and most of its documentation is about testing. It is filed under `web-scraping/` because that is
how it is used here — this repository classifies by use rather than by full capability, and
[`web-scraping/`](../README.md) section 1 states that openly. If the goal is end-to-end tests of your
own service, this is still the tool; read [`testing/`](../../testing/README.md) for where that layer
belongs and how small it should be.

Nothing is deployed for it. It is a library used from application code, so what would exist in a
repository is the `Job` that runs a scrape. The operational notes for that, all covered in
[`web-scraping/`](../README.md) section 4, are worth repeating because each one costs an afternoon
when hit cold:

- **use the official Playwright image** — the browsers and system libraries are already correct
- **increase `/dev/shm`**, or Chromium crashes with no useful error
- **run scrapes as `Job`s, not a `Deployment`** — a long-lived browser leaks
- **an init process to reap zombies**, or crashed browsers accumulate until the pod dies

---

[← Web scraping](../README.md)
