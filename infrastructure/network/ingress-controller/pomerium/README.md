[← Ingress controller](../README.md)

# Pomerium

<https://github.com/pomerium/pomerium>
<https://github.com/pomerium/ingress-controller>
<https://www.pomerium.com/docs>

---

> ## The particularity: it is an identity-aware proxy first
>
> Pomerium sits in `ingress-controller/` because it genuinely **is** one — it registers an
> `IngressClass`, consumes `Ingress` objects and routes HTTP like any other controller.
>
> But that is not where it shines. Every other controller in this folder answers *"where
> does this request go?"*. Pomerium also answers **"who is making it, and are they allowed?"**
>
> It is a controller you choose for **access control**, not for routing. If routing is the
> requirement, [ingress-nginx](../ingress-nginx/README.md) or [Traefik](../traefik/README.md) do it with far
> less to operate.

## The problem it solves

Internal tools — Grafana, Airflow, Kafka UI, Trino — each need authentication. The usual
outcomes are all bad: every tool configured separately for SSO, a shared password, or the
service exposed only over VPN and reachable by anyone already inside.

Pomerium puts authentication and authorisation **in front of the application**, at the
ingress. The application sees an already-authenticated request and needs to know nothing
about identity.

- authenticates against an identity provider — Entra ID, Google, Okta, GitHub, any OIDC
- authorises **per route**, with policy expressed on users, groups and claims
- applies to applications that have no auth of their own, and cannot be modified
- replaces "on the VPN therefore trusted" with a per-request decision — the practical form of zero trust for internal tooling

## When to use it

- internal tools that must be reachable without a VPN, with real access control
- an application with no authentication support that still needs to be restricted
- per-group access without configuring SSO separately in every tool

## When not to use it

- plain HTTP routing — this is a much larger component than the job needs
- for authenticating **end users of a public product**; that belongs in the application or an API gateway
- when [oauth2-proxy](../../../security/2-cluster/identity-access/) already covers it — it is lighter, if you only need authentication and not per-route authorisation policy

## Related capabilities

| Concern | Where |
|---|---|
| SSO and identity providers | [`security/2-cluster/identity-access/`](../../../security/2-cluster/identity-access/) |
| Certificates for the routes it serves | [`certificates/`](../../../security/2-cluster/certificates/README.md) |
| API keys, quotas, rate limiting for APIs | [`api-gateway/`](../../api-gateway/README.md) |

---

## Notes

Generate manifests from the upstream kustomization:

```bash
kubectl apply -k github.com/pomerium/ingress-controller/config/default?ref=v0.28.0 --dry-run=client -o yaml > input.yaml

yq eval '.items[] | "---\n" + to_yaml' input.yaml | kubectl-slice -f - -o ./output
```

Policy by group claim:

```yaml
allow:
  and:
    - claim/groups: 'xxxxxxxxxxxx'
```

Policy on the Ingress, by user:

```yaml
# ingress.pomerium.io/policy: |
#   allow:
#     and:
#     - user:
#         is: xxxxxxxxx
#   deny:
#     and:
#     - user:
#         is: xxxxxxxxxxxxx
```

---

[← Ingress controller](../README.md)
