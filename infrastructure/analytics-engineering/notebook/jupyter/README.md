[← Notebooks](../README.md)

# Jupyter

<https://github.com/jupyter/jupyter>
<https://github.com/jupyterlab/jupyterlab>
<https://github.com/jupyter/notebook>

---

## The problem it solves

The interactive loop: run a query, look at the result, adjust, run again. Nothing else in this
discipline supports finding out what the question is, as opposed to answering a known one.

For a data platform it is also the interface to
[Spark](../../../data-engineering/processing/spark/README.md) and
[Trino](../../../data-engineering/query-engine/README.md) for people who work in Python rather than in a
BI tool.

## When to use it

- exploration and analysis, by one person
- prototyping a transformation before it becomes a [dbt model](../../transform/dbt/README.md) or a job
- teaching and documentation where code and prose belong together

## When not to use it

- **as a production runtime.** Hidden state, unreviewable diffs, no tests — see [`../README.md`](../README.md#2-the-problem-with-notebooks-in-production)
- a team needs isolated environments — [JupyterHub](../jupyterhub/README.md)

## The ecosystem worth knowing

| Project | What it is |
|---|---|
| [JupyterLab](https://github.com/jupyterlab/jupyterlab) | the current interface; `notebook` is the classic one |
| [jupyter_server](https://github.com/jupyter-server/jupyter_server) | the backend everything else builds on |
| [jupyter-resource-usage](https://github.com/jupyter-server/jupyter-resource-usage) | shows memory and CPU in the UI — worth installing on shared clusters, where the alternative is a kernel dying without explanation |
| [jupyter-scheduler](https://github.com/jupyter-server/jupyter-scheduler) | scheduled notebook execution — see the caution above before using it |
| [jupyter_server_terminals](https://github.com/jupyter-server/jupyter_server_terminals) | terminal access inside the server |
| [nbextensions](https://github.com/ipython-contrib/jupyter_contrib_nbextensions) | the classic extension collection |

### Deployment and scale

| Project | What it is |
|---|---|
| [KubeSpawner](https://github.com/jupyterhub/kubespawner) | spawns per-user servers as pods — how JupyterHub runs on Kubernetes |
| [kernel_gateway](https://github.com/jupyter-server/kernel_gateway) · [enterprise_gateway](https://github.com/jupyter-server/enterprise_gateway) | remote kernels, so compute runs elsewhere — including Spark kernels on the cluster |
| [The Littlest JupyterHub](https://github.com/jupyterhub/the-littlest-jupyterhub) | single-machine JupyterHub, for small groups |
| [JupyterLite](https://github.com/jupyterlite/jupyterlite) | runs entirely in the browser via WebAssembly — no server at all |

### Images

[docker-stacks](https://github.com/jupyter/docker-stacks) ·
[images](https://github.com/jupyter/docker-stacks/tree/main/images) ·
[docs](https://jupyter-docker-stacks.readthedocs.io/en/latest/)

The images are the practical starting point for a cluster deployment — `pyspark-notebook` and
`all-spark-notebook` in particular, since they arrive with the Spark client already configured.

---

## Notes

Local install:

```bash
sudo apt install python3-pip -y
sudo pip install ipykernel --break-system-packages
```

---

[← Notebooks](../README.md)
