[← Toolchain](../README.md)

# downloadkubernetes

<https://github.com/kubernetes-sigs/downloadkubernetes>

Site: <https://downloadkubernetes.com>

---

## The problem it solves

The narrowest tool in this folder, and it is worth reading precisely because of how narrow it is.

Kubernetes binaries are published to `dl.k8s.io` under a URL that is entirely predictable once you
know it:

```
https://dl.k8s.io/release/v1.30.2/bin/linux/amd64/kubectl
```

Four variables — version, OS, architecture, binary — and a shape nobody remembers between the two
times a year they need it. So the actual behaviour is to search for it, land on a page that
suggests `curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/…"`,
and either take whatever `stable.txt` says today or hand-edit the version in a URL you are not sure
of.

downloadkubernetes is a **static site that turns those four variables into a picker.** Choose
`linux` / `arm64` / `v1.33.x`, and it lists every binary the release publishes with a direct link
and a copyable `dl.k8s.io/…` string.

It is a **kubernetes-sigs** project, Apache 2.0, and there is nothing to install: the published
artefact is HTML, CSS and JavaScript, regenerated offline by an `update-index` command and served
from Netlify. There is no CLI and no agent.

## The part that is actually worth knowing

Not the picker. **Every listed binary comes with its checksum, its signature and its certificate.**

That is the difference between this and a bookmarked URL pattern, and it is the reason this page
belongs in a repository that has a
[`supply-chain/signing-artifacts/`](../../../../security/0-governance/supply-chain/signing-artifacts/README.md)
folder. Kubernetes signs its release binaries with [Sigstore](../../../../security/0-governance/supply-chain/signing-artifacts/cosign/README.md)
— keyless, with the certificate and the transparency-log entry published alongside the artefact —
and the overwhelming majority of `kubectl` installations verify none of it, because doing so means
knowing three more URLs than the one you already could not remember.

Putting the four files next to each other makes verification a copy rather than a research task:

```bash
VERSION=v1.33.0 OS=linux ARCH=amd64
BASE=https://dl.k8s.io/release/$VERSION/bin/$OS/$ARCH

curl -LO "$BASE/kubectl" -LO "$BASE/kubectl.sha256" \
     -LO "$BASE/kubectl.sig" -LO "$BASE/kubectl.cert"

echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check

cosign verify-blob kubectl \
  --signature kubectl.sig --certificate kubectl.cert \
  --certificate-identity krel-staging@k8s-releng-prod.iam.gserviceaccount.com \
  --certificate-oidc-issuer https://accounts.google.com
```

The second command is what people do. The third is what almost nobody does, and this page is the
cheapest available nudge towards it.

It also covers more than `kubectl`: `kubeadm`, `kubelet`, `kube-proxy`, `kube-apiserver`,
`kube-controller-manager`, `kube-scheduler`, `kubectl-convert`, and the smaller ones. That matters
for a **[bare-metal or self-managed cluster](../../../../platform-engineering/kubernetes/on-premise/README.md)**,
where you are fetching node and control-plane components rather than one client binary, on more than
one architecture, and the download URL is being written into an automation script that will run
unattended for a year.

## When to use it

- **finding the exact URL for a specific version, OS and architecture**, without guessing — including
  the architectures nobody memorises: `arm64`, `ppc64le`, `s390x`
- when you need the **checksum, signature and certificate** and would otherwise skip verification
  because locating them is friction
- **pinning a version deliberately**, instead of taking whatever `stable.txt` resolves to on the day
  the script runs
- assembling the binary list for a **self-managed control plane or node image**, where several
  components have to match one version
- an air-gapped or restricted host, where the job is "produce the correct URL here so it can be
  mirrored there"

## When not to use it

- **as a toolchain manager.** It downloads nothing on your behalf, installs nothing, manages no
  `PATH` and records no version anywhere. Everything in
  [`../README.md`](../README.md) about declaring tools in a committed file is untouched by it
- when the answer is `latest stable` and you genuinely do not care — `stable.txt` is one line and
  needs no page
- **for anything that is not a Kubernetes release binary.** For the surrounding tool list — `helm`,
  `kind`, `flux`, `jq` — the broader acquisition tool is [arkade](../arkade/README.md)
- in CI. A pipeline should not resolve a download by clicking; pin the version in the workflow. On
  GitHub Actions that is [`setup-kubectl`](../../../../devops/cicd/github-actions/setup-kubectl/README.md)
- if you have already decided the tool version belongs in a committed file, which is the position
  this folder argues for — then the file is the source of the version and this page is at most where
  you looked it up once

## Notes

**Honest framing: this is a lookup table with a UI, and that is the whole product.** Filing it beside
[mise](../mise/README.md) and [devenv](../devenv/README.md) would be a category error, so it is filed
beside [arkade](../arkade/README.md) instead, in the **acquisition** half of this folder rather than
the **declaration** half — see [`arkade/`](../arkade/README.md#where-it-sits-among-the-tools-in-this-folder)
for that split. The two acquisition tools then differ on breadth: arkade covers ~200 tools and
fetches them; downloadkubernetes covers one project's release artefacts and only tells you where
they are.

**The kubectl version skew rule is the reason to pin at all.** `kubectl` is supported within one
minor version of the API server in either direction. A workstation that always takes `stable.txt`
will eventually be two minors ahead of a cluster that has not been upgraded, and the failure is not
a clean error message — it is a resource type that serialises slightly differently, or a subcommand
that is silently gone. Anyone working across clusters at different versions needs *several* pinned
`kubectl` binaries, which is a version-manager problem this page merely feeds.

**Where this fits in pikakube: a reference, and a pointed one.** The toolchain here is pinned in
[`devbox.json`](../../../../../devbox.json), which is the right mechanism and already covers
`kubectl`. What this page exposes is the gap that pinning does not close: **nothing in this
repository verifies a downloaded binary's signature**, and the security tree has a whole
[`supply-chain/`](../../../../security/0-governance/supply-chain/README.md) capability arguing that
it should. The check is four commands and it applies to the tools this platform is operated with,
not only to the images it runs. That is the takeaway worth keeping from a static site with 127
stars.

---

[← Toolchain](../README.md)
