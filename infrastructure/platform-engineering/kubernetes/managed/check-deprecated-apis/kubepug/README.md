[← Check deprecated APIs](../README.md)

# kubepug

<https://github.com/kubepug/kubepug>

---

## The problem it solves

The other two tools answer "what in here is deprecated?". kubepug answers a sharper question:
**"will this still exist in version X?"**

It does that by validating against the Kubernetes API definitions for a target version — the
generated API data for the release you are planning to move to — rather than against a list of
known deprecations baked into the tool. So the input is not just your manifests, it is your
manifests *plus the version you are aiming at*, and the output is what breaks on arrival.

It also exists as a `kubectl` plugin, installable through [krew](../../plugins/krew/README.md).

## When to use it

- Planning a specific upgrade — "we are going to 1.33, what breaks?"
- Skipping several minor versions at once, where cumulative removals are the risk
- You want validation against real API definitions rather than a curated deprecation list
- As a `kubectl` plugin, for ad-hoc checks without another binary in the path

## When not to use it

- Scanning Helm releases stored in the cluster — [Pluto](../pluto/README.md) is the tool for that
- A fast, zero-argument sweep; [kubent](../kube-no-trouble/README.md) is quicker to reach for
- Air-gapped, unless the API definitions are fetched in advance
- As a general manifest linter; the scope is API versions

## Notes

Recorded as a link only:

```
https://github.com/kubepug/kubepug
```

Known, not run.

The reason it earns a place next to the other two, rather than being redundant with them: **the
question it answers is version-targeted**. "This API is deprecated" produces a list nobody
prioritises. "These fourteen objects will not apply on 1.33" produces a task with a deadline
attached to it.

That distinction matters most on multi-version jumps, which is exactly when managed clusters force
your hand — providers drop support for old minor versions on their own schedule, and the jump is
often two or three versions rather than one.

Practical pairing: [Pluto](../pluto/README.md) in CI on every change, kubepug once per upgrade
against the target version. They are not competitors so much as different moments.

---

[← Check deprecated APIs](../README.md)
