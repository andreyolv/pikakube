[← Image update automation](../README.md)

# Watchtower

<https://github.com/containrrr/watchtower>

---

## The problem it solves

**Keeping containers on a Docker host up to date, with no pipeline at all.** Watchtower runs as a
container, polls the registry for the tags its neighbours are running, and when a tag has moved it
pulls the new image, stops the old container and starts a replacement with the same configuration.

| Capability | Detail |
|---|---|
| Automatic update | poll on an interval, pull, recreate |
| Same configuration | ports, volumes, environment and links are preserved |
| Selective | by label, or by explicitly named containers |
| Notifications | email, Slack, and others, on update |
| Cleanup | optionally removes the superseded image |
| Run-once mode | update and exit, for a cron job |

For a single Docker host running a handful of services from `docker-compose.yml`, this is genuinely
good: it removes a maintenance chore entirely, with one container and no infrastructure.

## When to use it

- **a plain Docker host** — a VPS, a home server, an appliance, a small self-hosted stack
- where there is no CI/CD and building one is not worth it
- for services where an unattended update is acceptable and rollback means editing a tag
- with notifications enabled, so at least there is a record that something changed

## When not to use it

- **on Kubernetes.** Not "suboptimal" — the wrong model. Three independent reasons, below
- anywhere the running state must be reconstructable from a repository
- for anything where an unreviewed update to a production service is unacceptable
- with images from third parties whose release schedule you do not control

## Notes

Recorded link:

- <https://github.com/containrrr/watchtower> — the project.

**Maintenance status.** The `containrrr/watchtower` repository has been very quiet: releases
stopped, and issues and pull requests accumulated without much movement. Community forks exist and
are more active than the original. It is still widely deployed and it still works; check the
repository's current state before adopting it, and expect the original to be effectively
unmaintained.

**Why it does not belong on Kubernetes**, spelled out, because it is the useful lesson in this
folder:

| Reason | Detail |
|---|---|
| **It mutates running state** | the container is replaced, and **nothing in Git records it**. The repository is no longer a description of what is running, which is the one property GitOps exists to provide |
| **It needs the Docker socket** | `/var/run/docker.sock` mounted into a container is root on the host — see [§2 of `builder-k8s/`](../../builder-k8s/README.md#2-what-the-socket-actually-grants). On a cluster running containerd there is no socket at all, so it simply does not work |
| **It requires mutable tags** | the whole mechanism is "the tag moved". That is precisely what [§5 of `image/`](../../README.md#5-tags-lie-digests-do-not) argues against, because it makes deployments non-reproducible and un-rollbackable |

There is also a fourth, more practical point: Kubernetes already has a controller that replaces
pods with new images — the `Deployment`. The missing piece is only *deciding* which image, and
that is what [Flux's image automation](../flux-image-update/README.md) does, writing the decision
to Git where it can be reviewed and reverted.

The contrast is the reason this folder is worth reading as a whole:

| | **Watchtower** | **Flux image automation** |
|---|---|---|
| What it changes | the running container | **the Git repository** |
| Record of the change | a log line, and a notification if configured | a commit |
| Rollback | repoint the tag and hope | `git revert` |
| Requires mutable tags | **yes** | no — immutable tags are the point |
| Requires the Docker socket | **yes** | no |
| Fits GitOps | no | yes |

## Where it fits here

Documented for completeness, and explicitly **not** a candidate for this cluster. Its value in this
repository is as the counter-example: it makes concrete what "the cluster is changed from outside
Git" actually costs, which is the argument that the rest of
[`update/`](../README.md) rests on.

For a Docker host that is not part of this cluster, it remains a reasonable tool — with the
maintenance caveat above.

---

[← Image update automation](../README.md)
