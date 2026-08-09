[← Development](../README.md)

# Tilt

<https://github.com/tilt-dev/tilt>

---

## The problem it solves

Same loop as Skaffold — watch, build, deploy, stream logs — with two differences that decide
whether it is the right pick.

First, configuration is a `Tiltfile` written in Starlark, a Python dialect. That means the build
graph can have logic in it: conditionals, loops over a list of services, functions. Where Skaffold
has a YAML document, Tilt has a small program.

Second, it ships a **web UI**. With a dozen services in one repository, that UI is the feature: per
service build status, logs, errors and a button to force an update, all in one place instead of one
terminal per service.

## When to use it

- A monorepo with several services you iterate on together
- You want per-service status at a glance rather than a merged log stream
- The build graph needs real logic, not just declarations
- Live-update rules can shortcut a full rebuild for interpreted languages

## When not to use it

- One service — the UI is overhead you will not use
- The team dislikes executable configuration; a `Tiltfile` is code and can grow accordingly
- You want the same config to drive CI; Skaffold is a better fit for that
- Production deployment — as with every tool in this folder, that is GitOps' job

## Notes

Recorded as a link only — no commands, no example, no evaluation:

```
https://github.com/tilt-dev/tilt
```

Read that as "known and not chosen". Given that
[Skaffold](../skaffold/README.md) is the one exercised here, that ordering makes sense: this
repository has single-service examples, and Tilt's advantage only appears once several services
change together.

Worth knowing anyway: Tilt's `live_update` can copy files into a running container and restart the
process — the same trick the sync-first tools use — so the build/sync distinction is not quite
binary. It is opt-in per service, which is the safer way round.

---

[← Development](../README.md)
