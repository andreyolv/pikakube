https://github.com/sigstore/cosign
https://github.com/sigstore/cosign-installer


LOCAL
cosign generate-key-pair

GITHUB
export GITHUB_TOKEN=xxxxxxxxxxxx
cosign generate-key-pair github://andreyolv/plumbers

KUBERNETES
cosign generate-key-pair k8s://cosign/testsecret

SIGN
cosign sign --key cosign.key docker.io/andreyolv/flink@sha256:1badb98e146ca63e9c92947dae5c9a0ba535e4bc3f9d57167845f4a3b325510f

VERIFY
cosign verify --key cosign.pub docker.io/andreyolv/flink:1.0@sha256:1badb98e146ca63e9c92947dae5c9a0ba535e4bc3f9d57167845f4a3b325510f

Docs:
https://gist.github.com/vfarcic/d1bd7ab00d2288c663e436cd513efe85
https://kyverno.io/docs/writing-policies/verify-images/sigstore/
https://github.com/vfarcic/silly-demo/blob/master/cosign/kyverno.yaml
https://github.com/marketplace/actions/cosign-installer
https://github.com/sigstore/cosign-gatekeeper-provider

https://gist.github.com/vfarcic/d1bd7ab00d2288c663e436cd513efe85
https://anaisurl.com/trivy-cosign-kyverno/

