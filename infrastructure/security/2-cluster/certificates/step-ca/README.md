# step-ca

<https://github.com/smallstep/certificates>
<https://github.com/smallstep/helm-charts>
<https://smallstep.com/docs/step-ca/>

A private certificate authority you operate yourself. Speaks ACME, OIDC and JWK, with
provisioners, policies and auditing.

Where it fits against cert-manager, mkcert and the managed cloud CAs:
[../README.md](../README.md)

---

## When it earns its place

- on-prem or air-gapped environments, where Let's Encrypt is unreachable
- when the CA's clients are **not only Kubernetes** — VMs, devices, CI, mTLS between services outside the cluster
- when very short-lived certificates (hours) with automatic renewal are wanted

## When it does not

If the cluster is the only consumer, a cert-manager `ClusterIssuer` of type `ca` delivers
the same outcome without another stateful service to operate, back up and monitor.

## Common pattern

step-ca as the CA, with **cert-manager as its ACME client**. The two work together rather
than competing — step-ca owns the CA lifecycle, cert-manager owns issuance inside the
cluster.
