[← Dashboard ingress](../README.md)

# Hajimari

<https://github.com/toboshii/hajimari>

---

## The problem it solves

The same problem as [Forecastle](../forecastle/README.md), aimed at a homelab rather than a
platform: a start page that discovers applications from `Ingress` annotations, adds a search bar and
a set of bookmarks, and looks pleasant enough to set as the browser's home page.

It is the lighter of the two discovery-based options here — fewer knobs, a nicer default
appearance, and personal bookmarks as a first-class feature rather than an afterthought.

## When to use it

- A homelab or a small cluster where the page is genuinely somebody's home page
- Discovery from Ingress annotations, with a search bar attached
- You want something that looks finished with almost no configuration

## When not to use it

- Large multi-team platforms where grouping and namespace scoping matter — Forecastle has more control there
- Services not behind an `Ingress`
- Anywhere it would be publicly reachable
- If project activity is a concern; check before adopting, as with any single-maintainer project

## Notes

**Chart** `hajimari` version `2.0.2` from `https://hajimari.io`, with the upstream values file
referenced as a comment:

- `https://github.com/toboshii/hajimari/blob/main/charts/hajimari/values.yaml`

The entire configuration is:

```yaml
values:
  ingress:
    main:
      enabled: true
```

Nothing else. No title, no bookmarks, no groups — the chart's defaults with an Ingress turned on.
Compared with [Forecastle](../forecastle/README.md), which has a title, colours, a namespace
selector, custom apps and TLS, this is a *does it install* check rather than an evaluation.

No notes were recorded against it, and no problems either, which given that Forecastle's folder
carries a filed bug is a mild signal in Hajimari's favour — though a chart installed with default
values has not been asked hard questions.

The `ingress.main` key shape comes from the `bjw-s` common chart library that this and many
homelab-oriented charts are built on. Worth knowing because the values structure will look
unfamiliar if you expect the usual `ingress.enabled`, and because it means the same patterns apply
across a whole family of charts.

---

[← Dashboard ingress](../README.md)
