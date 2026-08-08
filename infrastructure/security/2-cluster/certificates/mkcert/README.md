# mkcert

<https://github.com/FiloSottile/mkcert>

Creates a local private CA **and installs its root into the machine's trust store**
(`mkcert -install`). That second step is the actual product — it is why the browser shows a
green padlock immediately, with no warning.

Scope and limits versus cert-manager and step-ca: [../README.md](../README.md)

> Development only. The CA lives in your home directory — it is neither rotatable nor
> auditable, and it produces static files with no renewal. What runs *inside* the cluster is
> cert-manager + trust-manager territory.

---

## Windows

Open PowerShell as administrator.

First install Chocolatey — <https://chocolatey.org/install#individual>

```powershell
Set-ExecutionPolicy AllSigned
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco

choco install mkcert

mkcert -install

cd $HOME\Downloads

mkcert "*.127.0.0.1.nip.io"

mv _wildcard.127.0.0.1.nip.io.pem cert.pem
mv _wildcard.127.0.0.1.nip.io-key.pem key.pem
```

The `*.127.0.0.1.nip.io` wildcard covers every service in the cluster with a single
certificate — see the nip.io rationale in [../README.md](../README.md).

## Linux

```bash
cp /mnt/c/Users/Andrey/Downloads/cert.pem .
cp /mnt/c/Users/Andrey/Downloads/key.pem .

kubectl -n ingress-nginx create secret tls mkcert-tls-secret \
  --cert=cert.pem \
  --key=key.pem \
  --dry-run=client -o yaml > mkcert-tls-secret.yaml
```

Check the expiry dates of the certificate already stored in the cluster:

```bash
kubectl get secret mkcert-tls-secret -n ingress-nginx -o jsonpath="{.data['tls\.crt']}" | base64 -d | openssl x509 -noout -dates
```
