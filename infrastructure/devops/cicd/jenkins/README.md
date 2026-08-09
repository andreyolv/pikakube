[← CI/CD](../README.md)

# Jenkins

<https://github.com/jenkinsci/jenkins>
<https://github.com/jenkinsci/helm-charts>

---

## The problem it solves

Jenkins is the reason CI became normal. It automates *"run this when something changes"*, it does
it for any language, on any platform, against any tool — because whatever the tool is, there is a
plugin. Nearly two thousand of them.

That plugin ecosystem is simultaneously the reason it won and the reason it is hard to run:

| Strength | The same thing, as a cost |
|---|---|
| A plugin for everything | plugin versions, plugin conflicts, plugin CVEs, plugins abandoned upstream |
| Runs anywhere, including outside Kubernetes | it is a stateful Java application with a mutable home directory |
| Enormous installed base and knowledge | most of that knowledge is about the old, UI-configured way |
| Fully scriptable | Groovy, and a sandbox that surprises people |

**The historical weakness is configuration by clicking.** Jenkins' original model was jobs defined
through the web UI and stored in the controller's own filesystem — unreviewed, unversioned, and
impossible to rebuild from source. That is where "the build server nobody can recreate" comes from,
and it is why every tool built after Jenkins is code-first by construction. `Jenkinsfile` (pipeline
as code), Job DSL and JCasC (Configuration as Code) fixed it properly, but estates that predate
them largely did not migrate.

Modern Jenkins on Kubernetes is a genuinely different thing: the controller in a pod, JCasC
supplying the configuration from a ConfigMap, and the Kubernetes plugin creating an **ephemeral
agent pod per build**. That combination removes most of the classic objections.

## When to use it

- **An existing Jenkins estate.** Hundreds of jobs and years of institutional knowledge are a real
  asset; migrating is a project, not a preference
- Builds that must run **outside Kubernetes** or on unusual platforms — Windows, macOS, embedded
  hardware, bare metal with attached devices
- A tool or system with **no integration anywhere else** but a maintained Jenkins plugin. This is
  still surprisingly common in enterprise environments
- Deep, granular control over the build environment, where hosted CI's constraints do not fit
- Air-gapped environments where a self-hosted controller is required anyway

## When not to use it

- **Greenfield, with code on GitHub.** [GitHub Actions](../github-actions/README.md) gives PR
  integration, an ecosystem and hosted runners with no server to operate
- You are unwilling to own **plugin maintenance**. Plugins are the ongoing tax: updates, breakage,
  and a steady stream of security advisories. This is the honest reason not to choose it
- The team will configure jobs in the UI. Without an enforced `Jenkinsfile` + JCasC discipline you
  are rebuilding the unmaintainable server
- You want the pipeline to be portable. `Jenkinsfile` is Groovy tied to Jenkins;
  [Dagger](../dagger/README.md) exists precisely to avoid that lock-in
- You want it as a **CD** tool. A Jenkins job holding a production kubeconfig is the credentials
  problem described in [CI/CD §3](../README.md#3-the-credentials-consequence) in its most common
  form. Flux already does delivery here

## Notes

There is no `doc.md` for Jenkins in this repository — no recorded links, opinions or findings.
What exists is the deployment, and it is minimal.

**What is deployed here:**

| Piece | Detail |
|---|---|
| Chart | HelmRelease `jenkins`, chart `jenkins` version `5.7.26`, from the `jenkins` HelmRepository in `flux-system` |
| Namespace | its own, `jenkins` |
| Values | **empty** — only the two documentation comment lines |

The two comments are the chart references, and they are the right ones to keep:

- <https://artifacthub.io/packages/helm/jenkinsci/jenkins>
- <https://github.com/jenkinsci/helm-charts/blob/main/charts/jenkins/values.yaml>

`values.yaml` is the file that matters for this chart specifically, because the official chart does
far more than start a container. Three things in it decide whether the install is usable:

- **`controller.installPlugins`** — the chart installs a default plugin set at start-up. Left at
  defaults, plugin versions drift with the chart, which is exactly the reproducibility problem
  Jenkins is criticised for, reintroduced through Helm.
- **`controller.JCasC`** — Configuration as Code. This is the mechanism that makes a Helm-deployed
  Jenkins reproducible instead of a stateful pet: credentials, security realm, agent clouds and
  job definitions all declared in the values file rather than clicked in. **Deploying Jenkins
  without JCasC recreates the original problem**, because the configuration then lives only in the
  controller's PVC.
- **`agent`** — the Kubernetes plugin's pod template. This is what makes builds run as **ephemeral
  agent pods**, one per build, which is how Jenkins gets the same clean-runner property as
  [ARC](../github-actions/actions-runner-controller/README.md).

With defaults and no persistence configuration reviewed, this install should be read as
**mapped for comparison, not operated**. It is here so the incumbent is represented next to the
alternatives, and the note to carry forward is the specific one above: if Jenkins ever becomes
real on this platform, JCasC is not optional — it is the entire difference between a reproducible
controller and a snowflake.

---

[← CI/CD](../README.md)
