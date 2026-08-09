[← Attack path](../README.md)

# KubeHound

<https://github.com/DataDog/KubeHound>

Context and comparison against the other tools: [../README.md](../README.md)

---

## The problem it solves

Every other tool in this repository answers a question about **one object**: this pod is
privileged, this Role is too broad, this image has a CVE. None of them answer the question
that actually decides whether a finding matters:

> **If an attacker lands in *this* pod, can they reach cluster-admin, and how many steps
> does it take?**

That is a *graph* question, not a list question. A privileged pod is only interesting
because of what it is next to; a wide RoleBinding is only interesting because something
reachable can use it. Severity scores on individual findings cannot express that, which is
why a backlog of 400 "medium" findings tells you nothing about your real exposure.

KubeHound reads the cluster through your kubeconfig, models every asset (nodes, pods,
containers, volumes, identities, permissions) as a **vertex**, models every known
privilege-escalation technique as an **edge**, and loads the result into a graph database.
You then ask reachability questions directly:

- which containers are within N hops of cluster-admin
- which paths cross from a namespace a developer can deploy into, to the control plane
- if this specific pod were compromised today, what is the shortest path out

It is explicitly modelled on **BloodHound**, the tool that did the same thing for Active
Directory, and it comes from Datadog's Adversary Simulation Engineering team.

The edges encode real, published techniques rather than generic "misconfiguration"
categories, grouped roughly as:

| Edge family | What it represents |
|---|---|
| Container escape | `hostPID`/`hostNetwork`, privileged containers, sensitive host mounts, kernel module load, writable `/var/log`, exposed CGroup release agent |
| Credential theft | reading a mounted ServiceAccount token, reading a Secret, reading a host path holding kubelet credentials |
| Identity assumption | using a stolen token as the identity it belongs to |
| Permission traversal | a Role or ClusterRole that permits `pods/exec`, `pods/attach`, creating pods, or impersonation |
| Lateral movement | reaching another pod that shares a namespace, node, or process namespace |

The output is the sentence a report can actually be written around: *"a compromise of any
pod in `team-a` reaches cluster-admin in three hops via this specific ServiceAccount."*

## When to use it

- **After** the defensive controls exist, to check they actually cut the paths you assumed they cut. This is the validation step for `pod-security/`, `policies/` and RBAC in `identity-access/`
- Prioritising a backlog of posture findings by real reachability instead of by CVSS
- Designing RBAC: it makes the transitive effect of a RoleBinding visible, which is precisely the thing humans reason about badly
- Before and after a change, as a regression check ("did this new operator open a path to the control plane?")
- Red-team preparation, and blue-team verification of the same

## When not to use it

- As your only security tool. It models **paths**, not vulnerabilities. It will not tell you an image is unpatched (`3-container/`) or that a workload is behaving oddly right now (`runtime-security/`)
- As a continuous control. It is a point-in-time snapshot: run it, get a graph, reason about it. It is not an admission controller and it blocks nothing
- Where you cannot get broad read access. Building a complete graph needs wide read permission across the cluster, which is itself a sensitive credential. Treat the collection kubeconfig accordingly
- On an empty or trivial cluster. With no real workloads and no real RBAC there are no interesting paths, and the setup cost is not repaid
- As a substitute for benchmark compliance. `posture/` (kube-bench, kubescape) answers "does this match CIS"; KubeHound answers "what can be reached". Different questions, and auditors ask the first one

## Notes

The original note in this folder was the project link and nothing else:

- <https://github.com/DataDog/KubeHound> — the upstream repository. Apache 2.0, from Datadog.

Points worth recording alongside it:

- **How it runs.** A binary plus a Docker Compose stack for the backend. The graph store is
  a graph database queried with **Gremlin**; KubeHound also ships a simplified DSL and a
  **Jupyter notebook** interface (`http://localhost:8888`) so you do not have to write raw
  Gremlin for common questions. It picks the target cluster from `KUBECONFIG` or the current
  `kubectx` context, so **check which cluster is selected before running it**.
- **The BloodHound lineage is the fastest way to explain it** to anyone who has done Active
  Directory security. Same idea, different domain: assets are vertices, attack techniques
  are edges, and the interesting output is a shortest path.
- **It is a read-only collector.** It does not exploit anything, unlike
  [kubesploit](../kubesploit/README.md). The graph is derived from the API server's view of
  the cluster, which also means it inherits that view's blind spots: anything not expressed
  as a Kubernetes object (a host firewall rule, a node-level agent, an external IdP trust)
  is not in the graph.

---

[← Attack path](../README.md)
