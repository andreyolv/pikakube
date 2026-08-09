[← Remote shuffle](../README.md)

# Apache Celeborn

<https://github.com/apache/celeborn>
<https://celeborn.apache.org/>

---

## What it is

A remote shuffle service: intermediate shuffle data is written to Celeborn workers instead of
to executor local disk, which makes executors disposable and dynamic allocation actually
usable — see [`../README.md`](../README.md).

The most widely adopted option of the two here, originally from Alibaba.

## When to use it

- dynamic allocation with executors scaling down mid-job
- Spark on **spot instances**, where reclamation is routine
- large shuffles where local disk sizing has become a constraint

## When not to use it

- shuffles are small and the cluster is fixed-size
- you are not prepared for the deployment friction below

---

## Notes

### The Helm chart does not work

<https://github.com/apache/celeborn/issues/2744>

### There is no official Docker image

Which for an Apache project is a genuine signal about maturity. You have to clone the
repository and build it:

```bash
# from the Celeborn binary distribution
docker build . -f docker/Dockerfile
```

<https://github.com/apache/celeborn/blob/main/docker/Dockerfile>

### The honest assessment

Broken chart, no official image, and a build step before anything can be deployed. The problem
it solves is real, and the path to using it is rougher than the project's Apache status
suggests.

Worth revisiting rather than dismissing — but budget for the build pipeline, and check whether
[Uniffle](../uniffle/README.md) has a smoother path before committing.

---

[← Remote shuffle](../README.md)
