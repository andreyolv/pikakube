[← Check deprecated APIs](../README.md)

# kube-no-trouble

<https://github.com/doitintl/kube-no-trouble>

---

## The problem it solves

`kubent` is the fastest answer to "is this cluster safe to upgrade?". Point it at a cluster and it
collects manifests from three sources — the `last-applied-configuration` annotation on live objects,
Helm v3 release metadata, and any files you pass it — then reports every API version that has been
deprecated or removed, and in which Kubernetes release.

One binary, no installation into the cluster, no configuration. That is the appeal: it is the check
you run five minutes before an upgrade meeting, not a system you operate.

## When to use it

- A one-shot readiness sweep of a running cluster before a minor-version upgrade
- Auditing a cluster you have just been handed and know nothing about
- Quick verification after cleaning up manifests, to confirm the findings are gone
- CI, if you want a single binary with no dependencies

## When not to use it

- As the only source of truth for Helm-installed charts — [Pluto](../pluto/README.md) is more thorough there
- When you need to validate against a **specific target version's** API spec — that is [kubepug](../kubepug/README.md)
- On objects created without `kubectl apply`; the last-applied annotation will be missing and they are invisible to that collector
- As a policy engine; the scope is deprecated APIs and nothing else

## Notes

Recorded as a link only:

```
https://github.com/doitintl/kube-no-trouble
```

Known, not run — the same status as the other two tools in this folder.

The limitation worth knowing before trusting a clean report: the live-cluster collector reads the
**`kubectl.kubernetes.io/last-applied-configuration` annotation**. Objects created by a controller,
by `kubectl create`, or through server-side apply may not carry it, and those objects are simply not
examined. A clean `kubent` run means "nothing deprecated in what I could see", which is not the same
sentence.

That is the practical argument for running two of these tools rather than one — they collect from
different places, and the union is closer to the truth than either alone.

Maintained by DoiT. `kubent` is the binary name, and the project name is the joke it sounds like.

---

[← Check deprecated APIs](../README.md)
