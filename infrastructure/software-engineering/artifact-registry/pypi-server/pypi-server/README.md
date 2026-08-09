[← pypiserver](../README.md)

# pypiserver manifests

<https://github.com/pypiserver/pypiserver>
<https://python.plainenglish.io/private-pypi-server-on-kubernetes-7df169864972>

---

## The problem it solves

pypiserver has no official Helm chart, and the upstream image has no authentication configured.
This folder is the plain-manifest answer to both: a small custom image that sets up an htpasswd
file at start-up, and the five Kubernetes objects needed to run it.

It is the deployment that backs the workflow recorded in [`../`](../README.md) — the one that was
actually run, end to end, and worked.

What is here:

| File | What it does |
|---|---|
| `namespace.yaml` | the `pypi-server` namespace |
| `deployment.yaml` | one replica, rolling update, credentials from a secret, packages on a volume |
| `service.yaml` | `ClusterIP` on port 80 — reachable only from inside the cluster |
| `pvc.yaml` | a `PersistentVolume` (`hostPath`, 500Mi) and a `PersistentVolumeClaim` (400Mi) |
| `secret.yaml` | the `pypisecret` username and password |
| `docker/Dockerfile` | `python:3.8-alpine`, plus `apache2-utils` for `htpasswd`, plus `pypiserver` and `passlib` |
| `docker/docker_entry.sh` | creates the htpasswd file from env vars, then starts the server |
| `docker/build.sh` | builds, tags and pushes the image |

The entrypoint is the part worth reading, because it is where the authentication decision lives:
it runs `htpasswd -b -c` with `$PYPI_USER` and `$PYPI_PASS` from the secret, then starts
`pypi-server` with `-P` pointing at that file and `-a update,download,list` — meaning **all three
actions require a login**. Publishing, installing and listing are all authenticated.

## When to use it

- As the reference for **how this registry is actually deployed** in this cluster, and as the
  starting point for redeploying it.
- When a `ClusterIP` is the right exposure. Consumers inside the cluster reach it directly;
  everything else goes through `kubectl port-forward`, which is what the recorded workflow uses.
- As a worked example of adding authentication to an upstream image that does not ship it — the
  pattern (entrypoint script writes the credential file from a secret) generalises.

## When not to use it

Several things here are tutorial-grade and should not survive contact with anything shared. They
are listed in the notes below rather than hidden, because the manifests are honest about being
adapted from a blog post.

In short: **not as-is for anything beyond a single-node cluster used by one person.** The
`hostPath` volume, the committed credentials, the privileged container and the pinned `0.0.1`
image from a personal Docker Hub account each need addressing first.

## Notes

### What the manifests actually say

| Detail | Value |
|---|---|
| Image | `andreyolv/pypi-server:0.0.1`, with the comment *"Replace it with the remote container registry"* |
| Replicas | 1, `RollingUpdate` with `maxSurge` and `maxUnavailable` at 25% |
| Credentials | `PYPI_USER` / `PYPI_PASS`, from `secretKeyRef` on `pypisecret` |
| Packages | mounted at `/pypi-server/packages` from the `pypi-pvc` claim |
| Port | container port 80, named `pypiserver` |
| `imagePullSecrets` | present but commented out, with a note on how to add one |
| Base image | `python:3.8-alpine` |
| Server flags | `-p 80 -v --log-file /var/log/pypi-server.log -P .htpasswd -a update,download,list` |

### The problems, stated plainly

| Problem | Why it matters | What to do |
|---|---|---|
| **`hostPath` PersistentVolume at `/Users/packages`** | that path is a macOS/Docker Desktop artefact; the packages live on one node's filesystem and are lost if the pod is rescheduled elsewhere | a real `StorageClass` |
| **Credentials committed in `secret.yaml`** | the username and password are in Git as `stringData`, with a comment saying to change them | SOPS or an External Secret |
| **`securityContext.privileged: true`** | the container needs none of it — the entrypoint writes one file inside its own filesystem | remove it |
| **`python:3.8-alpine`** | Python 3.8 is past end of life; the base image no longer receives fixes | rebuild on a current Python |
| **A personal Docker Hub image** | `andreyolv/pypi-server:0.0.1` is outside this cluster's control, and the manifest's own comment says so | build into the cluster's registry |
| **`RollingUpdate` with `ReadWriteOnce`** | a surge pod cannot attach the same volume, so a rollout can wedge | `Recreate`, given one replica |
| **No probes, no resource requests or limits** | the pod is unschedulable-safe and unmonitored by default | add readiness and limits |
| **Plain HTTP** | credentials cross the wire in clear text on every `twine upload` | an Ingress terminating TLS |

None of these prevented the registry from working — the [recorded workflow](../README.md) ran to
completion and the note says *"top!"*. They are the difference between *it works on my cluster* and
*other people can depend on it*.

### Rebuilding the image

`docker/build.sh` builds the tag `pypi-server:0.0.1`, retags it under the `andreyolv` repository
and pushes it. Changing where it publishes means changing the `REPOSITORY` variable in that script
and the `image:` field in `deployment.yaml` together — they are two copies of the same fact.

---

[← pypiserver](../README.md)
