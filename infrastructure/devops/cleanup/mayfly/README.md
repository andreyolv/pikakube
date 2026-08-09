[← Cleanup](../README.md)

# mayfly

<https://github.com/NCCloud/mayfly>
<https://github.com/NCCloud/charts>

---

## The problem it solves

`ttlSecondsAfterFinished` exists for Jobs. Nothing equivalent exists for anything else. A test
namespace, a temporary Secret, a debugging Deployment, a preview environment's Ingress — all of
these are created with the intention of removing them later, and later never arrives.

mayfly gives **any** Kubernetes resource a lifetime, declared with one annotation:

```
mayfly.cloud.namecheap.com/expire: 5m
```

The controller watches for that annotation and deletes the object when the time elapses. It accepts
durations (`5m`, `24h`) and works on arbitrary kinds, not a fixed list.

It also ships a `ScheduledResource` CRD, which inverts the idea: instead of expiring something that
exists, it **creates** something on a schedule and lets that creation carry its own expiry. The
example in this repository schedules a `Secret` to appear in ten seconds and expire one minute
after it does:

| Field | Value | Meaning |
|---|---|---|
| `spec.schedule` | `10s` | create once, ten seconds from now |
| `spec.schedule` | `2024-12-31T00:00:00Z` | create once, at an exact time |
| `spec.schedule` | `*/20 * * * * *` | create repeatedly, on a cron expression |
| `spec.content` | an embedded manifest | what to create |
| annotation on the embedded manifest | `expire: 1m` | how long the created object lives |

That combination — create on a schedule, expire shortly after — is the piece neither
`ttlSecondsAfterFinished` nor a `CronJob` gives you, because both are about running work rather
than about the lifetime of an object.

## When to use it

- **ephemeral environments** — a preview namespace per pull request that must disappear whether or
  not the pipeline that created it finished cleanly
- temporary elevated access: a `RoleBinding` that expires by construction rather than by someone
  remembering
- short-lived test fixtures, especially resources created by hand during an incident
- anywhere the alternative is "we will clean it up later" written in a ticket

## When not to use it

- for **Jobs**, use `ttlSecondsAfterFinished` — native, no controller, and the field lives with the
  object that created it
- for **completed and failed Pods**, use [kube-cleanup-operator](../kube-cleanup-operator/README.md),
  which understands terminal states; mayfly only understands elapsed time
- for anything whose deletion must be safe rather than punctual. mayfly deletes on a timer, and a
  timer does not know whether the resource became load-bearing after it was annotated
- for production resources generally. An annotation that deletes things is exactly as dangerous as
  it sounds if it is copied into a template

## Notes

Two recorded references: the project, <https://github.com/NCCloud/mayfly>, and the chart
repository, <https://github.com/NCCloud/charts>. Both are maintained by Namecheap's cloud team
(`NCCloud`) — the chart lives in a shared repository rather than in the project itself, which is
why the second link is recorded separately. That is worth noting for a GitOps setup, where the
`HelmRepository` points at the charts repo and not at mayfly.

**Deployed here**, via a Flux `HelmRelease`, with a `ScheduledResource` example under `example/`
demonstrating all three schedule forms and the nested expiry annotation.

The mental model that makes it click: mayfly is a **TTL for objects**, where Kubernetes only gives
you a TTL for finished work. Everything it does could be done by a `CronJob` running `kubectl
delete`, and the reason not to do that is that the intent then lives in a script somewhere instead
of on the resource itself.

---

[← Cleanup](../README.md)
