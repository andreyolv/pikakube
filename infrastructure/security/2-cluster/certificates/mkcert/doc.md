https://github.com/FiloSottile/mkcert

at WINDOWS open powershell as admin and run:
first install chocolatey https://chocolatey.org/install#individual

Set-ExecutionPolicy AllSigned
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco

choco install mkcert

mkcert -install

cd $HOME\Downloads

mkcert "*.127.0.0.1.nip.io"

mv _wildcard.127.0.0.1.nip.io.pem cert.pem
mv _wildcard.127.0.0.1.nip.io-key.pem key.pem

--------------------
LINUX:

cp /mnt/c/Users/Andrey/Downloads/cert.pem .
cp /mnt/c/Users/Andrey/Downloads/key.pem .

kubectl -n ingress-nginx create secret tls mkcert-tls-secret \
  --cert=cert.pem \
  --key=key.pem \
  --dry-run=client -o yaml > mkcert-tls-secret.yaml

kubectl get secret mkcert-tls-secret -n ingress-nginx -o jsonpath="{.data['tls\.crt']}" | base64 -d | openssl x509 -noout -dates
