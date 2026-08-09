[← Dashboards](../README.md)

# Radar

<https://github.com/skyhook-io/radar>

---

## The problem it solves

Recorded as a bookmark, with no manifests and no evaluation. What is known is what the project name
and organisation say: a Kubernetes visualisation tool from Skyhook.

Rather than guess at its feature set, the useful thing to record is **why it is here at all** — this
folder is a survey of the dashboard category, and Radar was noted as something to look at and never
looked at. That is a legitimate state for an entry in an inventory, and pretending otherwise would be
worse than saying so.

## When to use it

- Nothing here justifies a recommendation; treat this as an unexplored option
- If the tools already evaluated in this folder do not fit, this is on the list to try next

## When not to use it

- Anywhere that matters, until someone has actually run it
- As a substitute for the evaluated options; [Headlamp](../headlamp/README.md) is the default here for good reasons
- Without first checking the project's activity and licensing

## Notes

The entire original note:

```
https://github.com/skyhook-io/radar
```

No chart, no `HelmRelease`, no namespace manifest, no commands. Compare with
[Headlamp](../headlamp/README.md), which carries a token command, a verdict and two upstream issues —
the difference between the two folders is the difference between a tool that was used and a tool that
was noticed.

The reason to keep the entry rather than delete it: a link with no evaluation still records that the
option exists and was considered, which is more than a missing folder communicates. The reason to
label it clearly: an unevaluated bookmark sitting in a directory of installed tools is easy to
mistake for a recommendation.

If it is ever picked up, the questions this folder has already learned to ask are the ones to bring:
how does it authenticate, does it scope by namespace for real, and does it need cluster-wide read to
render its navigation. Those three decide whether a dashboard is deployable, and they are not in any
project's README.

---

[← Dashboards](../README.md)
