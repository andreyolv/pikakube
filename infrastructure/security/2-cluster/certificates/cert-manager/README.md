# cert-manager

<https://github.com/cert-manager/cert-manager>
<https://cert-manager.io/docs/>

Declarative certificate issuance on Kubernetes. You write a `Certificate`, it produces and
renews a `Secret`.

Concepts, issuer types and comparison against the other tools: [../README.md](../README.md)

---

## Status

Done:

- Integrated with Linkerd through a `selfSigned` ClusterIssuer, plus `Issuer` and `Certificate`.
- Because the ClusterIssuer is `selfSigned`, no external CA is required for the certificates to be created — it signs with the certificate's own key, which is the standard way to bootstrap a private CA root.

## Examples in this folder

| Path | What it shows |
|---|---|
| `examples/selfsigned/` | `selfSigned` ClusterIssuer, Issuer and Certificate — the bootstrap chain |
| `examples/ca/` | `Issuer` of type `ca`, signing from a key pair stored in a Secret |
| `examples/selfsigned-linkerd/` | the Linkerd integration described above |
| `examples/my-domain/` | ClusterIssuer plus a full Deployment/Service/Ingress using the certificate |
| `examples/hashicorp-vault/` | `Issuer` delegating issuance to Vault |
