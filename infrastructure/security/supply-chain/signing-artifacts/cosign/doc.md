https://github.com/sigstore/cosign
https://github.com/sigstore/cosign-installer
https://github.com/sigstore/gh-action-sigstore-python

https://github.com/sigstore/rekor
https://github.com/sigstore/fulcio

LOCAL
cosign generate-key-pair

SIGN
cosign sign --key cosign.key docker.io/andreyolv/flink@sha256:1badb98e146ca63e9c92947dae5c9a0ba535e4bc3f9d57167845f4a3b325510f

VERIFY
cosign verify --key cosign.pub docker.io/andreyolv/flink:1.0@sha256:1badb98e146ca63e9c92947dae5c9a0ba535e4bc3f9d57167845f4a3b325510f
