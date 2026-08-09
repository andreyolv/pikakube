[← Manifest scanners](../README.md)

# kube-score

<https://github.com/zegl/kube-score>

---

## The problem it solves

[kubeconform](../kubeconform/README.md) proves a manifest is structurally valid. It says nothing
about whether it is any good, and the API server will happily accept a Deployment that is going to
cause an incident:

| What the schema accepts | What happens in production |
|---|---|
| No resource requests or limits | unschedulable, or a noisy neighbour taking down a node |
| No liveness or readiness probe | traffic to Pods that are not ready; hung Pods never restarted |
| `image: latest`, `imagePullPolicy: Always` | nobody can say what version is running |
| One replica, no `PodDisruptionBudget` | a routine node drain is an outage |
| No pod anti-affinity | every replica on the same node, defeating the point of replicas |
| `runAsRoot`, writable root filesystem | a container escape becomes a node compromise |
| No `NetworkPolicy` | flat cluster networking, by default |

kube-score is **static analysis for manifests**. It runs before anything is applied — against files,
or against rendered Helm and Kustomize output — grades each object, and explains each finding.

Because it works on files rather than on a cluster, it belongs in the pull request, which is the
only place these findings are cheap to act on.

Findings can be suppressed per object with annotations, and individual checks can be disabled
globally, so it can be adopted incrementally rather than as a wall of failures on day one.

## When to use it

- **in CI, on rendered manifests, as a required check.** This is the tool in this folder that
  actually changes how workloads are written
- when introducing workload standards to a team — the output explains *why* each finding matters,
  which is a better teaching mechanism than a policy document
- as the pre-merge counterpart to [Polaris](../../cluster/polaris/README.md): the same class of
  concern, before it reaches a cluster rather than after

## When not to use it

- **as enforcement.** It advises. Anything that must not be admitted belongs in a policy engine at
  admission time (`security/2-cluster/policies/`)
- against unrendered templates. Helm templates are not YAML; render first, or every finding is
  meaningless
- with every check enabled from day one on an existing repository, unless the intent is for the
  check to be immediately disabled by whoever it blocks. Start with the checks the team agrees with,
  and add
- as a security tool. It covers the security-adjacent workload settings and stops well short of a
  security review

## Notes

The only recorded reference is the repository: <https://github.com/zegl/kube-score>.

Nothing is deployed for this — it is a CLI belonging in a pipeline.

Its position in the three-layer sequence described in [`../README.md`](../README.md) is the top one:
[yamllint](../yamllint/README.md) checks that it is YAML,
[kubeconform](../kubeconform/README.md) checks that it is Kubernetes, kube-score argues about
whether it is *good* Kubernetes. Only the last one has opinions, which is why it is the only one of
the three that generates disagreement — and that disagreement is useful, because it is a
conversation about standards happening in a pull request rather than during an incident.

The overlap with [Polaris](../../cluster/polaris/README.md) is real and largely benign: they check
similar things at different times. If only one is going to be run, run this one, because a finding
before merge costs a comment and a finding after deployment costs a change window.

---

[← Manifest scanners](../README.md)
