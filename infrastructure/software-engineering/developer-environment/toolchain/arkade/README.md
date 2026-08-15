[← Toolchain](../README.md)

# arkade

<https://github.com/alexellis/arkade>

---

## The problem it solves

Getting a CLI binary onto a machine is a solved problem that nobody has solved the same way twice.
Every tool publishes its own instructions: a `curl | bash` script, a Homebrew tap that lags a
release behind, a `.deb` for one distribution, a GitHub release page with fourteen assets where
picking the wrong one gives you a `darwin/amd64` binary on an ARM laptop. Multiply that by the
twenty tools a platform repository assumes are installed and the result is the undeclared,
per-machine, per-person install ritual that [`../README.md`](../README.md#1-the-problem) opens with.

arkade collapses that into one verb:

```bash
arkade get kubectl helm kind flux
```

It detects OS and architecture, resolves the release, downloads the **statically linked binary**
and puts it in `~/.arkade/bin`. No root, no package manager, no distribution repository, no
container. Roughly 200 tools are described in its catalogue — the Kubernetes ones, plus the
adjacent set (`jq`, `terraform`, `k3s`, `gh`, `yq`) that shows up in the same workflows.

It is MIT-licensed and maintained by Alex Ellis and the OpenFaaS community.

**The second verb is a different tool wearing the same name**, and separating them is the whole of
understanding arkade:

| Verb | What it does | Where it acts |
|---|---|---|
| **`arkade get`** | downloads a CLI binary for your OS and architecture | **your machine** |
| `arkade install` | deploys a Kubernetes app — a Helm chart, a manifest, a bespoke installer — with typed CLI flags instead of a `values.yaml` | **a cluster** |
| `arkade system` | installs system-level packages on a host: Go, containerd, a runner | a server |
| `arkade oci install` | extracts a package from an OCI image to a path | your machine |

`arkade get` is the reason to have it. `arkade install` is the reason to be careful with it, and
that boundary is dealt with in [notes](#notes) below.

## Where it sits among the tools in this folder

arkade answers a question the other four do not ask, which is why it is filed here rather than
compared against them:

| Question | Answered by |
|---|---|
| **How does this binary get onto this machine, right now?** | **arkade** (or, for Kubernetes release binaries only, [downloadkubernetes](https://github.com/kubernetes-sigs/downloadkubernetes)) |
| Which tools exist in this repository, at which versions, for everyone? | [mise](../mise/README.md), [devenv](../devenv/README.md), [flox](../flox/README.md), [Devbox](../../../../platform-engineering/kubernetes/local/linux/virtual-enviroment/devbox/README.md) |

That is **acquisition versus declaration**, and they are not competing answers to one question.

An acquisition tool is imperative and stateless: you run a command, a binary appears, and nothing
records that it happened. Ask "what version of `helm` is this repository built against" a month
later and arkade cannot tell you — it never claimed to. A declaration tool commits a file, and the
file is the answer.

The practical consequence: **arkade is excellent for the machine and wrong as the repository's
answer.** A `devbox.json` or a `mise.toml` is what makes two developers agree; `arkade get` is what
gets you unstuck on a fresh laptop, a jump host, or a container where installing a Nix store to
obtain one binary is absurd.

They also compose in the direction you would expect and not the other: a declared environment can
shell out to arkade for the two tools its catalogue lacks, but arkade cannot pin what a declared
environment pins.

## When to use it

- **a fresh machine, or a machine you do not own** — a bastion, a colleague's laptop, a support
  session — where the goal is a working `kubectl` in thirty seconds and nothing else
- **inside a container image or a CI step**, where `arkade get --path /usr/local/bin` replaces a
  column of hand-written `curl | tar | mv` lines that each need their own URL, checksum and
  architecture switch
- **tools with no good distribution story**: the ones whose install instructions are a shell
  pipeline from a personal domain. arkade's catalogue entry is not a stronger trust claim, but it is
  a single, auditable one instead of twenty different ones
- **workshops, demos and onboarding**, which is the case it was built for — the OpenFaaS lineage is
  visible and it shows in how little context it assumes
- when you want a binary **without root and without a package manager**, which is the situation on
  most locked-down or minimal hosts

## When not to use it

- **as the repository's toolchain definition.** It has no lock file and no manifest. Everyone runs
  the same command on a different day and gets a different version, which is the
  [`latest` everywhere anti-pattern](../README.md#8-anti-patterns) with a nicer interface. This
  repository already declares its toolchain in
  [`devbox.json`](../../../../../devbox.json) — replacing that with `arkade get` would be a
  regression
- **`arkade install` in a GitOps repository.** This is the one to be firm about: it installs charts
  into a cluster imperatively, from a laptop, with no record in Git. Everything in
  [`platform-engineering/gitops/`](../../../../platform-engineering/gitops/README.md) exists to make
  that unnecessary. A chart installed this way is invisible to Flux, drifts immediately, and is
  discovered by whoever next wonders why the cluster does not match the repository
- as a **kubectl plugin manager** — that is [krew](../../../../platform-engineering/kubernetes/managed/plugins/krew/README.md),
  and the two overlap only at the edges
- when the tool you want is not in the catalogue, which for anything niche is the common case.
  There is no generic "fetch this GitHub release" fallback that is as good as the curated path
- when **supply-chain provenance is a requirement**. See the note below; this is the strongest
  argument against it in a regulated context

## Notes

**The trust question, stated plainly.** `arkade get` downloads a binary from a third-party release
page, chosen by a catalogue entry in someone else's repository, and puts it on your `PATH`. That is
a real trust decision and it is the same one made by every `curl | bash` it replaces — arkade makes
the decision *once, visibly* instead of twenty times invisibly, which is an improvement in
auditability and not a change in kind. It fetches from upstream release URLs and does not rebuild
or re-sign anything, so the checksum and signature story is whatever upstream provides. For a
workstation this is normally an acceptable trade; for anything that feeds an artefact into a build
you are shipping, the relevant discipline is in
[`security/4-code/`](../../../../security/4-code/README.md), and the answer there is a vendored,
verified binary rather than a convenient fetch.

**The CI case is more interesting than the workstation case.** `arkade get --path` in a job replaces
the pattern that
[`toolchain/` §5.2](../README.md#52-ci) names as the root of "passes locally, fails in CI": a
pipeline that assembles its tools by a completely different mechanism from the laptop. arkade does
not fix that on its own — it is still a second, undeclared assembly — but it makes the CI half short
enough to read, and it makes the versions explicit if you write them:
`arkade get kubectl@v1.30.2`. Without the version suffix it is `latest`, and `latest` in CI is how a
pipeline breaks with no commit to blame. On GitHub Actions specifically, the narrower
option for one tool is a `setup-*` action — see
[GitHub Actions §9](../../../../devops/cicd/github-actions/README.md#9-notes); arkade earns its
place when the list is five tools long rather than one.

**Where this fits in pikakube: useful, and not the answer to the question this folder asks.** The
toolchain here is already declared and pinned in [`devbox.json`](../../../../../devbox.json) —
`kubectl`, `kubectx`, `kind`, `kubernetes-helm`, `fluxcd` — and that file is worth more than any
acquisition tool, because it is the thing that makes two machines agree. arkade's realistic role
here is the gaps around it: a one-off binary on a host that has no Nix store, a container image
build, or the moment somebody needs `flux` on a machine that is not their own. Filed as a tool to
know rather than a tool to adopt.

**And the `arkade install` half stays off.** Not because it is bad — the typed-flag interface over
Helm values is genuinely nicer than editing a `values.yaml` — but because this repository has
already answered "how does a chart reach the cluster" with Flux, and a second answer that leaves no
trace in Git is exactly the drift that GitOps is for.

---

[← Toolchain](../README.md)
