# Ephemeral Pull Request Preview Environments on Kubernetes with Flux ResourceSet

## Problem:
- No Environment per Change: Every change competes for the same shared dev/staging namespace, so reviewers validate a queue of merged changes instead of the one under review, and a broken change blocks everyone else.
- Manual Environment Provisioning: Creating an isolated environment for a change means hand-crafting namespaces, deployments and services, or maintaining bespoke CI jobs that template and apply them.
- Unreliable Teardown: Cleanup driven by CI jobs or webhooks silently fails when a webhook is missed, a pipeline is cancelled, or the branch is deleted while the cluster is unavailable — leaving orphan namespaces that consume quota and cost indefinitely.
- Lifecycle Tied to the Wrong Signal: Environments keyed on branch existence never go away when the branch is long-lived, turning an "ephemeral" environment into a permanently running one.
- Uncontrolled Blast Radius: Without an opt-in mechanism, every pull request — including automated dependency bumps — provisions a full environment, multiplying cost and noise on a shared cluster.
- Credential Sprawl: Each new automation that talks to the Git provider tends to introduce yet another token to issue, store and rotate.

## Solution:
- Declarative Environment Templating: Adopted the Flux Operator `ResourceSet` CRD as a template rendered once per input, producing a complete environment (Namespace, Deployment, Service) per pull request without any imperative scripting.
- Git Provider as Source of Truth: Used `ResourceSetInputProvider` with `type: GitHubPullRequest` to poll the provider API and export one input per open pull request, decoupling the environment lifecycle from the CI pipeline and from source-controller.
- Reconciliation-Based Teardown: Made deletion a consequence of reconciliation rather than an event handler — when a pull request is merged or closed the input disappears, the `ResourceSet` re-renders empty and the operator prunes what it owns, so cleanup survives controller restarts, missed webhooks and cluster downtime.
- Correct Lifecycle Semantics: Compared branch-scoped (`GitHubBranch`) and pull-request-scoped (`GitHubPullRequest`) providers side by side to document why the pull request is the right lifecycle boundary: the source branch can live indefinitely while the environment exists only during review.
- Stable, Human-Readable Addressing: Derived namespaces from the exported pull request number (`preview-pr-<number>`), which is stable across force-pushes and immediately recognizable, instead of the checksum-based identifier exported by branch providers.
- Reviewer Context in the Cluster: Propagated pull request number, source branch, author, commit SHA and title into labels, annotations and the workload itself, so any preview namespace can be traced back to the change that created it.
- Opt-In and Bounded Provisioning: Applied label-based filtering (`deploy/preview`) and `filter.limit` so environments are created only on explicit request and the number of concurrent previews is capped, containing cost and cluster pressure.
- Zero Additional Credentials: Reused the existing GitHub App secret already referenced by the `FluxInstance` for repository sync, avoiding a new credential to manage while staying well within authenticated API rate limits.
- Meaningful Readiness Signals: Enabled `spec.wait` so an environment reports `Ready` only after the workload is actually available, making the status a real answer for reviewers rather than "the apply succeeded".
- Documented Constraints and Trade-Offs: Recorded the limits of the approach — no base-branch filter in the provider, service account scoping on shared clusters, prune semantics of the parent `Kustomization`, and templating pitfalls — together with the escape hatch (`type: ExternalService`) for requirements the built-in providers cannot express.
- Previews Treated as Real Environments: Applied the same admission policies, resource requests and quotas as any other workload, acknowledging that a preview environment is production-adjacent infrastructure, not a scratch space.

## Skills:
- Platform Engineering
- DevOps
- GitOps

## Tools:
- Flux
- Flux Operator
- Kubernetes
- GitHub
- Kustomize
