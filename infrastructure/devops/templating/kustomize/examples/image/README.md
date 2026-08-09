[← Kustomize examples](../README.md)

# image

Rewrites container images without patching each container.

```yaml
resources:
  - ../../base
images:
  - name: ubuntu
    newName: my-registry/my-image
    newTag: dev-latest
```

`name` is the image as written in the base — the thing being matched, not a resource name.
`newName` and `newTag` replace it. Either can be given alone, and `digest` can replace `newTag`
when pinning by content.

Kustomize finds **every** `image:` field with that value, across every container in every
workload kind, including `initContainers`. There is no path to write and nothing breaks when a
container is added later.

This is the most-used transformer in practice, because it is the hook a CI pipeline needs: after
building, `kustomize edit set image ubuntu=my-registry/my-image:$SHA` updates the overlay, the
commit lands in Git, and the GitOps controller rolls it out. That single command is how most
image-tag automation works, including Flux's image update automation, which writes the new tag
back to the repository.

Rendered result in [`output.yaml`](output.yaml):

```bash
kustomize build overlays/dev -o output.yaml
```

---

[← Kustomize examples](../README.md)
