[← Integration](../README.md)

# Camel K

<https://github.com/apache/camel>
<https://github.com/apache/camel-k>

---

## The problem it solves

Apache Camel is the reference implementation of the **Enterprise Integration Patterns** — content-
based routing, splitters, aggregators, filters, transformations, dead-letter channels — and its
real asset is the **component catalogue**: hundreds of connectors for protocols and systems you do
not want to write a client for. SFTP, JMS, AS2, SOAP, S3, Kafka, mail, databases, dozens of SaaS
APIs.

Camel K takes that and makes it Kubernetes-native. You apply an `Integration` resource containing
a route; the operator builds an image for it and runs it. There is no application to scaffold, no
Java project, no Dockerfile:

```yaml
# apply this, get a running workload
apiVersion: camel.apache.org/v1
kind: Integration
metadata:
  name: helloworld
spec:
  flows:
  - from:
      uri: timer:yaml
      steps:
      - setBody:
          simple: Hello Camel from ${routeId}
      - log: ${body}
```

Two repositories, as the note records: `apache/camel` is the framework and the component
catalogue, `apache/camel-k` is the operator, the CRDs and the Helm chart.

## When to use it

- **the connector already exists.** This is the reason to choose Camel over writing code, and it
  is close to being the only one that matters — if the odd protocol at the far end has a Camel
  component, you have skipped the hard part
- many integrations, changing at a different rate than the services around them
- the EIP vocabulary genuinely fits the problem: splitting a batch, aggregating responses,
  routing by message content
- a Camel estate already exists elsewhere and the routes can be carried across

## When not to use it

- two or three connections between systems you control — a small service is less to own than an
  operator, a build pipeline and a DSL
- nobody on the team knows Camel. The DSL is not the hard part; **debugging it** is, and that
  knowledge tends to live in one person
- you have no registry the operator can push to, and no intention of choosing one — see below
- the requirement is bulk data movement rather than per-message logic — that is
  [`data-streaming/`](../../../data-streaming/README.md)

## Notes

**Camel K builds an image for every Integration**, and that shapes everything about running it.
The operator compiles the route, produces a container image and pushes it to a registry, then runs
that image. So there are two prerequisites before a single route works: in-cluster build capacity,
and **a registry the operator can push to and the kubelet can pull from**.

That is what the committed `IntegrationPlatform` is for:

```yaml
spec:
  build:
    registry:
      address: registry.io
      organization: camel-k
      insecure: true
```

`registry.io` is **a placeholder, not a working address** — nothing builds until it points at a
real registry. `insecure: true` allows a plain-HTTP or self-signed registry, which is fine for an
in-cluster evaluation registry and is the flag to remove for anything else. This repository maps
several registries under `devops/image/oci-registry/` — Harbor, Zot and a plain docker-registry
all have charts — so the work is choosing one and putting its address here.

**The committed example is a timer, deliberately.** `from: timer:yaml` fires on a schedule, sets a
body, and logs it. It touches no external system, which makes it the correct smoke test: if the
log line appears, the operator, the build, the registry push and the pull all worked. Every
failure it can produce is a platform failure rather than an integration failure — which is exactly
what you want to establish first.

**What is deployed here:** chart `camel-k` 2.5.0 from `https://apache.github.io/camel-k/charts`,
in the `camel-k` namespace, with an empty `values` block.

**A note on scope.** The route in the example is trivial, and that is worth remembering when
judging the tool: Camel K's cost is roughly fixed regardless of how many integrations you run, and
its value scales with the number and strangeness of the systems being connected. One hello-world
route makes it look absurdly heavy. Forty routes against SFTP, JMS and a mainframe make it look
cheap. Which of those you are looking at is the decision.

---

[← Integration](../README.md)
