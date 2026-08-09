[← Resource orchestrator](../README.md)

# kro

<https://github.com/awslabs/kro>
<https://github.com/awslabs/kro/tree/main/examples/webapp>

---

## The problem it solves

Kube Resource Orchestrator. You define a **ResourceGroup** in YAML: a schema for a new custom
resource, and the set of Kubernetes objects an instance of it should expand into. kro generates the
CRD, watches for instances, works out the dependency order from the references between the resources,
and creates and maintains them.

The developer-facing result is a short custom resource — `kind: WebApplication`, a few fields —
backed by a Deployment, Service, Ingress and whatever else the ResourceGroup declares. No controller
code, no Go, no CRD authoring by hand.

It is a joint effort from AWS, Google Cloud and Azure, which is unusual and a meaningful signal about
its intended durability.

## When to use it

- The same set of manifests is copied repeatedly across teams, and the shape has stabilised
- You want the abstraction to be a real API object with status, not a Helm release
- Correct dependency ordering and garbage collection matter — both come from the ownership model
- No appetite for writing and maintaining a controller

## When not to use it

- Installing third-party software; Helm does that well and this does not replace it
- Where real reconciliation logic is needed — backups, failover, external systems: write an
  [operator](../../operators/README.md)
- Before the pattern is known; building an abstraction around a guess is the classic failure
- If the team would rather read plain manifests, which is a legitimate preference

## Notes

**Installed from an `OCIRepository`**, with a namespace manifest, and — the part that makes this
folder useful — **committed examples**:

- `example/resourcegroup.yaml` — the abstraction: the schema of the new kind, and the resources it
  expands into
- `example/instance.yaml` — a use of it

Those two files together are the entire mental model. A `ResourceGroup` is the definition; an
instance is the consumption. Everything else in kro is detail.

**The upstream example** recorded in the notes is
<https://github.com/awslabs/kro/tree/main/examples/webapp> — a web application expanding into a
Deployment, Service and Ingress. It is the canonical illustration, and it is the case nearly every
platform team has hand-rolled at least once.

**Three mechanics worth knowing before writing a ResourceGroup:**

- **Dependency order is inferred, not declared.** If resource B references a field of resource A, kro
  creates A first and waits for the value to exist. That removes the ordering problem that makes
  Helm hooks and `dependsOn` chains unpleasant — and it means an unreferenced dependency is not
  ordered, which occasionally surprises.
- **Instances own their resources.** Kubernetes garbage collection removes the children when the
  instance is deleted. That is the property Helm cannot give you without `helm uninstall`, and it is
  what makes the abstraction feel like a real object.
- **The generated CRD is an API.** Once teams write instances of it, changing the schema breaks them.
  Version it deliberately.

**Project maturity** is the caution. kro is young. The multi-cloud sponsorship suggests it will
continue, and it does not follow that the API is stable yet — pin the version, and expect the
ResourceGroup schema to move.

The comparison worth keeping in mind: [KubeVela](../../platforms/kubevela/README.md) does the same
thing with far more machinery — CUE, traits, policies, an application model and a UI. kro is the
minimal expression of the idea, and for a team that wants one abstraction rather than a platform, the
minimal version is the right one.

---

[← Resource orchestrator](../README.md)
