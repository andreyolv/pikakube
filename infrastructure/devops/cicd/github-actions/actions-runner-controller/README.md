[← GitHub Actions](../README.md)

# actions-runner-controller (ARC)

<https://github.com/actions/actions-runner-controller>
<https://github.com/actions/runner>
<https://docs.github.com/en/actions/hosting-your-own-runners>

---

## The problem it solves

GitHub-hosted runners cannot reach your private network, do not offer your hardware, and run your
source on someone else's machine. Self-hosting fixes all three and immediately creates a worse
problem: **a fleet of long-lived VMs that accumulate state.** A runner that has been up for a month
has installed packages, leftover Docker images, half-populated caches and files from other teams'
jobs — until a build passes only on that machine, and a compromise in one job reaches every job
after it.

ARC makes runners **pods**. A job arrives, a pod is created, the job runs, the pod is destroyed.
Ephemeral is not a policy you enforce; it is how the thing works. The controller watches the
GitHub API for queued jobs against a *runner scale set* and scales pods to match, between
`minRunners` and `maxRunners`.

Two generations exist and confusing them wastes real time:

| | **Legacy ARC** | **Runner Scale Sets** (current) |
|---|---|---|
| CRDs | `RunnerDeployment`, `HorizontalRunnerAutoscaler` | `AutoscalingRunnerSet`, `AutoscalingListener` |
| Charts | `actions-runner-controller` | `gha-runner-scale-set-controller` + `gha-runner-scale-set` |
| Scaling signal | webhooks, or polling | a **long-poll listener** against GitHub's scale-set API |
| Targeted by | labels | `runs-on: <runnerScaleSetName>` |
| Status | community era, superseded | what GitHub supports |

The `gha-` charts are the current ones, and they are what this repository deploys. Anything found
online referencing `RunnerDeployment` is the old generation.

The install is deliberately **two releases**: one controller, and one release *per scale set*. A
scale set is bound to a single repository or organisation, so more pools means more releases — the
runner release must `dependsOn` the controller.

## When to use it

- Jobs need to reach something **private** — an internal registry, a database, a package index,
  the cluster itself
- You need **hardware the hosted fleet does not have**: GPUs, ARM, large memory, specific kernels
- **Source and secrets must stay inside your own network** for policy reasons
- You already run Kubernetes, so runner capacity is just more pods on existing nodes
- Hosted-runner minutes have become a genuinely large bill *and* you have somewhere to run them

## When not to use it

- None of the above applies. Hosted runners are free of operational cost and that is worth a lot
- You need private networking only, and you are on Azure — **GitHub's Azure VNET integration**
  gives hosted runners inside your VNET without a fleet to operate (see
  [GitHub Actions notes](../README.md#9-notes))
- You cannot accept **Docker-in-Docker**. Building images inside pods means either a privileged
  DinD sidecar or a rootless builder; if privileged containers are prohibited, plan this before
  installing, not after
- Your cluster is the production cluster and untrusted pull-request code would run on it.
  Fork-triggered jobs on a shared cluster is a boundary problem, not a scheduling one
- You want an autoscaler that reacts in seconds. Pod start plus image pull plus runner
  registration is not instant, and `minRunners: 0` makes the first job of the day slow

## Notes

**GitHub App authentication is the recommended path, and the permissions are non-obvious.** The
runner scale set authenticates to GitHub as an App rather than with a PAT — short-lived tokens,
scoped to an installation, revocable independently of any person. The exact permission set is
documented here and is the page to follow rather than guessing:

- <https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/authenticating-to-the-github-api#authenticating-arc-with-a-github-app>

**Metrics require work the chart does not do for you.** The controller and the listener expose
Prometheus metrics, but:

- <https://github.com/actions/actions-runner-controller/discussions/3024> — recorded finding:
  **the PodMonitor has to be created manually.** The chart does not ship one, so with a
  Prometheus Operator setup nothing is scraped until you write it yourself. That is why the
  HelmRelease here sets `metrics.controllerManagerAddr`, `metrics.listenerAddr`,
  `metrics.listenerEndpoint` and the `prometheus.io/*` pod annotations — the annotations are the
  fallback path for scrape configurations that use annotation-based discovery, and they are a
  workaround for the missing PodMonitor rather than the intended design.
- <https://github.com/actions/actions-runner-controller/tree/master/docs/gha-runner-scale-set-controller/samples/grafana-dashboard> —
  the upstream **Grafana dashboard** sample. Worth importing once metrics are actually arriving;
  it covers queue depth, runner counts and job durations, which are the three things that tell you
  whether the fleet is sized correctly.

**Open issues and discussions recorded here**, all of them real rough edges rather than
misconfiguration:

- <https://github.com/actions/actions-runner-controller/issues/4169>
- <https://github.com/actions/actions-runner-controller/discussions/4213>
- <https://github.com/orgs/community/discussions/160697>

Kept because ARC's behaviour is largely decided in its issue tracker and in community
discussions rather than in the documentation — the same pattern noted for GitHub Actions as a
whole. When runner behaviour is surprising, the tracker is the first place to look, not the docs.

**GARM, and an honest note.** <https://github.com/cloudbase/garm> is recorded with the verdict
*"I really do not understand what this thing is for"*. For the record: GARM (GitHub Actions Runner
Manager) provisions self-hosted runners as **cloud VMs or LXD containers** rather than as
Kubernetes pods. That is precisely why it looked pointless from inside this repository — if you
already run Kubernetes, ARC covers the same ground with the scheduler you already operate. GARM is
for estates that need runners on hypervisors, bare metal, or clouds without a cluster to host
them. The confusion was well founded: **in this context it solves nothing ARC does not.**

**What is deployed here**, from the manifests:

| Piece | Detail |
|---|---|
| Controller | HelmRelease `actions-runner-controller`, chart `gha-runner-scale-set-controller` `0.9.3` |
| Runner pool | HelmRelease `runner-mtolv`, chart `gha-runner-scale-set` `0.9.3`, `dependsOn` the controller |
| Target | `githubConfigUrl: https://github.com/andreyolv/plumbers` — a single repository, not an org |
| Scale | `minRunners: 1`, `maxRunners: 3` |
| Docker | `containerMode: dind` |
| Naming | `runnerScaleSetName: runner-mtolv` — **this is the string workflows put in `runs-on:`**; without it the name defaults to the HelmRelease name |
| Auth | `githubConfigSecret: runner-mtolv`, a Secret in the same namespace |
| Image | a `Dockerfile` with `FROM ghcr.io/actions/actions-runner:latest` — a placeholder for a custom runner image, currently adding nothing |

Two things follow from that configuration and are worth stating plainly:

**`containerMode: dind` means a privileged Docker daemon sidecar in every runner pod.** It is what
makes `docker/build-push-action` work inside the cluster, and it is a security decision. The
alternative is `containerMode: kubernetes`, which runs job containers as separate pods and needs a
`ServiceAccount` with pod-creation rights plus ReadWriteMany storage — different trade-off, not a
free upgrade. A rootless builder is the third option and avoids privilege entirely.

**`minRunners: 1` keeps one pod idle permanently.** That is the deliberate cost of not making the
first job of the day wait for a pod to start, pull the runner image and register with GitHub. At
`maxRunners: 3` this fleet is sized for one developer, which matches what it is.

The commented-out `template.spec.containers` block pinning
`ghcr.io/onedr0p/github-actions-runner` by digest is the escape hatch for when the default runner
image lacks a tool a build needs — a custom image, pinned by digest rather than by tag, which is
the right way to do it.

---

[← GitHub Actions](../README.md)
