[← Multi-tenancy](../README.md)

# Capsule

<https://github.com/projectcapsule/capsule>

---

## The problem it solves

Capsule introduces a `Tenant` resource. A tenant has owners, and those owners can create their own
namespaces — as many as they are allowed — with quotas, network policies, allowed registries,
ingress hostnames and storage classes applied automatically to every namespace they create.

The problem it addresses is real: Kubernetes RBAC cannot express "this user may create namespaces,
but only with this prefix, and each one must carry this quota". Capsule enforces that through
admission webhooks, giving teams self-service namespace creation without giving them the cluster.

## When to use it

- Many teams needing self-service namespaces without a ticket to the platform team
- Policy that must be applied uniformly to every namespace a tenant creates
- Soft multi-tenancy — colleagues, not adversaries
- A flat tenant model, as opposed to the hierarchy [HNC](../hierarchical-namespaces/README.md) provides

## When not to use it

- Hard multi-tenancy; the kernel and the API server are still shared
- Tenants needing their own CRDs or Kubernetes version — that is [vcluster](../vcluster/README.md)
- **Without testing the webhook failure path first.** See below
- Small clusters with few teams, where namespaces and RBAC are already sufficient

## Notes

**Chart** `capsule` from the project's Helm repository, with a namespace manifest and empty values.

### The recorded failure

The original note, translated, is a warning rather than a description: *"careful with this rubbish,
it breaks the cluster."* And the error it produced:

```
Error from server (InternalError): Internal error occurred: failed calling webhook
"owner.namespace.capsule.clastix.io"
could not get REST client: unable to load root certificates: unable to parse bytes as PEM block
```

Read that message carefully, because it explains the whole failure:

- `failed calling webhook "owner.namespace.capsule.clastix.io"` — this is Capsule's **namespace
  ownership** webhook. Every namespace create and update passes through it.
- `unable to load root certificates: unable to parse bytes as PEM block` — the API server could not
  validate the webhook's TLS certificate. The CA bundle in the `ValidatingWebhookConfiguration` was
  missing, malformed, or out of step with the certificate the webhook pod was serving.
- The result is not a Capsule outage. It is **every namespace operation in the cluster failing**,
  because the API server cannot get an answer from a webhook whose failure policy says to reject.

This is the canonical admission-webhook failure, and it is worse than it first sounds: the operations
you would reach for to fix it — creating a namespace, reinstalling into one — are the operations that
are broken.

**The escape route**, worth knowing in advance rather than discovering under pressure:

```sh
kubectl get validatingwebhookconfiguration
kubectl delete validatingwebhookconfiguration <capsule webhook>
```

Deleting the webhook configuration removes it from the request path immediately and restores normal
operation. It also disables the tenancy enforcement, which is the correct trade while the cluster is
broken.

**Why it happens.** Capsule generates its own certificates and patches the CA bundle into the webhook
configurations. If that patching does not complete, if the certificate expires, or if the controller
is reinstalled while old webhook configurations remain, the API server holds a CA bundle that does not
match the served certificate. Reinstallation that leaves stale `ValidatingWebhookConfiguration`
objects behind is the most common route in.

**Before deploying this anywhere real:** stop the Capsule pods on a disposable cluster and try to
create a namespace. Whatever happens is what will happen in production the day the certificate
rotation fails. If the answer is unacceptable, scope the webhook to exclude system namespaces, or
reconsider `failurePolicy` — knowing that relaxing it means the policy can be bypassed whenever the
controller is down.

The tool is not bad. This failure is inherent to enforcing policy through admission, and Capsule is
simply where it was hit and recorded.

---

[← Multi-tenancy](../README.md)
