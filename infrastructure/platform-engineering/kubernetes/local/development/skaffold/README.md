[← Development](../README.md)

# Skaffold

<https://github.com/GoogleContainerTools/skaffold>

---

## The problem it solves

Skaffold watches your source, and on every change it builds the image, tags it uniquely, pushes it
if needed, applies the manifests and streams the logs back. One `skaffold dev` replaces the whole
build-tag-push-apply-wait sequence, and because it tags every build differently, the "I deployed
and nothing changed" class of problem disappears.

It is deliberately unopinionated: it drives whatever builder you already use (Docker, Buildpacks,
Bazel, ko, Jib) and whatever deployer you already use (`kubectl`, Helm, Kustomize). It does not ask
you to restructure the project.

## When to use it

- You want the loop to build the **real image** on every change, not sync files into a pod
- The project already has a Dockerfile and plain manifests — `skaffold init` will infer the config
- One or a few services; for many at once, Tilt's UI is better suited
- You want the same config usable in CI (`skaffold build`, `skaffold run`)

## When not to use it

- Sub-second feedback is the requirement — image builds cannot compete with file sync
- The build is slow and cannot be made incremental; the loop inherits that cost
- You want a graphical view of a dozen services — that is [Tilt](../tilt/README.md)
- As a production deployment mechanism; GitOps owns that

## Notes

Recorded install and usage:

```sh
brew install skaffold
skaffold init
skaffold dev
```

`skaffold init` scans the directory, finds Dockerfiles and manifests, and writes a `skaffold.yaml`
for you. That single command is most of why this is the tool that got picked up here — the other
five need a config written by hand before anything runs.

Two flags were noted alongside it:

```sh
skaffold init --skip-build
skaffold init -f skaffold.yaml
```

- `--skip-build` generates a config with **no build stage**, for when the images already exist and
  you only want the deploy-and-watch half. Useful when iterating on manifests rather than code.
- `-f skaffold.yaml` points at an explicit config file rather than the default lookup — the flag
  you need once there is more than one profile or more than one config in the tree.

The working example lives beside this file: a small Python app under `docker/`, its manifests under
`kubernetes/`, and `skaffold.yaml` tying them together. It is the only complete inner-loop setup in
the repository.

---

[← Development](../README.md)
