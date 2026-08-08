[← Profiling](../README.md)

# Parca

<https://github.com/parca-dev/parca>
<https://github.com/parca-dev/helm-charts>

---

## The problem it solves

Continuous profiling using **eBPF**: an agent samples every process on every node with no
code changes, no SDK and no restart, and a server stores the profiles for comparison over
time.

CNCF project, deliberately focused — profiling and nothing else.

## When to use it

- you want continuous profiling without adopting a wider platform
- zero instrumentation is a requirement — eBPF means nothing changes in the application
- comparing profiles across time to find regressions

## When not to use it

- Grafana is the stack — [Pyroscope](../pyroscope/) integrates with it directly
- broad multi-language coverage from one agent is the goal — [gProfiler](../gprofiler/)

---

## Notes

```bash
kubectl port-forward svc/parca-server 7070
```

### The agent does not run on Kind out of the box

The agent fails inside a Kind node because of the container cgroup layout. The error is long
and does not obviously say "Kind":

```
msg="failed to set GOMAXPROCS automatically"
err="path \"/docker/<id>/kubelet.slice/...\" is not a descendant of mount point root
\"/docker/<id>/kubelet\" and cannot be exposed from \"/sys/fs/cgroup/cpuset/kubelet\""

msg="the agent can't run in a container, run with privileges and in the host PID
(`hostPID: true` in Kubernetes, `--pid host` in Docker)"
```

The second line is the actionable one: the agent needs **`hostPID: true` and elevated
privileges**. On Kind the cgroup path mismatch is a further obstacle, since the node is itself
a container.

Worth knowing before spending time on it — the failure looks like a permissions problem and
is really an environment one.

---

[← Profiling](../README.md)
