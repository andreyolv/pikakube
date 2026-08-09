[← Artifact registry](../README.md)

# pypiserver

<https://github.com/pypiserver/pypiserver>

---

## The problem it solves

**GitHub Packages does not host Python packages.** npm, Maven, Gradle, NuGet, RubyGems and
container images, yes; PyPI packages, no. The open request is
<https://github.com/orgs/community/discussions/8542>.

That single gap is why this folder exists. A team on GitHub writing Python has no registry that
comes with the forge, so an internal library has nowhere to go except copy-paste,
`pip install git+ssh://...`, or something self-hosted.

pypiserver is the smallest possible answer to that. It is a minimal PyPI-compatible server: it
implements the simple index that `pip` reads and the upload endpoint that `twine` posts to, over a
directory of files. There is no database, no UI worth speaking of, and no configuration language —
packages are files in a folder, and the server lists them.

That minimalism is the feature. The requirement is *"somewhere `pip install` and `twine upload`
can point at"*, and this meets it with one container and one volume.

## When to use it

- **Internal Python libraries**, shared between services in the same organisation, on GitHub.
- When the registry should be **one pod and one volume** rather than a platform to operate.
- Kubernetes, with a `PersistentVolumeClaim` for the package directory — see the
  [manifests](pypi-server/README.md) in this folder.
- Behind an Ingress with TLS. The container serves plain HTTP; credentials are sent on every
  upload, so terminating TLS in front of it is not optional outside a `port-forward`.

## When not to use it

- As a **proxy or cache for public PyPI**. It serves what has been uploaded to it. Consumers still
  need public PyPI for their other dependencies, which is what makes the `--index-url` versus
  `--extra-index-url` question below matter.
- Where **fine-grained permissions** are required. Authentication is htpasswd, and the granularity
  is which *actions* need a login (`update`, `download`, `list`) — not which package a given user
  may publish.
- Where the registry must **scan for vulnerabilities**, promote between staging and release
  indexes, or produce an audit trail. That is Nexus or Artifactory.
- For container images. Different protocol, different tool — `infrastructure/devops/`.
- As the only copy of a published artifact, without a backup of the volume. A published version
  that disappears breaks every build pinned to it.

## Notes

Everything recorded in the original note, preserved and explained.

### Recorded links

| Link | What it is |
|---|---|
| <https://github.com/pypiserver/pypiserver> | the project |
| <https://testdriven.io/blog/private-pypi/> | tutorial — also the source of the `muddy_wave` sample package in `package/` |
| <https://python.plainenglish.io/private-pypi-server-on-kubernetes-7df169864972> | tutorial — running it on Kubernetes |
| <https://github.com/orgs/community/discussions/8542> | **GitHub Packages does not support Python packages** — the reason any of this is necessary |

### The workflow that was actually run

This worked end to end. The note records the result as *"top!"* — it worked well.

**1. Reach the server.** The service is `ClusterIP`, so it is forwarded to the workstation:

```
k port-forward svc/pypi-server 8080:80
```

**2. Build and publish.** From inside the `pypi-server/package` folder, which holds the
`muddy_wave` sample package:

```
python3 setup.py sdist
pip install twine
twine upload --repository-url http://127.0.0.1:8080 dist/*
```

`setup.py sdist` produces a source distribution under `dist/`. `twine` is the upload client —
it is deliberately separate from the build step, so the thing that talks to the network is not the
thing that executes arbitrary build code. `--repository-url` points at the forwarded port instead
of public PyPI, which is the only change from publishing publicly.

**3. Install it from the private index, then remove it:**

```
pip install muddy_wave --index-url http://127.0.0.1:8080
pip uninstall muddy_wave
```

`--index-url` **replaces** the index rather than adding to it, and that detail is a security
control, not a preference:

| Flag | Behaviour | Risk |
|---|---|---|
| `--index-url` | only this index is consulted | none from public PyPI |
| `--extra-index-url` | both are consulted, highest version usually wins | **dependency confusion** — a public package of the same name and a higher version is installed instead |

The recorded command uses `--index-url`, which is the correct form.

### Open item

> *"this is the older way — test build and publish with Poetry and uv"*

`setup.py sdist` plus `twine` is the pre-`pyproject.toml` toolchain. It still works, and it is the
most widely documented path, which is why the tutorial uses it. The modern equivalents:

| Step | Old | With uv | With Poetry |
|---|---|---|---|
| Metadata | `setup.py` | `pyproject.toml` | `pyproject.toml` |
| Build | `python3 setup.py sdist` | `uv build` | `poetry build` |
| Publish | `twine upload --repository-url ...` | `uv publish --publish-url ...` | `poetry publish -r <repo>` |

This is worth closing because uv is already the recorded preference for
[Python dependency management](../../language/python/dependency-management/README.md) in this
repository — same vendor as Ruff in [`../../code-quality/lint/`](../../code-quality/lint/README.md),
one toolchain instead of three. The task is untested here, so it stays an open item rather than a
recommendation.

### What is in this folder

| Path | Contents |
|---|---|
| [`pypi-server/`](pypi-server/README.md) | the Kubernetes manifests and the Dockerfile that adds authentication |
| `package/` | `muddy_wave` — the sample package from the testdriven.io tutorial, with `setup.py` and a single `hello_world()` function |

### The gap between "it works" and "it is in use"

Publishing was done from a laptop through a `port-forward`. That proves the registry accepts and
serves packages; it is not a publishing process. What is missing is a CI job that publishes on a
tag, and an Ingress with TLS so the port-forward stops being the access path.

---

[← Artifact registry](../README.md)
