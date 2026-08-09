[← Dependency updates](../README.md)

# Nova

<https://github.com/FairwindsOps/nova>

---

## The problem it solves

Nova answers one narrow question that is otherwise surprisingly annoying to answer:

> **Which Helm charts installed in this cluster are out of date, and by how much?**

It reads the Helm releases present in the cluster, resolves each chart back to its upstream
repository, compares the installed version against the latest available, and prints the gap:

```bash
# which installed charts are behind upstream
nova find

# which container images running in the cluster are behind
nova find --containers
```

The second mode is the less obvious one and often the more useful: it checks the **images**
rather than the charts, reporting where a newer tag exists upstream.

Why this is not trivial to do yourself: a Helm release records the chart name and version but not
reliably where it came from, so mapping an installed release back to a repository and a current
version requires the chart-repository index lookups Nova does for you. It also knows about
deprecated charts, which is the finding people most often did not know they needed.

It is a Fairwinds tool, from the same organisation as Polaris and Goldilocks, and it fits their
pattern: a small, single-purpose CLI that reports on cluster state.

## When to use it

- **A quick audit of chart currency.** One command, no installation in the cluster, and a
  concrete list
- **Finding deprecated charts.** Charts that upstream has abandoned are a real risk and nothing
  else routinely tells you
- **A cluster you did not build.** Nova is at its best on an inherited cluster where nobody knows
  what was installed when — it works from live state, requiring no knowledge of the repository
- **As an occasional report**, run by a person, alongside the automated updating done by
  [`../renovate/README.md`](../renovate/README.md)

## When not to use it

- **As the mechanism for keeping charts current.** Nova reports; it does not remediate. It opens
  no pull requests and changes nothing. That job belongs to Renovate, which understands Flux
  `HelmRelease` resources directly
- **In a GitOps workflow, as the source of truth.** See the recorded note below — this is the
  decisive limitation for this repository
- **Expecting vulnerability data.** "Out of date" is not "vulnerable". For the second question the
  tools are [`../../sca/README.md`](../../sca/README.md) and
  [`../../../3-container/scan/README.md`](../../../3-container/scan/README.md)
- **As a continuously running component.** It is a CLI producing a snapshot, not a controller

## Notes

Original notes recorded for this tool:

- <https://github.com/FairwindsOps/nova> — the upstream project from Fairwinds. The repository
  documents `nova find`, the `--containers` mode, the output formats (table and JSON), how to
  supply additional chart repository URLs so it can resolve charts it does not recognise, and the
  handling of deprecated charts.

- **"not GitOps friendly"** — the recorded verdict, with
  <https://github.com/FairwindsOps/nova/issues/45> as the reference.

  **What this means.** Nova works from the **live cluster**: it inspects the Helm releases
  actually installed and compares them against upstream. In a GitOps repository the source of
  truth is not the cluster, it is the Git manifests — here, the `HelmRelease` resources with their
  pinned `spec.chart.spec.version`. That mismatch produces two concrete problems:

  - **It tells you the cluster is behind, not which file to edit.** The remediation for a Flux
    repository is a version bump in a specific YAML file, and Nova's output does not connect to
    it.
  - **It requires cluster access to answer a question about Git.** That inverts the GitOps model,
    where the repository should be answerable on its own, in CI, without credentials to a running
    cluster.

  The linked issue is the record of that gap. Check its current state upstream before assuming it
  still applies — but the architectural point holds regardless of the issue's status: a tool that
  reads installed releases is answering a different question from one that reads declared
  desired state.

  **The practical consequence for this repository:** Renovate's `flux` manager already reads
  `HelmRelease` chart versions from Git and opens pull requests against them, which is both the
  detection and the remediation. Nova's remaining value here is the **deprecated chart** check and
  the `--containers` audit — genuine, and worth running occasionally by hand, but not part of the
  automated path.

---

[← Dependency updates](../README.md)
