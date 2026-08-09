[← Right-sizing](../README.md)

# Goldilocks

<https://github.com/FairwindsOps/goldilocks>
<https://github.com/FairwindsOps/charts>

---

## The problem it solves

[VPA](../vpa/README.md) produces good recommendations and puts them somewhere nobody looks — inside
a `VerticalPodAutoscaler` object's status, one `kubectl describe` at a time. Recommendations that
require a platform engineer to extract them do not turn into merged pull requests.

Goldilocks is a **dashboard over VPA recommendations**. Label a namespace, and it creates a VPA in
`Off` mode for each workload in it, then presents the results as a page: what each container
requests today, and what the recommender thinks it should request — with a "guaranteed" and a
"burstable" suggestion side by side.

It changes nothing. Its entire value is social: **a page a team can open themselves.** Right-sizing
stalls because it needs dozens of application teams to lower a number that protects them, and a URL
they can see their own namespace on moves that conversation further than a spreadsheet from the
platform team.

## When to use it

- **driving right-sizing across many teams**, where the constraint is attention rather than data
- alongside a cost-per-namespace number from [`visibility/`](../../../visibility/README.md) — "this
  is what you spend, and this is what you would spend" is a complete argument
- as the read-only front end for a VPA installation that will never be allowed to mutate anything
- onboarding a namespace to spot or to a tightly-packed node pool, where wrong requests are about to
  start mattering — see [`node/`](../../node/README.md)

## When not to use it

- **without VPA** — it is a UI over VPA's recommender, not an independent one, and it inherits every
  property of that algorithm
- as an enforcement mechanism; nothing here applies a change
- when a one-off report is what is wanted — [KRR](../krr/README.md) prints the same gap from the CLI
  with nothing installed
- as the only input for workloads with seasonal or startup peaks its VPA window never observed
- expecting it to cover limits as thoughtfully as requests; the underlying recommendations are
  request-shaped

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/FairwindsOps/goldilocks>** — the project. Fairwinds also maintain the VPA chart
this repository uses, which is why the two are usually deployed together and why the pairing is well
trodden.

**<https://github.com/FairwindsOps/charts>** — the chart repository, served over HTTP at
`https://charts.fairwinds.com/stable`. Note the constraint recorded against
[VPA](../vpa/README.md): Fairwinds do not publish OCI artefacts
(<https://github.com/FairwindsOps/charts/issues/1817>, still open), so both charts have to be
consumed through a classic `HelmRepository` rather than the `OCIRepository` shape used elsewhere in
this repository.

**On the deployment here.** Flux, chart **9.0.0** from `https://charts.fairwinds.com/stable`, into a
dedicated `goldilocks` namespace, with default values.

Two things that are not in the manifests and decide whether it produces anything:

1. **Namespaces must be opted in with a label** (`goldilocks.fairwinds.com/enabled=true`). Nothing
   happens by default — an empty dashboard usually means no namespace has been labelled, not that it
   is broken. The opt-in model is a feature: it is the same incremental, per-namespace onboarding
   pattern the [Spot Ocean](../../node/spot-ocean/README.md) notes describe for spot.
2. **VPA must be installed and its recommender must have history.** Goldilocks with a
   freshly-restarted recommender shows confident numbers derived from minutes of data. Wiring the
   recommender to Prometheus — the commented-out block in [VPA](../vpa/README.md) — fixes that, and
   matters more here than anywhere, because this is the surface teams will actually read.

**The dashboard is not exposed** by anything in this folder — no Ingress or route is defined, so
access is by port-forward. For a tool whose entire value is that other people open it, that is the
gap worth closing.

---

[← Right-sizing](../README.md)
