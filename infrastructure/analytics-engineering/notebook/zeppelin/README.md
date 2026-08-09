[← Notebooks](../README.md)

# Apache Zeppelin

<https://github.com/apache/zeppelin>
<https://zeppelin.apache.org/>

---

## The problem it solves

Multi-language notebooks with **built-in visualisation** and first-class Spark integration.

Its differentiator from [Jupyter](../jupyter/README.md) is the interpreter model: a single notebook can
mix Spark (Scala), SQL, Python and shell, with results passed between paragraphs. And charts
are built in — a SQL paragraph renders a chart without any plotting code.

| Feature | Detail |
|---|---|
| **Interpreters** | Spark, JDBC, Python, shell, and more, in one notebook |
| Built-in charts | SQL results become visualisations directly |
| Dynamic forms | parameterised notebooks with input widgets |
| Spark integration | mature, and predates Jupyter's |
| Multi-user | with authentication and per-note permissions |

## When to use it

- **Spark and Scala are central**, where its integration is more natural than Jupyter's
- SQL exploration where automatic charting saves real time
- a mixed-language workflow in one document

## When not to use it

- **Python is the ecosystem.** Jupyter has far more libraries, extensions and material, and it is what most people already know
- you want the widest community; Zeppelin's is smaller and less active

## On Kubernetes

- [Quickstart](https://github.com/apache/zeppelin/blob/master/docs/quickstart/kubernetes.md)
- [zeppelin-server.yaml](https://github.com/apache/zeppelin/blob/master/k8s/zeppelin-server.yaml)

Zeppelin can launch interpreters as **separate pods**, which is a good fit for Spark: the
driver runs in its own pod with its own resources rather than inside the notebook server. That
is closer to how Spark should be run than a notebook holding a long-lived session.

## The honest positioning

It has lost ground to Jupyter in general use, and remains genuinely strong for Spark and Scala
work. Choosing it makes sense when that is the centre of gravity; otherwise Jupyter's ecosystem
is the stronger argument.

---

[← Notebooks](../README.md)
