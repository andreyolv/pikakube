[← Manifest templating](../README.md)

# ytt

<https://github.com/carvel-dev/ytt>

---

## The problem it solves

ytt templates YAML while **understanding that it is YAML**. Templating directives live in
comments — `#@` — so a ytt template is still a parseable YAML document, and the tool operates on
the parsed structure rather than on text.

That removes the entire class of problems that come with
[Helm's string templating](../README.md#3-why-helms-string-templating-hurts): there is no
indentation to get right, because ytt inserts a node into a tree rather than a string into a
buffer. The expression language is **Starlark**, a Python dialect from Bazel — real functions,
loops and conditionals, with no filesystem or network access.

The second capability is **overlays**: patch any YAML document by matching on its structure,
without owning or forking it. That works on arbitrary YAML, not only Kubernetes manifests, which
is what distinguishes ytt from everything else in this folder — a CI configuration, an
application config file and a Kubernetes manifest are all just YAML to it.

ytt is part of Carvel, a set of tools that also covers packaging (`kapp-controller`), applying
(`kapp`) and image resolution (`kbld`).

## When to use it

- **Patching YAML you do not own**, where forking is not an option and there is no parameter for
  the field you need.
- **Non-Kubernetes YAML.** It is the only tool here that treats that as a first-class case.
- **When Helm's templating is the specific objection** and you want the same shape of solution
  without the string problem.
- **Inside Carvel.** If `kapp-controller` is already in use, ytt is the native templating layer.

## When not to use it

- **When Helm's package management is what you actually need.** ytt templates; it does not
  version, distribute or track releases. That is `kapp-controller`'s job, and adopting it is a
  much larger decision.
- **For third-party software.** No vendor ships ytt templates.
- **When Kustomize already covers it.** For patching Kubernetes manifests specifically, Kustomize
  is in `kubectl` already and ytt is not.

## Notes

The recorded link is [carvel-dev/ytt](https://github.com/carvel-dev/ytt).

The recorded install method:

```bash
wget -O- https://carvel.dev/install.sh > install.sh
# Inspect install.sh before running...
sudo bash install.sh
ytt version
```

The middle line is the point of writing it this way. The script is **downloaded first and run
second**, as two steps, so it can be read before it executes as root. The common form —
`wget -O- ... | sudo bash` — executes whatever the server returns, which is a different security
posture entirely. Keep the two steps.

`ytt version` afterwards confirms the binary is on `PATH`; the installer places the Carvel tools
in `/usr/local/bin` by default.

ytt's real differentiator against everything else here is that it is **not Kubernetes-specific**.
Every other tool in this folder assumes it is producing Kubernetes resources; ytt assumes only
that the input is YAML. Where a repository has configuration to template that is not manifests,
that matters — and where it does not, it is the reason the tool is less specialised than
Kustomize at the one job Kustomize does.

For this repository it is an alternative on the list. The Carvel stack is a coherent, complete
answer to the same problems that Flux and Helm answer here, and mixing halves of the two is worse
than either.

---

[← Manifest templating](../README.md)
