[← Workload identity](../README.md)

# autocert

<https://github.com/smallstep/autocert>

---

## The problem it solves

You want mTLS between services. You do not want a service mesh, and you do not want to adopt
the SPIFFE model. autocert is the small answer: **a mutating webhook that injects a
certificate into a pod**.

Annotate a pod with a name, and autocert:

1. Intercepts pod creation through the admission webhook.
2. Requests a certificate from **step-ca** — the private CA already documented in
   [`certificates/step-ca/README.md`](../../../../certificates/step-ca/README.md) — for the
   name in the annotation.
3. Injects an **init container** that fetches the certificate before the application starts, and
   a **sidecar** that renews it continuously.
4. Mounts the certificate, key and root bundle into the pod at a known path.

The application reads two files and does mTLS. It needs no library, no SDK, no awareness of any
of this, and no change to its code.

| Property | autocert |
|---|---|
| Credential in the pod | a short-lived X.509 certificate — hours to days |
| Rotation | automatic, by the renewer sidecar |
| Stored secret | none; the certificate is requested at pod start |
| Application changes | none, if it can already load a certificate from disk |
| Identity model | a DNS-style name, from the annotation |
| Depends on | step-ca |

It is the same idea as everything else in this folder — **credentials issued at runtime against
an attested fact, short-lived, rotated automatically** — with the narrowest possible scope. What
it attests is thin: the annotation is checked against the webhook's configuration, and the trust
comes from the fact that only the admission controller can inject the bootstrap token. That is
weaker than SPIRE's process-level attestation, and it is honest about being so.

## When to use it

- **You want pod-to-pod mTLS and nothing else.** No mesh, no sidecar proxy, no SPIFFE
  vocabulary — just certificates in pods.
- **You already run step-ca.** autocert is smallstep's own component, and the integration is
  direct. If step-ca is the platform's private CA, this is a natural extension of it.
- **Applications already speak TLS from files.** Most databases, brokers and servers do. Kafka,
  Postgres and Elasticsearch all take a certificate path in their configuration, and that is
  exactly what autocert provides.
- **A service mesh is too much.** The mesh gives you mTLS plus traffic management, observability
  and policy — and the operational weight of all of it. If the requirement is only mTLS, this is
  a much smaller commitment.
- **Non-HTTP workloads.** Meshes are strongest with HTTP; a certificate in a file works for any
  protocol that speaks TLS.

## When not to use it

- **A service mesh is already deployed.** Istio and Linkerd already issue identities and do mTLS
  transparently. Adding autocert means two certificate lifecycles in the same pods.
- **You need SPIFFE semantics.** SPIFFE IDs, federation between trust domains, the Workload API,
  and attestation based on what the platform can observe rather than on an annotation — all of
  that is [SPIRE](../spire/README.md). If identity has to extend beyond the cluster or across
  organisations, this is not it.
- **You need to reach a cloud service.** Certificates do not help; cloud federation does — see
  [`../README.md`](../README.md) §4.
- **You do not want step-ca.** autocert is not a general-purpose certificate injector; it is
  step-ca's admission-time client.
- **Certificates need to be issued to things other than pods.** VMs, CI runners and devices are
  step-ca's own territory directly, not autocert's.
- **Project activity matters to you.** autocert is a small, stable and lightly maintained
  project. Check its current state before building a platform on it — smallstep's own emphasis
  has shifted toward its broader certificate management offering.

One thing worth naming clearly: **cert-manager is the more common answer to "certificates in
Kubernetes"**, and it overlaps here. The difference is granularity. cert-manager issues a
`Certificate` into a Secret, which a Deployment then mounts — one certificate per Secret,
declared as a resource. autocert issues **per pod, at admission time**, with no Secret and no
resource to declare. For workload identity, per-pod matters; for a server certificate on an
Ingress, cert-manager is the right tool. They are not competitors so much as different
granularities of the same operation, and the whole comparison is laid out in
[`certificates/README.md`](../../../../certificates/README.md).

## Notes

**`https://github.com/smallstep/autocert`** — the project, and the only note recorded for this
folder. From smallstep, the same people as `step-ca` and the `step` CLI.

**No manifests are staged here.** The folder contained only the link — autocert was catalogued
as an option and not taken further.

Three things worth knowing if it ever is:

- **It requires step-ca to be running first**, with a provisioner configured for autocert to
  use. The dependency direction is one-way and absolute.
- **The annotation is the identity.** `autocert.step.sm/name: service.namespace.svc.cluster.local`
  determines what the certificate is issued for. Whoever can set pod annotations can therefore
  request a certificate for any name the CA will sign — which makes the CA's provisioner policy
  the actual security boundary, not the annotation. Constrain what names the provisioner will
  issue.
- **The renewer is a sidecar**, so it shares the pod's lifecycle. A pod that runs for weeks keeps
  renewing; a pod that is evicted takes its certificate with it, which is the correct behaviour
  and worth understanding when reading the CA's issuance logs.

For this platform, the relevant observation is that the private-CA groundwork is already
documented in [`certificates/`](../../../../certificates/README.md), and step-ca is catalogued
there. If pod-to-pod mTLS ever becomes a requirement here without a mesh, autocert is the
lightest path from that existing groundwork to certificates in pods.

---

[← Workload identity](../README.md)
