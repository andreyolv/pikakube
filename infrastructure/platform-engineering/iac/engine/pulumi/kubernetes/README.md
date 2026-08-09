[← Pulumi](../README.md)

# pulumi-kubernetes

<https://github.com/pulumi/pulumi-kubernetes>

---

## The problem it solves

`pulumi-kubernetes` exposes the Kubernetes API as classes in a programming language. A `Deployment`
becomes an object constructed in Python or TypeScript, and Pulumi applies it to a cluster and records
it in state. It can also render Helm charts and Kustomize overlays into the same graph, so a whole
manifest tree can be produced by code.

The pitch is that manifests stop being YAML: types are checked, values are computed rather than
templated, and the output of a cloud resource can be passed directly into a Deployment's environment
without a copy step.

The recorded reaction to that pitch, in full:

> **"Why would anyone want to use this?"**

## When to use it

- an existing Pulumi program provisions the cluster **and** a small number of bootstrap objects have
  to exist before any in-cluster reconciler does — the CNI, the GitOps controller itself
- a single tool for cloud and cluster is a hard requirement and the reconciliation loop is genuinely
  not wanted
- values must flow from cloud resources into Kubernetes objects at apply time and no secrets
  controller is available to do it

That list is short, and the honest summary is that the first item is the only one this repository
would defend.

## When not to use it

- **for anything a GitOps controller can reconcile**, which is nearly everything. This is a push
  model with a state file, replacing a pull model that self-heals
- for application manifests, which belong in Git and be reconciled from there — see
  [`gitops/`](../../../../gitops/README.md)
- when the alternative is Helm or Kustomize, which are what the cluster's own ecosystem expects and
  what every controller in this repository consumes
- when nobody wants a state file to be authoritative about objects the API server already stores

## Notes

The original note was the project link, one command, and a question with five question marks:

- <https://github.com/pulumi/pulumi-kubernetes>

```sh
pip install pulumi-kubernetes
```

> **"Why would anyone want to use this?????"**

### Why the objection is right

The reaction is worth unpacking, because it is the sharpest opinion in
[`iac/`](../../../README.md) and it is not just distaste.

Kubernetes already has a state store, a declarative API and controllers that continuously reconcile
toward the declared state. Managing Kubernetes objects with an external engine adds a **second**
record of intent — the Pulumi state file — that is authoritative only between applies, and that has
to be reconciled with an API server which is itself being changed by controllers, HPAs, admission
webhooks and operators.

The failure modes follow directly:

- **Drift is not corrected.** Something changes a Deployment; nothing notices until the next
  `pulumi up`, run by a person.
- **Two writers.** If a GitOps controller also manages the object, they fight. If it does not, the
  cluster now has two deployment mechanisms and two mental models.
- **Push, from outside.** Applying requires credentials for the cluster wherever the program runs,
  which is the credential argument in [`gitops/`](../../../../gitops/README.md) section 2, in
  reverse.
- **State can disagree with reality.** An HPA changing `replicas` becomes a diff Pulumi wants to
  revert.

The same objection applies to Terraform's Kubernetes provider, and it is the anti-pattern named in
[`iac/`](../../../README.md) section 6. This folder is where it was met in person.

### The example

```python
deployment = Deployment(
    "nginx",
    spec={
        "selector": { "match_labels": app_labels },
        "replicas": 1,
        "template": {
            "metadata": { "labels": app_labels },
            "spec": { "containers": [{ "name": "nginx", "image": "nginx" }] }
        },
    })

pulumi.export("name", deployment.metadata["name"])
```

Nested dictionaries in the exact shape of the YAML. The typed argument classes are imported at the
top of the file and then not used, which is telling: written this way, the program is YAML with
Python punctuation and none of the type safety that was the reason to leave YAML. It is a fair
illustration of the complaint.

`image: "nginx"` is unpinned, and `replicas: 1` next to an HPA would be the drift problem in its
simplest form.

### The narrow case where it is defensible

There is one. Something has to create the objects that exist before a reconciler does — the GitOps
controller itself, in a cluster provisioned by the same program. That is the bootstrap problem from
[`iac/`](../../../README.md) section 1, it is small, and it ends the moment the controller starts.

This platform solves that differently: the [flux-operator](../../../../gitops/flux/flux-operator/README.md)
installs Flux from a `FluxInstance`, and everything after it reconciles from Git. Which is the
answer to the recorded question — for this repository, nobody would want to use this.

---

[← Pulumi](../README.md)
