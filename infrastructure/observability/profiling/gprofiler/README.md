[← Profiling](../README.md)

# gProfiler

<https://github.com/Granulate/gprofiler>

---

## The problem it solves

A cluster rarely runs one language. gProfiler is a single agent that profiles **many runtimes
at once** — Java, Python, Go, Ruby, Node.js, .NET — and merges the results into one flame
graph per node.

The alternative is a different profiling approach per language, each configured separately,
which is how profiling ends up covering only the one service someone cared about.

## When to use it

- a genuinely polyglot cluster where per-language profilers would mean several deployments
- you want one agent and one view rather than a per-runtime setup
- JVM and Python workloads coexist — common on a data platform, with Spark alongside Airflow

## When not to use it

- the stack is effectively one language — a native profiler goes deeper
- you want tight integration with an existing stack — [Pyroscope](../pyroscope/) for Grafana, [Parca](../parca/) for a standalone CNCF option

## Note on the project

Check its current maintenance status before adopting it. The multi-runtime coverage is
genuinely useful; confirm it is still being kept up with current runtime versions, since
profilers break against new releases more readily than most tools.

---

[← Profiling](../README.md)
