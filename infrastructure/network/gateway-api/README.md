[← Network](../README.md)

# Gateway API

Conceptual reference for the `gateway-api/` folder: the **successor to Ingress**, and the
implementations built around it.

Tools covered: [`envoy-gateway`](envoy-gateway/) · [`kgateway`](kgateway/) ·
[`nginx-gateway-fabric`](nginx-gateway-fabric/) · [`kuadrant`](kuadrant/)

## Contents

1. [Where this folder sits](#1-where-this-folder-sits)
2. [Why Ingress was replaced](#2-why-ingress-was-replaced)
3. [The resource model](#3-the-resource-model)
4. [The tools in this folder](#4-the-tools-in-this-folder)
5. [Migrating from Ingress](#5-migrating-from-ingress)
6. [Anti-patterns](#6-anti-patterns)
7. [How this applies to pikakube](#7-how-this-applies-to-pikakube)
8. [References](#references)

---

## 1. Where this folder sits

| Folder | Shines at |
|---|---|
| [`ingress-controller/`](../ingress-controller/README.md) | HTTP entry configured through the `Ingress` API |
| **`gateway-api/`** | tools whose **reason for existing** is implementing the Gateway API |
| [`api-gateway/`](../api-gateway/README.md) | API management — keys, quotas, consumers, portal |

Several controllers in the neighbouring folders also support the Gateway API. What lands
here are the projects built around it first — that is where they shine.

## 2. Why Ingress was replaced

`Ingress` expresses host, path, backend and TLS. Everything else — rate limiting, auth,
timeouts, rewrites, header manipulation, traffic splitting — lives in **vendor-specific
annotations**.

Three consequences drove the replacement:

- **manifests do not port.** Switching controllers means rewriting every Ingress.
- **no validation.** An annotation with a typo is silently ignored; nothing rejects it.
- **one object, many owners.** Cluster operators, platform teams and application teams all edit the same resource, with no way to separate their concerns.

`Ingress` is now **feature-frozen** upstream. It keeps working and is not being removed, but
new capability lands in the Gateway API.

## 3. The resource model

The core idea is **separation by role**, which is what the annotation model could not do:

| Resource | Who owns it | What it declares |
|---|---|---|
| `GatewayClass` | infrastructure provider | which implementation is available |
| `Gateway` | **cluster operator** | listeners, ports, TLS — the entry point itself |
| `HTTPRoute` (also `GRPCRoute`, `TCPRoute`, `TLSRoute`) | **application team** | routing rules, attached to a Gateway |

An application team writes `HTTPRoute` and never touches TLS or listeners. A platform team
owns the `Gateway` and does not review every routing change. That split is the actual
product.

Features that needed annotations are now typed fields: traffic splitting by weight, header
matching and manipulation, request mirroring, timeouts. Typed means **validated at admission**
rather than ignored at runtime.

The API also extends beyond north-south traffic — **GAMMA** applies the same resources to
service mesh configuration, which is why the line between ingress and mesh is blurring by
design. See [`service-mesh/`](../service-mesh/README.md).

## 4. The tools in this folder

| Tool | Data path | Shines when | Detail |
|---|---|---|---|
| **Envoy Gateway** | Envoy | the reference-grade implementation, from the Envoy project itself | [→](envoy-gateway/) |
| **kgateway** | Envoy | Gateway API plus AI and LLM routing — the successor line to Gloo's open-source edge | [→](kgateway/) |
| **NGINX Gateway Fabric** | NGINX | you want NGINX as the data path with the new API | [→](nginx-gateway-fabric/) |
| **Kuadrant** | policy layer | **not a gateway** — adds rate limiting and authz to an existing one via policy attachment | [→](kuadrant/) |

## 5. Migrating from Ingress

**[ingress2gateway](https://github.com/kubernetes-sigs/ingress2gateway)** converts existing
`Ingress` objects into `Gateway` and `HTTPRoute`. It handles the structural translation;
vendor annotations still need manual attention, since that is precisely what has no
equivalent.

Both APIs can run side by side during a migration — different controllers, different
objects, same cluster.

### The CRD distribution problem

> The Gateway API CRDs are **not distributed as a Helm chart**, which is genuinely annoying
> for a GitOps setup where everything else is a `HelmRelease`.

The CRDs live in the API repository and are applied directly:

- standard channel: <https://github.com/kubernetes-sigs/gateway-api/tree/main/config/crd/standard>
- tracking issues: [#1590](https://github.com/kubernetes-sigs/gateway-api/issues/1590) · [#4809](https://github.com/kubernetes-sigs/gateway-api/issues/4809)

In practice this means a separate `Kustomization` for the CRDs, applied before any
implementation, rather than the single `HelmRelease` everything else uses.

## 6. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Installing the implementation before the CRDs | the controller crash-loops on missing types | apply CRDs first, as an ordered dependency |
| Expecting annotations to carry over | that is the entire problem the API set out to fix | translate them to typed fields, or accept the rewrite |
| Migrating everything at once | both APIs coexist happily; a big-bang cutover adds risk for nothing | migrate route by route |
| Treating Kuadrant as a gateway | it is a policy layer attached to one | pair it with an implementation |

## 7. How this applies to pikakube

Not in use — the cluster runs [ingress-nginx](../ingress-controller/ingress-nginx/) with
`Ingress` objects.

This folder is the mapped answer to "what replaces it". The realistic first step on a real
cluster is running `ingress2gateway` against the existing manifests to see how much
translates automatically and how much is annotation-specific.

## References

- [Gateway API](https://github.com/kubernetes-sigs/gateway-api) · [documentation](https://gateway-api.sigs.k8s.io/)
- [Standard channel CRDs](https://github.com/kubernetes-sigs/gateway-api/tree/main/config/crd/standard)
- [ingress2gateway](https://github.com/kubernetes-sigs/ingress2gateway)
- [gateway-api-state-metrics](https://github.com/Kuadrant/gateway-api-state-metrics)
- [GAMMA — mesh configuration](https://gateway-api.sigs.k8s.io/mesh/)

---

[← Network](../README.md)
