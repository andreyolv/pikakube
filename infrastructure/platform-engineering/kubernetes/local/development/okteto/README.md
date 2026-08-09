[← Development](../README.md)

# Okteto

<https://github.com/okteto/okteto>

---

## The problem it solves

`okteto up` takes an existing Deployment and swaps its container for a development container with
your source synced in, then gives you a shell inside it. `okteto down` puts the original back. The
loop is: keep the cluster's networking, service discovery, secrets and config exactly as they are,
and replace only the code.

That framing is the useful part. Where other tools deploy a development version of your service,
Okteto develops **in place**, inside the deployment that already exists and already talks to
everything else.

## When to use it

- The service under development depends on many other in-cluster services
- You want the dev container to inherit the real environment: same secrets, same config, same DNS
- Fast iteration matters more than image fidelity
- A namespace-per-developer model is already how the team works

## When not to use it

- Against a shared cluster where swapping a deployment affects other people — that is an outage, not a loop
- When the code must be exercised in the production image
- If you want only the open-source CLI but keep reaching for platform features; much of the product surface is the hosted offering
- For a purely local kind cluster, where inheriting "the real environment" buys nothing

## Notes

Recorded as a link only:

```
https://github.com/okteto/okteto
```

Known, not evaluated — the same status as most of this folder.

One caution worth writing down before anyone tries it: because `okteto up` mutates a Deployment
that is already running, using it against a cluster managed by GitOps puts it in a fight with the
reconciler. Flux or Argo CD will see the swapped container as drift and revert it, possibly
mid-session. If it is ever used here, it needs either a namespace outside the reconciled tree or
the sync paused for that resource.

---

[← Development](../README.md)
