[← Site Reliability Engineering](../README.md)

# Tools update

Keeping the platform current without causing the outage you were trying to prevent.

---

## Why this is a capability, not a chore

Most self-inflicted platform outages are upgrades. Not code deploys — an operator minor
version, a CRD that changed `apiVersion`, a Helm chart that renamed a value, a managed
Kubernetes upgrade that removed an API something still used.

Treating updates as a procedure with a defined risk classification is what turns that from a
recurring surprise into scheduled work.

## The procedure

1. **Follow the environment order: DEV → QA → PRD.** No exceptions, including for "trivial" updates.
2. **Update Helm chart versions and image versions.**
3. **Internalise the public image** into the private container registry, and point the tool at the internal copy.
4. **Tools with PV/PVC: take a Velero backup before updating**, for resilience if the upgrade goes wrong.
5. **Read the documentation and the GitHub releases** for anything noted about this specific version jump.
6. **Update the `apiVersion` of the tool's CustomResourceDefinitions**, where required.
7. **Update Prometheus alerts and Grafana dashboards**, where the metrics changed.
8. **Send the announcements** for updates that affect users — AKS, Airflow.

Step 4 is the one people skip, and the one that turns a bad upgrade from an incident into an
inconvenience.

## Criticality classification

The value of this list is that it is empirical: it records how each tool has actually behaved
across upgrades, not how risky it looks.

### Low

| Tool | Note |
|---|---|
| cert-manager | |
| **velero** | update the image **only** when compatible with the plugin versions |
| keda | |
| marquez | |
| opencost | |
| replicator | |
| reloader | |
| elasticsearch / kibana | install the new operator and repoint fluentd/fluentbit |
| grafana | |

### Medium

| Tool | Note |
|---|---|
| prometheus | |
| sealed-secrets | |
| nginx-ingress-controller | |
| pomerium | leave it — still pinned |
| gatekeeper | |
| kube-scheduler / descheduler | update together with AKS |
| kubecost | watch for API changes affecting the cost extraction DAG |
| external-secrets | |
| fluentd / fluentbit | |
| ocean-kubernetes-controller | chart version is fine now; minor and bugfix update automatically, so only check major occasionally. Update the Kubernetes version in the Virtual Node Group **after** the cluster upgrade |
| **AKS** | before upgrading, run a deprecated-`apiVersion` check |

### High

| Tool | Note |
|---|---|
| **airflow** | check the checkup and maintenance DAGs after upgrading |
| **kafka** | |
| **flux** | |

## Reading the classification

The three high-risk entries share a property: **other things depend on them being up**. Flux
failing means nothing else reconciles; Kafka and Airflow failing means data stops moving, and
the failure is discovered downstream rather than in the cluster.

The medium tier is mostly about **coupling** — AKS with the scheduler, kubecost with the cost
pipeline, the ocean controller with the node groups. Nothing here is hard on its own; the risk
is that it is not one component.

The low tier is genuinely low, with the one exception recorded inline: Velero's image and its
plugins must move together.

## Related

- Deprecated API detection before a cluster upgrade: [`platform-engineering/kubernetes/managed/check-deprecated-apis/`](../../platform-engineering/kubernetes/managed/check-deprecated-apis/README.md)
- Backup before upgrading: [`backup/velero/`](../backup/velero/README.md)
- Image internalisation: [`security/3-container/`](../../security/3-container/README.md)

---

[← Site Reliability Engineering](../README.md)
