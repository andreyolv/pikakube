[← Dashboards](../README.md)

# Meshery

<https://github.com/meshery/meshery>

---

## The problem it solves

Meshery is not a cluster dashboard, despite living in this folder. It is a **service mesh management
plane**: install and configure Istio, Linkerd, Consul, Cilium and others through one interface,
compare their behaviour, run conformance and performance tests against them, and design
infrastructure visually as "designs" that can be applied to clusters.

Its distinguishing claim is being mesh-agnostic. Where each mesh ships its own console, Meshery sits
above them and treats the mesh as a pluggable component.

## When to use it

- Evaluating several service meshes and wanting a like-for-like comparison
- Managing more than one mesh across a fleet
- Performance-testing a mesh's overhead with a repeatable harness
- Visual design of infrastructure topologies, if that workflow suits the team

## When not to use it

- You have no service mesh, and no plan to have one — then it does nothing for you
- One mesh, already chosen; its own tooling is more direct and better documented
- You wanted a cluster dashboard; this is a much larger and differently-shaped thing
- Small clusters, where a mesh itself is likely the wrong call

## Notes

**Chart** `meshery` version `0.7.169` from `https://meshery.io/charts/`, with a namespace manifest.
Recorded as a link only, with no evaluation.

**Its placement in `dashboards/` is the thing worth flagging.** Meshery has a web UI, which is
presumably how it landed here, but the comparison set is wrong: it is not an alternative to
[Headlamp](../headlamp/README.md) or [Skooner](../skooner/README.md). It manages service meshes.
Someone looking for a cluster console and installing this will get a large multi-component system
that does not answer their question.

A more natural home would be alongside networking and service-mesh material rather than beside
single-cluster consoles. Left where it was recorded, with the mismatch stated.

**Two practical cautions**, since the folder has none:

- **It is not small.** Meshery deploys a server, a broker and adapters per mesh. The footprint is
  closer to a platform component than to a dashboard, and it wants to be run continuously rather than
  port-forwarded when needed.
- **It manages meshes, which means it changes them.** Giving it the access required to install and
  reconfigure a service mesh across clusters is a significant grant — a mesh controls all
  service-to-service traffic, so write access to its configuration is write access to the network.

Version `0.7.169` reflects a fast release cadence, which cuts both ways: active development, and a
moving target for pinning.

---

[← Dashboards](../README.md)
