[← Development](../README.md)

# Garden

<https://github.com/garden-io/garden>

---

## The problem it solves

Garden is the most ambitious tool in this folder, and the ambition is the trade-off. It models the
repository as a **dependency graph of actions** — build, deploy, test, run — and caches results
across that graph. A change to one service rebuilds only what depends on it; tests that nothing
touched are skipped because their inputs are unchanged.

So it is not only an inner-loop tool. It aims to be the thing that runs locally *and* in CI, with
the same graph and the same cache, so that "it passed locally" means something.

## When to use it

- A monorepo where integration tests between services are a routine part of development
- CI is slow because it rebuilds and retests everything unconditionally
- You want one definition of build/deploy/test rather than three
- The team is willing to model the repository, not just point a tool at it

## When not to use it

- A single service — the graph is overhead with nothing to cache
- You want to try a tool in an afternoon; Garden asks for modelling up front
- The build system already caches well (Bazel, Nx, Turborepo) — the overlap is large
- You only wanted a file watcher

## Notes

Recorded as a link only:

```
https://github.com/garden-io/garden
```

Known, not evaluated.

The reason to keep it on the list despite that: Garden is the only tool here that treats **tests**
as part of the loop. Everything else stops at "your code is running in the cluster"; Garden's model
extends to "and the integration tests that depend on it have been re-run, and the ones that do not
were skipped". That is a different product to Skaffold, filed in the same folder because it
answers the same question on the way past.

Licensing is worth checking before adoption — the project has moved between models, and the
caching that makes it attractive at scale has historically been the part tied to the commercial
offering.

---

[← Development](../README.md)
