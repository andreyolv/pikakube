[← Manifest scanners](../README.md)

# kubectl-validate

<https://github.com/kubernetes-sigs/kubectl-validate>

Recorded issue: <https://github.com/kubernetes-sigs/kubectl-validate/issues/181>

---

## The problem it solves

The same job as [kubeconform](../kubeconform/README.md) — validating manifests against Kubernetes
schemas without a cluster — approached from inside the project. kubectl-validate is a
`kubernetes-sigs` repository and a `kubectl` plugin, and it uses **the API server's own validation
code paths** rather than a separately-generated set of OpenAPI schemas.

In principle that is the better design:

| Property | Why it should matter |
|---|---|
| Same validation logic as the API server | no drift between "kubeconform says fine" and "the API server rejects it" |
| Built-in schemas for every supported Kubernetes version | no schema fetching or vendoring |
| Native CRD support | point it at CRD definitions and custom resources validate properly |
| Official SIG project | the natural long-term home for this capability |

## When to use it

- when validation must match the API server's behaviour exactly, and the difference between "close
  enough" and "identical" is worth accepting an unmaintained dependency for
- for CRD-heavy repositories, where the CRD handling is genuinely good
- with the caveat below understood and accepted

## When not to use it

- **as the default choice today**, because of the project's state. Use
  [kubeconform](../kubeconform/README.md), which is maintained, fast, and covers the same ground for
  practical purposes
- for anything beyond schema validation. Like kubeconform it says nothing about whether the manifest
  is a *good* one — that is [kube-score](../kube-score/README.md)

## Notes

**The recorded opinion, and the reason this README exists:** *"parece bacana e 'oficial' mas super
largado, anos sem release"* — "it looks nice and 'official', but it is completely abandoned, years
without a release."

The evidence recorded alongside it is issue **#181**,
<https://github.com/kubernetes-sigs/kubectl-validate/issues/181>, titled **"State of the Project"**.
It is a community member observing that the last release is roughly two years old and asking
plainly whether the project is still maintained. The issue is **open**, which is its own answer.

This is worth carrying forward as a general lesson rather than a note about one tool. Living under
`kubernetes-sigs` looks like a guarantee of maintenance and is not one: SIG repositories range from
core infrastructure to experiments that stalled. The checks that actually matter are release
cadence, recent commits, and whether "is this maintained?" has been asked and left unanswered.

Nothing is deployed for this; it is a CLI, and it is mapped rather than adopted. The recommendation
in [`../README.md`](../README.md) is kubeconform, for this reason.

---

[← Manifest scanners](../README.md)
