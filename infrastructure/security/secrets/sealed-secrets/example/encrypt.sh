# Usage: encrypt.sh <secret.yaml>
# Needs to have kubeseal cli installed
# kubeseal --cert pub-cert.pem -f secret.yaml -o yaml > sealed-secret.yaml

kubeseal --cert pub-cert.pem <"$1" >"${1%.*}-sealed.yaml" -o yaml