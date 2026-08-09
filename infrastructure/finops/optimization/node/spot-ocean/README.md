[← Node optimization](../README.md)

# Spot Ocean

<https://github.com/spotinst/charts>

---

## The problem it solves

Spot instances are worth roughly 90% off on-demand, and the reason most platforms do not run
production on them is not price — it is that a reclaimed machine takes two minutes' notice, and
nobody wants to own the consequences.

Spot Ocean (NetApp, formerly Spotinst) is a **commercial SaaS** whose entire product is making that
survivable. A controller in the cluster reports pods and capacity; the vendor's control plane
chooses the machines, and — this is the differentiator — **predicts interruptions and provisions the
replacement before the reclamation happens**, rather than reacting to the termination notice.

It also runs the two things a fixed node pool cannot: heterogeneous fleets, so a machine can be
sized to the workload that needs it rather than to the largest workload in the pool; and continuous
repacking, moving pods off underused nodes so those nodes can be shut down.

Commercial, on a "pay as you save" model — the fee is a share of the savings.

## When to use it

- **production workloads on spot**, where the interruption handling has to be better than "hope and
  a PodDisruptionBudget"
- a mixed fleet where per-workload machine sizing matters more than a uniform pool
- when nobody will own autoscaler tuning, and the alternative is that the cluster stays on
  on-demand indefinitely
- an existing Spot account, where the marginal cost of adding a cluster is small

## When not to use it

- when [Karpenter](../karpenter/README.md) reaches the same place: group-less provisioning,
  consolidation, spot-to-spot replacement and diversification are all open source now, and the gap
  is predictive replacement rather than capability
- when an external control plane holding authority to delete production nodes is unacceptable
- **before right-sizing** — the notes below record exactly why, from experience
- for the workloads in the "not recommended" list below, whatever the tool
- purely for cost reporting; that is [`visibility/`](../../../visibility/README.md)

## Notes

The original notes for this folder are the most substantial in `finops/` — a full internal
description of the platform's spot strategy, written from running it. Translated in full below, with
commentary. The reasoning survives whichever tool ends up implementing it.

**<https://github.com/spotinst/charts>** — the vendor's chart repository, served from
`https://charts.spot.io`. Several separate charts: the controller, the metric exporter, the network
client.

### Virtual machine types

> All workloads running on Kubernetes cluster instances run on virtual machines at a cloud provider,
> in our case Azure.
>
> In terms of how they are paid for, there are basically three classes of virtual machine at the
> cloud providers:
>
> **On demand:** you pay as you use. Recommended when there is no predictability of continuous
> machine usage.
>
> **Reserved instance:** you pay up front to reserve specific instances. Recommended when there is
> predictable continuous usage. Gives discounts of roughly **30 to 40%** relative to on-demand.
>
> **Spot:** these are the cloud provider's leftover unused machines. Gives discounts of roughly
> **90%** relative to on-demand. They have no SLA, because the provider can interrupt the machines
> at any time.

This is the framing the whole discipline rests on, and it is worth keeping visible: the three
purchasing models are a *reliability* choice as much as a price one. Reservations trade flexibility
for a discount; spot trades availability for a much larger one. See
[`finops/`](../../../README.md) section 6.

### What Spot Ocean adds

> Specific characteristics that the Spot Ocean solution offers for spot machines:
>
> **It monitors which virtual machine families are cheapest and least likely to be interrupted**, in
> order to guarantee greater availability even on a spot machine, improving the cost/benefit ratio.
> Without Spot Ocean, the cloud provider can take some minutes to reallocate the interrupted load.
> Ocean can predict when a machine is going to be deprovisioned and requests the creation of another
> one in advance.
>
> **Heterogeneous allocation of virtual machine classes, avoiding wasted resources.** That is, it is
> possible to bring up a machine of the ideal size for the workload you want to place at that
> moment. Unlike reserved instances, where it is always the same machine class and the same size
> that is made available, causing wasted machine resource when you provision a machine with a lot of
> resource for a workload that requests little.
>
> **Resizing of the virtual machines** — that is, resizing the current machines to fit the
> workloads, avoiding wasted resources. For this there is transfer of workloads between machines
> that are not near their maximum resource allocation, in order to deprovision unnecessary machines.
> Example: 2 identical machines each at 30% usage — one machine transfers its workloads to the
> other, which ends up at 60%, and one of them can be shut down.

Three claims, and they map exactly onto the four jobs in [`node/`](../README.md) section 1:
predictive interruption handling, instance selection, and consolidation. The first is the one
Karpenter does not do — it reacts to the provider's termination notice rather than anticipating it.
The other two are now open-source table stakes.

> **Note:** the "Pay as you save" contract model gives a net discount of roughly **65%** relative to
> on-demand machines.
>
> If no spot machine is available for your workload, a regular machine will be selected.

Two important details. **65% net, not 90%** — the vendor's share of the savings is the difference,
and that is the number to compare against doing it yourself. And the fallback to on-demand is what
makes spot safe to default to: capacity scarcity degrades cost, not availability.

### Workload types

> **Recommended**
>
> - Workloads where high availability is not required. Example: DEV and QA environments. (Today all
>   projects' workloads are already on spot VMs.)
> - Airflow workloads in general.
> - Backend and frontend applications, jobs.
>
> **Not recommended**
>
> Some kinds of workload are not recommended for spot; here they are, with their reasons:
>
> - **Very long Airflow tasks, above a few hours.** The longer it is, the greater the risk.
> - **Non-distributed databases (with only 1 replica):** the database pod resetting because of a
>   virtual machine change can cause unavailability in every application that depends on access to
>   the database (if there are many, and they need high availability).

This classification is the genuinely valuable part of the document, and it is tool-independent.
The two exclusions are the two that catch everyone:

- **Interruption risk compounds with duration.** A six-hour task with no checkpointing has a high
  chance of being interrupted at least once, and each restart pays the whole elapsed cost again.
  Past some duration, spot is more expensive than on-demand.
- **Single-replica stateful workloads convert an interruption into an outage** — and the blast
  radius is not the database, it is everything that queries it.

### Adjustments the move requires

> **Badly configured resources in the KubernetesExecutor**
>
> The non-spot VMs used today are provisioned with plenty of resource, and that allows spare
> resource for scaling and for accommodating badly-sized workloads that use more resource than they
> request. But with spot VMs, the size of the VMs will be allocated more optimally according to the
> workload's request. Therefore the workloads' resources must be configured correctly.
>
> If a workload uses much more than it requests while on a spot VM, there is a large risk of the
> workload breaking, because the initial request asked for a certain amount of resource, but the
> workload needs to use more than exists on the VM it was allocated to.
>
> To avoid this it is good to follow the Grafana dashboard `xxxxxxxx`, which shows the difference
> between requested and used resource, and make the necessary corrections.

**This is the most important paragraph in the folder.** It is the ordering rule in
[`optimization/`](../../README.md) section 2, derived from experience rather than from theory:
generously-sized on-demand nodes silently subsidise every workload whose requests are wrong, and
tightly-provisioned capacity removes that subsidy. The failure then looks like "spot broke our
workloads" when it is actually "our requests were always wrong".

The mitigation named — a dashboard comparing requested against used — is precisely what
[`rightsizing/`](../../rightsizing/README.md) automates. Right-size **before** moving to spot, not
after.

The reference to `KubernetesExecutor` places this in Airflow: each task runs as its own pod with the
resources declared in the DAG, so the corrections have to be made per task by whoever owns the DAG.

### Onboarding a namespace

> **Requesting the addition of a namespace to Spot**
>
> Nothing needs to be configured by the project or the namespace's technical owner.
>
> They only need to open a card at the end of the DataOps backlog with the following information:
>
> - **Namespace:** the name of the Kubernetes namespace to be added to spot VMs.
> - **Technical owner of the namespace:** the Analytics Engineer, Data Engineer or Data Scientist
>   responsible for following the namespace's workload execution for 1 week and reporting to DataOps
>   if there is any problem.
> - **Particular case:** by default the entire namespace will be added for execution on spot VMs. If
>   there is an exception where you want to add only some of the namespace's workloads to spot VMs
>   but not others, explain the case.
>
> **Example**
>
> Card name: `VM Spot/PRD - Add namespace xyz`
>
> Definition of Done:
> - Namespace: xyz
> - Technical owner: xyz
> - Particular case: no

The process is worth preserving because it is the part most platforms never write down, and it gets
three things right:

1. **Opt-in per namespace**, not a cluster-wide switch. Migration is incremental and reversible.
2. **A named technical owner who watches for a week.** Interruptions are probabilistic — a day
   proves nothing, and the person who can tell whether a failure is spot-related is the one who
   knows what normal looks like.
3. **An explicit escape hatch** for namespaces with mixed tolerance, so the answer to "we have one
   workload that cannot take this" is a conversation rather than a blanket refusal.

The ticket link and the Grafana dashboard name were redacted in the original.

### On the deployment here

Three HelmReleases, all Flux-managed from `https://charts.spot.io` into a `spot-ocean` namespace:

| Release | Version | Purpose |
|---|---|---|
| `ocean-kubernetes-controller` | **unpinned** | the controller itself — reports state and executes decisions |
| `ocean-metric-exporter` | 1.0.10 | Ocean's metrics as Prometheus series |
| `ocean-network-client` | 1.1.0 | network cost and traffic data |

Points worth noting:

- **The controller is deliberately unpinned**, with a comment recording that updates are automatic by
  default and can be disabled through values. For a component with authority to delete production
  nodes, automatic upgrades are a real risk to weigh — this is the one release in `finops/` where the
  version is unpinned on purpose rather than by omission.
- **`metrics-server.deployChart: false`** — the chart bundles metrics-server and it is switched off,
  because the cluster already has one. Exactly the right instinct, and the same one applied to
  Kubecost's bundled Prometheus elsewhere in this folder.
- **The metric exporter is scraped by annotation** (`prometheus.io/scrape`, port 5050) and configured
  for the `scaling` and `cost_analysis` categories — so Ocean's own view of savings and scaling
  activity lands in the platform's Prometheus rather than only in the vendor's console. That is what
  makes the vendor's claims checkable.
- The exporter is pinned to the `sysephem` node pool with a `CriticalAddonsOnly` toleration — the
  thing that watches spot capacity should not itself be running on spot capacity.
- **Credentials (`token`, `account`, `clusterIdentifier`) are placeholders** in all three releases.
  They belong in a Secret, not in a values file.

---

[← Node optimization](../README.md)
