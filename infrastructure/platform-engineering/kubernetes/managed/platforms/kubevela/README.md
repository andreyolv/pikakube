[← Platforms](../README.md)

# KubeVela

<https://github.com/kubevela/kubevela>

---

## The problem it solves

KubeVela implements the **Open Application Model**. Instead of a developer writing a Deployment, a
Service, an Ingress, an HPA and a ConfigMap, they describe an `Application` made of **components**
(a web service, a worker, a database) with **traits** attached (scaling, ingress, rollout) and
**policies** for which environments it goes to.

The platform team defines what those components and traits mean — as CUE templates — and the
developer composes them. The abstraction is not fixed by the product; you author it. That is the
distinguishing feature, and it is a genuinely different proposition from a platform that hands you
its own model.

It is a CNCF project.

## When to use it

- A platform team that wants to define reusable abstractions rather than accept someone else's
- Multi-environment delivery where placement and per-environment differences are first-class
- Applications composed of a repeatable set of pieces across many teams
- You want developers to stop copying five manifests and adjusting them slightly

## When not to use it

- Small teams; authoring and maintaining the abstraction is a real, ongoing job
- Where developers already work comfortably with Kubernetes objects
- If nobody will own the component and trait definitions — an unmaintained abstraction is worse than none
- CUE is a hard requirement and an unfamiliar language for most teams

## Notes

**Chart** `vela-core` version `1.9.11` from `https://charts.kubevela.net/core`, with a namespace
manifest and empty values. Recorded as a link only.

Note the chart name: `vela-core` installs the **controller** only. The `velaux` UI and the CLI are
separate. Installing `vela-core` and expecting a console is the common first confusion.

**Why this is the most interesting entry in the folder** despite being link-only: everything else
here decides the abstraction for you. KubeVela gives you the machinery to build one — which is what a
platform team is supposedly for — and then makes you responsible for it. That reframes the question
from "do we accept this product's opinions" to "do we have the capacity to have opinions of our own".

Both answers are legitimate. A three-person team almost certainly does not, and would be better served
by Helm charts everyone can read.

**Two practical cautions:**

- **CUE is the definition language** for components and traits. It is powerful, it is not widely
  known, and the abstractions you write in it become a dependency the whole organisation has.
- **The abstraction must stay ahead of its users.** The first time a team needs something the traits
  do not express, they will either wait for you or bypass the model. An abstraction that is bypassed
  is overhead with no benefit.

The comparison worth drawing is with [kro](../../resource-orchestrator/kro/README.md), which solves a
smaller version of the same problem — bundling resources behind one simple resource — with far less
machinery and no new language.

---

[← Platforms](../README.md)
