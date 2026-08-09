[← Notebooks](../README.md)

# JupyterHub

<https://github.com/jupyterhub/jupyterhub>
<https://github.com/jupyterhub/zero-to-jupyterhub-k8s>

---

## The problem it solves

[Jupyter](../jupyter/README.md) is single-user. A shared Jupyter server means everyone shares one Python
environment, one filesystem and one memory limit — so one person's runaway cell kills everyone
else's session.

JupyterHub gives each user their **own server**, spawned on demand. On Kubernetes that means a
pod per user, with its own image, resource limits and storage.

| Capability | Why it matters |
|---|---|
| **Per-user isolation** | one user's memory error affects only them |
| Authentication | OAuth, OIDC, LDAP — real identity rather than a shared password |
| **Resource limits** | requests and limits per user, so the cluster is not a free-for-all |
| Per-user storage | a PVC that survives the pod |
| Image choice | different profiles — a plain Python image, or one with Spark |
| Culling | idle servers shut down, which is the difference between viable and expensive |

Idle culling is the one that decides cost. Without it, every user who opened a notebook in
March is still holding a pod.

## When to use it

- **a team** needs notebooks, not one person
- users need different environments — Spark, GPU, plain Python
- identity and access control matter
- cluster resources have to be bounded per user

## When not to use it

- one or two people, where [Jupyter](../jupyter/README.md) locally is far simpler
- a fully-featured development environment is what is actually wanted, in which case notebooks are one component of it rather than the product

## Deploying it

[zero-to-jupyterhub-k8s](https://github.com/jupyterhub/zero-to-jupyterhub-k8s) is the
reference, and it is genuinely good — it covers spawner configuration, storage, authentication
and culling, which are the four things that decide whether the deployment survives contact with
users.

For smaller groups on a single machine,
[The Littlest JupyterHub](https://github.com/jupyterhub/the-littlest-jupyterhub) avoids
Kubernetes entirely.

## Related

This repository's approach was a **development environment** rather than JupyterHub alone —
Airflow, Jupyter and VS Code together in a custom Helm chart, so exploration and pipeline
development share one place. See [`../README.md`](../README.md#6-how-this-applies-to-pikakube).

---

[← Notebooks](../README.md)
