[← Plugins](../README.md)

# krew

<https://github.com/kubernetes-sigs/krew>

---

## The problem it solves

`kubectl` plugins are just executables named `kubectl-something` on your `PATH`. That is simple and
it means installing, updating and discovering them is entirely manual — download a binary, put it
somewhere, remember to update it, and hope you find out that a better one exists.

krew is the package manager: a curated index, `krew install`, `krew upgrade`, `krew search`, and a
single directory on the `PATH` holding everything. It is a `kubernetes-sigs` project and it is itself
installed as a plugin.

## When to use it

- Any workstation where more than one or two plugins are in use
- Keeping plugin versions current without tracking each project separately
- Discovering plugins for a problem you did not know had one
- Reproducing a working setup on another machine

## When not to use it

- Inside containers or CI, where explicit binary installation is more predictable
- Where the plugin you need is not in the index; then install it directly
- If installing arbitrary third-party executables that run with your cluster credentials is not
  acceptable in your environment

## Notes

**The recorded installation**, which is the upstream snippet and is worth keeping verbatim because
it is fiddly:

```sh
(
  set -x; cd "$(mktemp -d)" &&
  OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
  KREW="krew-${OS}_${ARCH}" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
  tar zxvf "${KREW}.tar.gz" &&
  ./"${KREW}" install krew
)
```

What it is doing, since it looks more mysterious than it is: detect the OS and normalise the
architecture name (`x86_64` → `amd64`, `aarch64` → `arm64`), download the matching release, and run
the binary once to install itself. The subshell and `mktemp -d` keep the whole thing out of your
working directory. `set -x` prints each step, which is why a failure is diagnosable.

**Then the `PATH`, which is the step people miss:**

```sh
echo 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

kubectl krew
```

Without that export, krew installs plugins into `~/.krew/bin` and `kubectl` never finds them — the
plugin appears to install successfully and then does not exist. `${KREW_ROOT:-$HOME/.krew}` respects
an override if one is set and defaults sensibly otherwise. `kubectl krew` with no arguments is the
verification: if it prints help, the `PATH` is right.

**The trust question**, stated once: krew installs executables that run as you, with your kubeconfig.
The index is curated by the project and plugins are reviewed for inclusion, which is meaningfully
better than downloading from anywhere — but it is not an audit. On a workstation with credentials to
production clusters, that is worth a moment's thought before `krew install` becomes reflexive.

---

[← Plugins](../README.md)
