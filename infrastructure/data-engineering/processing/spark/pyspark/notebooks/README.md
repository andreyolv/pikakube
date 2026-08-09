[← PySpark](../README.md)

# Hands on PySpark

Notebooks for practising PySpark locally, with Jupyter and Spark in one container.

---

## Running it

```sh
sudo service docker start

docker run --name spark -p 8888:8888 \
  -v /home/andreolv/Desktop/pyspark:/home/jovyan/pyspark \
  jupyter/all-spark-notebook:spark-3.3.0
```

Replace `/home/andreolv/Desktop/pyspark` with the path where your notebooks live.

Then open the link printed in the terminal.

<p align="center">
  <img src="pyspark.jpg" title="Jupyter with PySpark">
</p>

---

## Why this image

`jupyter/all-spark-notebook` arrives with Spark and the Python client already configured, so
there is no local Spark installation, no `SPARK_HOME`, and no version mismatch between the
client and the runtime.

For learning and for prototyping a transformation before it becomes a job, that removes the
setup that usually consumes the first hour.

See [docker-stacks](https://github.com/jupyter/docker-stacks) for the other images —
`pyspark-notebook` is the smaller variant without Scala and R.

## What this is not

**Local mode.** Spark runs in a single JVM inside the container, so it exercises the API and
not the distributed behaviour — no real shuffle across nodes, no executor scheduling, no skew
that only appears at scale.

Good for learning the API and writing transformations. The behaviour that matters in production
only shows up on a cluster — see [`../../README.md`](../../README.md#2-deployment-modes).

## Related

- [`../README.md`](../README.md) — the UDF trap and the style guide
- [`analytics-engineering/notebook/`](../../../../../analytics-engineering/notebook/README.md) — notebooks explore; they do not run in production

---

[← PySpark](../README.md)
