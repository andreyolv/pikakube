[← Plugins](../README.md)

# kubectl-slice

<https://github.com/patrickdappollonio/kubectl-slice>

---

## The problem it solves

A single YAML file containing forty resources separated by `---` is impossible to review, impossible
to diff usefully, and hostile to GitOps — which wants one resource per file, named predictably.
Vendors ship exactly such files; `helm template` produces them; `kubectl get -o yaml` produces them.

`kubectl-slice` splits a multi-document YAML file into one file per resource, named from the kind and
the metadata — `pod-nginx-ingress.yaml`, `namespace-production.yaml`. The naming template is
configurable, so the output can match whatever layout a repository uses.

## When to use it

- Importing a vendor's single-file install manifest into a GitOps repository
- Breaking up `helm template` output to read what a chart actually produces
- Making a large manifest reviewable, so a diff shows which resource changed
- Extracting resources from a cluster dump into a per-resource layout

## When not to use it

- Where Kustomize or Helm already manages the resources; do not fork them into loose files
- As a one-way conversion from a chart — the chart remains the upstream source
- For `List` objects without the workaround below; the plain command does not handle them

## Notes

**The basic command**, in both forms:

```sh
kubectl-slice --input-file=input.yaml --output-dir=./output
# or
kubectl-slice -f input.yaml -o ./output
```

The `example/` directory beside this file has both input and generated output committed: an
`input.yaml` containing a Pod and a Namespace, producing `output/pod-nginx-ingress.yaml` and
`output/namespace-production.yaml`. The naming convention — `<kind>-<name>.yaml`, lower-cased — is
visible directly from those filenames, which is why committing the output is worth doing once.

**Recorded upstream issue:** <https://github.com/patrickdappollonio/kubectl-slice/issues/28>.

### Splitting a `List`

This is the transferable part, and it is recorded in `example-list/`:

```sh
yq eval '.items[] | "---\n" + to_yaml' input.yaml | kubectl-slice -f - -o ./output
```

The problem it solves: `kubectl get pods -o yaml` does **not** return a multi-document stream. It
returns a single document of `kind: List` with everything inside `.items`. `kubectl-slice` sees one
document — the List — and there is nothing to split.

The pipeline unwraps it: `yq` iterates `.items[]`, emits each element as YAML with a `---` separator
in front of it, producing the multi-document stream `kubectl-slice` expects, and `-f -` reads that
from standard input. The `example-list/` directory has the input and the two resulting ConfigMap
files committed.

Worth knowing beyond this tool. The List-versus-stream distinction catches people out constantly —
it is why `kubectl get -o yaml | kubectl apply -f -` behaves differently from what a naive reading
suggests, and why any tool that processes "a YAML file of resources" needs to be asked which of the
two shapes it means.

---

[← Plugins](../README.md)
