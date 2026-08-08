[← API gateway](../README.md)

# Tyk

<https://github.com/TykTechnologies/tyk>
<https://github.com/TykTechnologies/tyk-charts>
<https://tyk.io/docs/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

A full **API management platform** rather than a gateway with plugins. Written in Go, with
its own proxy, and the pieces that turn APIs into products included rather than bolted on:

- **developer portal** — documentation, self-service key issuance, onboarding
- **policies and plans** — quotas and rate limits attached to a plan, not a route
- **analytics per consumer** — who called what, how often, against which plan
- **multi-tenancy** — organisations with separate keys, limits and portals

## When to use it

- APIs are consumed **outside the company**, and onboarding those consumers is a process someone owns
- you need a portal and per-plan analytics without buying an enterprise tier
- multi-tenant API exposure

## When not to use it

- the requirement is routing plus a plugin or two — [Kong](../kong/) has a larger ecosystem and more community material for that shape
- there are no external consumers, in which case none of this applies and an [ingress controller](../../ingress-controller/README.md) is enough

## The distinction against Kong

Kong is a gateway you extend into API management. Tyk is API management that includes a
gateway. Both reach a similar place; the difference shows in what is present on day one and
what has to be assembled.

---

[← API gateway](../README.md)
