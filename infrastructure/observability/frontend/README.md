[← Observability](../README.md)

# Frontend observability

What the user actually experienced — measured in their browser, not in your cluster.

Tools covered: [`faro`](faro/README.md)

---

## The blind spot

Every other folder here measures the **server side**. The request arrived, was processed in
40ms, and returned 200. By those numbers the platform is healthy.

The user waited four seconds.

The gap is real and invisible from inside: JavaScript execution, rendering, third-party
scripts, a slow CDN, a failing request the backend never saw, an error thrown in the browser.
None of it appears in a server-side metric.

**Real User Monitoring** closes it by instrumenting the browser: page load timings, Core Web
Vitals, JavaScript errors, and failed requests — from the client, with the client's network
and device.

## Why it belongs in this repository

For a data platform, mostly it does not — pipelines have no browser. It becomes relevant at
the edges where the platform has a UI: Grafana, Airflow, Superset, a data portal. "Airflow is
slow" is frequently a frontend problem, and nothing in `metrics/` will ever show it.

The other reason is completeness: server-side observability that reports green while users
suffer is the most expensive kind of blind spot, and it is worth having mapped even when it is
not deployed.

## The tools in this folder

| Tool | Role | Detail |
|---|---|---|
| **Grafana Faro** | web SDK for RUM — sends browser telemetry into the same Grafana stack as everything else | [→](faro/README.md) |

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Declaring health from server metrics alone | the server is fine and the user is not | measure the client too |
| RUM without sampling | high-traffic sites generate enormous volume | sample, and keep errors unsampled |
| Sending session data without review | browser telemetry can carry personal data and URLs with tokens | scrub before shipping, and agree the scope |

## How this applies to pikakube

Not deployed — there is no user-facing frontend. Mapped as the missing half of the picture on
any platform that has one.

---

[← Observability](../README.md)
