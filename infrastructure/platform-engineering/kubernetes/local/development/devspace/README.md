[← Development](../README.md)

# DevSpace

<https://github.com/devspace-sh/devspace>

---

## The problem it solves

DevSpace is sync-first. Instead of rebuilding an image on every change, it deploys a development
container once, then keeps your local source tree and the container's filesystem in sync
bidirectionally and restarts the process. Feedback is sub-second, because nothing is built.

It also gives you a terminal directly inside that container, which turns the cluster into something
closer to a remote development machine than a deployment target.

## When to use it

- Interpreted languages, where restarting a process is the whole build
- You want a shell in the pod as part of the normal workflow, not as a debugging escape hatch
- The image build is slow enough that a build-based loop is genuinely painful
- Explicit dev/prod config separation appeals — DevSpace pushes you towards it

## When not to use it

- The code being tested must run in the production image; sync mode deliberately does not
- Compiled languages with a heavy build step gain much less from sync
- You need one config that also drives CI; that is [Skaffold's](../skaffold/README.md) strength
- Bidirectional sync makes you nervous — it can, in principle, pull changes back onto your machine

## Notes

Recorded as a link only:

```
https://github.com/devspace-sh/devspace
```

No commands, no example, no verdict. Known, not evaluated.

The thing to keep in mind if it ever is: sync-based loops trade fidelity for speed, and the trade
is invisible until deploy time. The container you develop in has your source mounted into it; the
one that ships has the source baked in at whatever the Dockerfile decided. Anything that depends on
that difference — file permissions, the working directory, files excluded from the build context —
only shows up after the loop is over.

---

[← Development](../README.md)
