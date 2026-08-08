# openssl

<https://github.com/openssl/openssl>
<https://docs.openssl.org/master/man1/>

The cryptographic library nearly everything else uses underneath, plus a CLI.

Not a certificate *management* tool — it is the **inspection and diagnosis** tool. It cuts
across every path in [../README.md](../README.md): when cert-manager, mkcert, step-ca or a
cloud load balancer misbehaves, `openssl` is how you find out why.

> **Where not to use it:** as a process. Generating certificates by hand means manual
> renewal — a scheduled incident. Use it to *understand* certificates, not to operate them.

---

## Inspecting a local certificate

```bash
# full contents
openssl x509 -in cert.pem -noout -text

# validity dates only
openssl x509 -in cert.pem -noout -dates

# the names the certificate is actually valid for
openssl x509 -in cert.pem -noout -ext subjectAltName

# who issued it, and who it was issued to
openssl x509 -in cert.pem -noout -issuer -subject

# is it a CA certificate?
openssl x509 -in cert.pem -noout -ext basicConstraints,keyUsage,extendedKeyUsage
```

## Inspecting a live endpoint

```bash
# what the server actually serves, including the chain it sends
openssl s_client -connect host:443 -servername host </dev/null

# expiry only, without the noise
openssl s_client -connect host:443 -servername host </dev/null 2>/dev/null \
  | openssl x509 -noout -dates

# does the server send the full chain, or only the leaf?
# (a missing intermediate is the classic "works in my browser, fails in curl" bug)
openssl s_client -connect host:443 -servername host -showcerts </dev/null
```

`-servername` sets SNI. Without it you get whatever the default vhost serves, which is a
common source of confusing results on shared ingress.

## Validating

```bash
# validate a chain against a specific CA
openssl verify -CAfile ca.pem cert.pem

# confirm a certificate and a key are the same pair
# (both hashes must be identical — mismatch is the usual cause of
#  "key values mismatch" when loading a TLS Secret)
openssl x509 -noout -modulus -in cert.pem | openssl md5
openssl rsa  -noout -modulus -in key.pem  | openssl md5
```

## Format conversion

Format problems cause a large share of TLS incidents — see the format axis in
[../README.md](../README.md).

```bash
# PEM -> PKCS#12 (for Windows or the JVM)
openssl pkcs12 -export -out bundle.p12 -inkey key.pem -in cert.pem -certfile ca.pem

# PKCS#12 -> PEM
openssl pkcs12 -in bundle.p12 -nodes -out cert-and-key.pem

# DER <-> PEM
openssl x509 -inform der -in cert.der -out cert.pem
openssl x509 -in cert.pem -outform der -out cert.der
```

## In-cluster

```bash
# read a TLS Secret straight out of Kubernetes and check its dates
kubectl get secret <name> -n <namespace> \
  -o jsonpath="{.data['tls\.crt']}" | base64 -d | openssl x509 -noout -dates

# same, but show the SANs — useful when the browser complains about the hostname
kubectl get secret <name> -n <namespace> \
  -o jsonpath="{.data['tls\.crt']}" | base64 -d | openssl x509 -noout -ext subjectAltName
```
