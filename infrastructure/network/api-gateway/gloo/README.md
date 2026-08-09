[← API gateway](../README.md)

# Gloo

<https://github.com/solo-io/gloo>
<https://docs.solo.io/gateway/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

An **Envoy**-based gateway from Solo.io, aimed at the edge of a cluster with function-level
routing, transformation and strong Envoy integration.

Historically it filled the gap between an ingress controller and full API management: more
than routing, less than a management platform.

## Where the project went

Solo.io donated the open-source line to the CNCF as
[**kgateway**](../../gateway-api/kgateway/README.md), which continues as a Gateway API implementation
with an AI and LLM routing focus. Gloo continues as the commercial product line.

For a new deployment, that redirect matters:

| You want | Go to |
|---|---|
| Open-source Envoy gateway, Gateway API native | [kgateway](../../gateway-api/kgateway/README.md) |
| Commercial Gloo with enterprise support | Solo.io |
| Envoy at the edge, neutral and upstream | [Envoy Gateway](../../gateway-api/envoy-gateway/README.md) |

## When to use it

- there is already a Solo.io relationship or a Gloo deployment to maintain
- you need the enterprise features specifically

## When not to use it

- starting fresh with open source — follow the line to kgateway or Envoy Gateway rather than
  starting on a product tier you will have to migrate off

---

[← API gateway](../README.md)
