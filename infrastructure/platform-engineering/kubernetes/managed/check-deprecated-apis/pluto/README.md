[← Check deprecated APIs](../README.md)

# Pluto

<https://github.com/FairwindsOps/pluto>

---

## The problem it solves

Pluto finds deprecated and removed Kubernetes API versions in four places: YAML files on disk, the
output of `helm template`, **Helm releases already installed in a cluster**, and live cluster
objects. It reports which API each object uses, which version deprecated it, and — the field that
actually matters — which version **removed** it.

The Helm release scanning is the differentiator. Helm stores the last applied manifest in a Secret
in the release namespace; Pluto reads those, so a chart installed a year ago and never touched is
still checked. Nothing about that is visible from your Git repository.

## When to use it

- As a CI gate on manifests and rendered charts — it exits non-zero on findings, which is the whole point
- Auditing Helm releases installed in a cluster you inherited
- Before any minor-version upgrade, as the checklist item that comes first
- Producing a list you can sort by removal version, to separate the urgent from the eventual

## When not to use it

- As the only check; it finds deprecated APIs, not bad manifests generally — that is a policy engine's job
- Expecting it to fix anything; it reports, you edit
- Against a version it does not know about — the version data ships with the binary, so an old Pluto misses new removals
- As a substitute for reading the upstream deprecation guide on a major jump

## Notes

Recorded as a link only:

```
https://github.com/FairwindsOps/pluto
```

No commands, no deployment. Known, not run.

The thing to keep straight when it is run: **deprecated and removed are different columns and
different urgencies.** Deprecated means it still works and upstream has announced an intent;
removed means the API server will reject it. Pluto reports both, and a report with fifty deprecated
entries and zero removed ones requires no action this quarter.

The other operational detail: Pluto's knowledge of which version removed what is **compiled into the
binary**. An old Pluto scanning for a new Kubernetes release will confidently report nothing.
Pinning it in CI is right; pinning it and forgetting it is how the check silently stops checking.

Fairwinds maintain it alongside Polaris and Goldilocks, which is a reasonable signal about the
project's ongoing health — and if the wider question is "what else is wrong with these manifests",
those are the neighbours to look at.

---

[← Check deprecated APIs](../README.md)
