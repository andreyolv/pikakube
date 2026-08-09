[← Workload identity](../README.md)

# Athenz

<https://github.com/AthenZ/athenz>

---

## The problem it solves

Athenz is Yahoo's (now Yahoo/Verizon Media, and a CNCF sandbox project) open-source system for
**service identity and role-based authorization**, built and battle-tested at very large scale
before SPIFFE existed.

It is unusual in this folder because it spans both halves of
[`identity-access/`](../../../README.md) in one product:

| Component | Job |
|---|---|
| **ZMS** — Athenz Management Service | the source of truth: domains, roles, policies, services. This is the authorization half |
| **ZTS** — Athenz Token Service | issues short-lived credentials — **X.509 certificates** and role tokens — to authenticated services |
| **SIA** — Service Identity Agent | runs alongside the workload, obtains and renews its identity certificate |

The identity model is a hierarchical **domain** namespace — `media.news.frontend` — where a
domain owns services, roles and policies together. So "who is this service" and "what may it
do" are answered by the same system, with the same names, in one place.

The mechanics match the argument in [`../README.md`](../README.md): services receive **X.509
certificates**, not stored secrets; those certificates are short-lived and rotated
automatically; identity is bootstrapped from an attested fact — on Kubernetes, the projected
ServiceAccount token; and mTLS between services is the normal mode of communication.

It also predates most of this space. The design choices it made — certificate-based service
identity, short lifetimes, a central policy service — were correct, and are the same ones
SPIFFE later standardised.

## When to use it

- **You are adopting the whole Athenz model**, identity *and* authorization, as a single
  coherent system. Athenz is strongest as a package; picking out only its identity half means
  paying for machinery you do not use.
- **You already run Athenz.** Existing users have a working, proven system and no reason to
  migrate.
- **You need service identity and role-based authorization to share one namespace and one
  administrative model**, rather than composing SPIRE with a separate policy engine.
- **Multi-tenant infrastructure with domain-level delegation.** The domain hierarchy handles
  delegated administration well, which is what it was built for.

## When not to use it

- **Almost always — choose SPIFFE/SPIRE instead.** This is the honest recommendation, and the
  reasons are ecosystem rather than technical:

| | Athenz | SPIFFE/SPIRE |
|---|---|---|
| Standard | one project's model | a **specification** with several implementations |
| CNCF status | sandbox | **graduated** |
| Service mesh integration | limited | Istio, Linkerd and Envoy all speak SPIFFE natively |
| Community and documentation | small, Yahoo-centric | large and growing |
| Cloud integrations | limited | broad |
| Learning material | sparse | plentiful |

  For a platform starting today, [SPIRE](../spire/README.md) is where the ecosystem is, and
  ecosystem is most of the value in an identity standard — the point of an identity is that
  other things recognise it.

- **You only need workload identity.** Athenz brings a full authorization system with it, and
  running ZMS, ZTS and their datastores is significant weight if the policy half is unused.
- **You only need cloud access.** Cloud federation is free and needs none of this.
- **Kubernetes-first environments.** Athenz's Kubernetes integration exists but is not where its
  centre of gravity is; SPIRE's is.

## Notes

**`https://github.com/AthenZ/athenz`** — the project, and the only note recorded for this
folder. Java, Apache-2.0, a CNCF sandbox project, originally from Yahoo.

**No manifests are staged here.** The folder contained only the link. Athenz was catalogued as
an option and not taken further, which is consistent with the assessment above.

Its value in this repository is comparative rather than practical: Athenz is the clearest
example of the **combined identity-and-authorization** approach, where one system owns both
"who is this service" and "what may it do". Everything else in this folder splits the two —
SPIRE issues identities and leaves authorization to something else, cloud federation issues
identities and leaves authorization to cloud IAM.

That split is the more common design today and is generally the better one, for the usual
reason a separation of concerns is better: the identity layer and the policy layer have
different lifecycles, different owners and different rates of change. But the combined approach
is not wrong, and seeing it makes the split a deliberate choice rather than an assumption. The
same trade-off appears again in
[`authorization/application/`](../../../authorization/application/README.md), where OpenFGA and
Permify answer permission questions for identities they do not issue.

---

[← Workload identity](../README.md)
