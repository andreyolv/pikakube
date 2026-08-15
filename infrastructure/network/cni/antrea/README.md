[← CNI](../README.md)

# Antrea

<https://github.com/antrea-io/antrea>

<https://antrea.io>

A CNI built on **Open vSwitch**, donated to the CNCF by VMware. The only mainstream plugin whose
Windows support is a first-class implementation rather than a footnote.

---

## The problem it solves

The CNI choice usually comes down to [Cilium](../cilium/README.md) or [Calico](../calico/README.md),
and for a Linux-only cluster that is a reasonable place for it to end. Antrea exists for the cases
where it does not:

| Situation | Why Antrea answers it |
|---|---|
| **Windows nodes carry production workloads** | the same OVS dataplane and the same policy model run on Windows and Linux — not a reduced feature set on one side |
| **The team already runs Open vSwitch** | OVS is the switch under OpenStack and NSX; the operational knowledge, the flow tables and `ovs-ofctl` all transfer |
| **"Why was this packet dropped?" is asked often** | **Traceflow** answers it directly, and nothing else in this folder has an equivalent |
| Policy needs tiers and priorities | Antrea-native policies had cluster-scoped tiers, priorities and real `Drop` rules years before upstream did |

The dataplane distinction is the structural one. [Cilium](../cilium/README.md) is eBPF; Calico is
iptables, eBPF or nftables depending on how it is configured; Antrea programs **OpenFlow rules into
Open vSwitch**. All three satisfy the Kubernetes network model described in
[§1](../README.md#1-what-a-cni-plugin-is-responsible-for) — the difference is what you debug when it
misbehaves, and OVS is a mature, well-instrumented switch with twenty years of tooling behind it
rather than a technology you are learning at the same time as the incident.

Encapsulation is Geneve by default, with VXLAN, GRE and STT available, plus a `noEncap` mode that
routes natively when the underlay allows it — the overlay/native-routing decision from
[§2](../README.md#overlay-vs-native-routing), exposed as a configuration option rather than a
product choice.

## What it has that the others do not

**Traceflow.** You submit a `Traceflow` CR naming a source pod, a destination, and a synthetic
packet; Antrea injects it, traces it through the OVS flow tables on every node it crosses, and
reports each step — including the rule that dropped it and which policy that rule came from. The
usual answer to *"the NetworkPolicy is applied and traffic still fails"* is an afternoon of
`tcpdump` on two nodes; here it is a CR and a status field. For a folder whose most-repeated warning
is [policies that silently do nothing](../../../security/2-cluster/network-policies/README.md#1-the-fact-that-matters-most-networkpolicy-is-an-api-not-an-implementation),
a tool that *proves* enforcement is not a small feature.

**Windows, properly.** The same agent, the same OVS, the same policy semantics. Every other option
here treats Windows as either unsupported or a second implementation with gaps, and mixed-OS
clusters are the one scenario where that difference decides the choice outright.

**Antrea-native policies.** `ClusterNetworkPolicy` and `NetworkPolicy` in the `crd.antrea.io` group,
with tiers, integer priorities, explicit `Allow`/`Drop`/`Reject`/`Pass` actions, and cluster scope —
everything the core API leaves out
([network-policies §5](../../../security/2-cluster/network-policies/README.md#5-policies-are-additive-there-is-no-deny-rule)).
Antrea was also an early implementer of the upstream
[network-policy-api](../../../security/2-cluster/network-policies/network-policy-api/README.md), and
the same caveat applies as to `CiliumNetworkPolicy`: the CRD form is a lock-in, the upstream form is
portable, and the upstream form is now moving to `ClusterNetworkPolicy` in `v1alpha2`.

**Egress, and flow visibility.** `Egress` CRs pin a workload's outbound traffic to a chosen node IP,
which is what makes an external firewall rule expressible at all when pod IPs are ephemeral — the
gap named in [cloud network §2](../../../security/1-cloud/network/README.md#2-why-this-is-a-different-world-from-networkpolicy).
Flow exporter emits IPFIX to a collector, with **Theia** as the analytics companion, feeding the same
appetite as [`observability/network/`](../../../observability/network/README.md).

Also present: IPsec or WireGuard encryption for inter-node pod traffic, multi-cluster connectivity,
NodePortLocal, and Service load balancing implemented in OVS.

## When to use it

- **mixed Linux and Windows clusters** — the clearest case, and effectively the deciding one
- an organisation with **existing Open vSwitch** competence, from OpenStack or NSX
- when **network troubleshooting is a recurring cost** and Traceflow would be used, not admired
- on-premise clusters where Geneve/VXLAN over an uncooperative underlay is the reality
- when policy tiers and a real deny are needed and the CNI decision is still open

## When not to use it

- **eBPF is the requirement** — kube-proxy replacement, Hubble-grade L7 visibility, or the
  performance profile that comes with it. That is [Cilium](../cilium/README.md), and Antrea is not
  competing on that axis
- the cluster is Linux-only and the team already knows Calico or Cilium. **Familiarity beats
  feature lists for a CNI**, because the cost of this component is paid during incidents
- managed Kubernetes where the provider's CNI is integrated with its load balancers, IPAM and
  support contract — replacing it is a large decision with a small payoff
- the OVS kernel module is unavailable or unwelcome on the nodes, which is a real constraint on
  locked-down images
- a Kind or local cluster, where [kindnet](../kindnet/README.md) is already there and the point is
  not the CNI

## Antrea, kube-ovn and ovn-kubernetes

Three OVS-based options live in this repository and they are not the same product. Worth stating
plainly, because "it uses Open vSwitch" is where the similarity ends:

| | **Antrea** | [**kube-ovn**](../../sdn/kube-ovn/README.md) / [**ovn-kubernetes**](../../sdn/ovn-kubernetes/README.md) |
|---|---|---|
| What it programs | OpenFlow rules into OVS, directly | **OVN** — a logical network controller *above* OVS |
| Mental model | a Kubernetes CNI with a good dataplane | a full SDN: logical switches, routers, subnets per namespace |
| Filed here under | [`cni/`](../README.md) | [`sdn/`](../../sdn/README.md) |
| Reach for it when | you want a CNI and good policy/observability | you need VPC-like multi-tenant networking, static IPs, per-namespace subnets |

The split between the two folders in this repository is the honest one: Antrea is a CNI, OVN-based
options are a software-defined network that happens to also be a CNI. The second is more capable and
substantially more to operate.

## Notes

**CNCF status.** Antrea was donated by VMware and is a CNCF sandbox project, Apache-2.0. That
lineage is worth naming for the same reason it is named for any vendor-donated project: the
development centre of gravity has been one company, and post-Broadcom VMware is a company whose
open-source priorities have visibly changed. It is not a reason to avoid the project; it is the
question to ask about release cadence before standardising on it.

**The OVS dependency is real.** Antrea needs the Open vSwitch kernel module (or a userspace
datapath) on every node. On a curated node image that is a non-issue; on a hardened or immutable
distribution it is a prerequisite to verify before the install, not during it.

**Verify enforcement, then use Traceflow to prove it.** The standing rule from
[network-policies §1](../../../security/2-cluster/network-policies/README.md#1-the-fact-that-matters-most-networkpolicy-is-an-api-not-an-implementation)
is to deploy a deny policy and confirm a connection actually fails before trusting any policy.
Antrea is the one plugin here where the confirmation step is a first-class API rather than an
improvisation — which is an argument for it that only shows up after the cluster is running.

**Where this fits in pikakube.** This cluster is [Kind](../kindnet/README.md)-based and Linux-only,
so the case that decides for Antrea — Windows nodes — does not exist here, and nothing in this
folder is deployed on top of the default. It is catalogued for two reasons that outlive the current
setup: it is the reference answer for mixed-OS clusters, and **Traceflow is the capability this
repository most conspicuously lacks** whenever a NetworkPolicy question comes up. The policy
material in [`security/2-cluster/network-policies/`](../../../security/2-cluster/network-policies/README.md)
is written and unverified; a dataplane that can answer *which rule dropped this packet* is what
turns that from documentation into something testable.

---

[← CNI](../README.md)
