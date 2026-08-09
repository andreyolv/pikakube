[← Platforms](../README.md)

# Tsuru

<https://github.com/tsuru/tsuru>

---

## The problem it solves

Tsuru is a Platform-as-a-Service in the Heroku sense: developers `git push`, the platform builds the
application with a buildpack, deploys it, wires up routing, and provides backing services through a
service catalog. Applications, not manifests. `tsuru app deploy`, not `kubectl apply`.

It predates Kubernetes — it was built at Globo.com and ran on its own scheduler — and now uses
Kubernetes as a backend. That history matters: the abstraction was designed to hide a cluster, not to
expose one, so it hides Kubernetes more completely than anything else in this folder.

## When to use it

- You genuinely want Heroku semantics on your own infrastructure
- Many similar applications — twelve-factor web services — deployed by teams that should not think
  about Kubernetes
- A buildpack-based build path is preferable to everyone writing Dockerfiles
- The organisation already has Tsuru experience

## When not to use it

- Workloads that do not fit the twelve-factor shape: stateful systems, jobs, operators, anything
  needing specific scheduling
- Where developers should learn Kubernetes rather than be shielded from it
- If you will need to reach through the abstraction regularly — that is a sign it is the wrong one
- Newer, more Kubernetes-native abstractions such as [KubeVela](../kubevela/README.md) may fit better

## Notes

**Chart** `tsuru` version `0.8.2` from `https://tsuru.github.io/charts`, with a namespace manifest
and empty values. Recorded as a link only.

**The strongest abstraction in the folder, and therefore the strongest trade.** Tsuru does not
present Kubernetes with a nicer interface; it presents a different product. Developers get
applications, environment variables, service bindings and a router, and the Kubernetes objects
underneath are an implementation detail.

That is exactly right when it fits and painful when it does not. The question to ask before adopting
it is not "is the abstraction good" but "what fraction of our workloads fit inside it" — because
anything that does not fit needs a second, parallel way of being deployed, and now there are two
platforms.

**Assess the project's activity before adopting.** Tsuru is long-established with real production
history at scale, and its development community is smaller than that of the CNCF-backed projects
alongside it here. For a platform that would own how every application is deployed, that is a
first-order consideration rather than a footnote.

The closest comparison in this repository is [KubeVela](../kubevela/README.md): both put an
application-shaped model above Kubernetes, but KubeVela lets the platform team define the model while
Tsuru supplies it. Supplied is simpler; defined survives requirements the supplier did not anticipate.

---

[← Platforms](../README.md)
