[← Dashboards](../README.md)

# Perses

<https://github.com/perses/perses>
<https://github.com/perses/helm-charts>

---

## The problem it solves

Grafana grew a code-first story over time; Perses started there. It is a CNCF dashboard tool
built around **dashboards-as-code from the beginning**, with a defined schema, CRDs, and a
CLI for validating and deploying them.

What that buys over bolting GitOps onto a UI-first tool:

- a **specified dashboard format**, versioned and validatable — not JSON scraped out of a UI
- **native Kubernetes resources**, so dashboards reconcile like anything else
- a much smaller footprint

## When to use it

- dashboards must be code, reviewed and validated in CI, with no UI-first path available to drift back into
- you want something lightweight, without Grafana's plugin surface
- CNCF governance matters for the choice

## When not to use it

- you depend on Grafana's **ecosystem** — the community dashboard library and plugins are the
  practical reason most teams stay, and Perses does not replace them
- the team already knows Grafana and there is no pain to fix

## The honest framing

Technically cleaner for the declarative use case, and behind on ecosystem. Worth tracking;
worth adopting when dashboard drift is a real problem rather than a theoretical one.

---

[← Dashboards](../README.md)
