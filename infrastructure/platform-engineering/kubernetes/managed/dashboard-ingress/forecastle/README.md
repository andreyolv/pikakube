[← Dashboard ingress](../README.md)

# Forecastle

<https://github.com/stakater/Forecastle>

---

## The problem it solves

Forecastle builds a launchpad page by reading `Ingress` objects across the cluster. Annotate an
Ingress with `forecastle.stakater.com/expose: "true"`, give it an icon and a group, and it appears
on the page. Remove the Ingress and it disappears.

The value is that the list cannot go stale: it *is* the cluster's ingress configuration, rendered.
Static apps can be added on top for things that live outside Kubernetes.

## When to use it

- A cluster with many web interfaces behind Ingress objects
- You want the list to maintain itself from annotations
- Grouping and namespace filtering matter
- A few external links need to sit alongside the discovered ones

## When not to use it

- Services not exposed through `Ingress` — they are invisible to it
- You want service **health** and widgets — that is [Homepage](../homepage/README.md)
- Public exposure; there is no authentication in front of it
- Wildcard `nip.io`-style hosts with TLS — see the recorded bug below

## Notes

**Chart** `forecastle` version `1.0.158` from the `stakater-charts` repository. Upstream references
kept as comments:

- `https://artifacthub.io/packages/helm/stakater/forecastle`
- `https://github.com/stakater/Forecastle/blob/master/deployments/kubernetes/chart/forecastle/values.yaml`

Configured with `namespaceSelector: any: true` — scan every namespace — the title
"PikaKube Platform", a yellow header (`#FFEB3B`) with red text (`#D32F2F`), one custom external app,
and an Ingress on `pikakube.127.0.0.1.nip.io` using a `mkcert`-issued TLS secret.

### The bug

The recorded note is emphatic, and translated it reads: *"a completely ridiculous bug — it takes the
URL from `tls.hosts` instead of `rules.hosts`. Karpor's ingress does not work with
`*.127.0.0.1.nip.io`."*

- <https://github.com/stakater/Forecastle/issues/440>
- <https://github.com/stakater/Forecastle/issues/496>

Why it matters, spelled out: an `Ingress` has two places a hostname can appear. `spec.rules[].host`
is the host that is actually routed. `spec.tls[].hosts` is the list of names the certificate covers,
and it is legitimate — normal, even — for it to hold a **wildcard** such as `*.127.0.0.1.nip.io`.
Forecastle builds its link from the TLS entry, so the page ends up with a literal `*.` in the URL,
which resolves to nothing.

The consequence is that a perfectly correct Ingress produces a broken link, and the page looks like
it is working. This is the precise failure mode that makes a link page dangerous: it is trusted
because it is generated, and it is generated from the wrong field.

Workaround, if it is deployed as-is: avoid wildcards in `spec.tls[].hosts` for anything Forecastle
should discover, and list the concrete hostname there as well as in the rules. That duplicates
information, which is exactly why the note calls the bug ridiculous.

**Stakater maintain it** alongside Reloader and other cluster utilities, and the issues have been
open long enough that the behaviour should be treated as current rather than as pending a fix.

---

[← Dashboard ingress](../README.md)
