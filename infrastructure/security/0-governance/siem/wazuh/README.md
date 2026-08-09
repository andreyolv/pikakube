[← SIEM](../README.md)

# Wazuh

<https://github.com/wazuh/wazuh>

---

## The problem it solves

Security events are scattered across hosts, containers, cloud audit trails and identity
providers, and none of it is collected, normalised or retained anywhere that could answer
"what happened".

Wazuh is the open-source platform for that. It began as a fork of OSSEC and grew into a
combined **agent-based endpoint monitor** and **SIEM**: agents on hosts (and as a DaemonSet in
Kubernetes) collect logs, watch files for modification, monitor processes and network activity,
and run configuration and vulnerability checks locally; a central server normalises everything
against a large rule set, correlates, alerts, and stores it in an OpenSearch-derived indexer
with a dashboard on top.

What distinguishes it from a log pipeline is that the agent does real work rather than shipping
lines:

| Capability | What it gives you |
|---|---|
| **File integrity monitoring** | alerts when binaries or configuration change on hosts that should be immutable |
| **Log collection and decoding** | thousands of maintained decoders and rules, so sources arrive normalised |
| Configuration assessment | CIS-style checks run on the endpoint, mapping to [`compliance/`](../../compliance/README.md) |
| Vulnerability detection | inventories installed packages and matches them against feeds |
| Rootkit and anomaly detection | classic host intrusion detection |
| Active response | scripted reaction — block an address, kill a process |
| Compliance mappings | rules tagged against PCI DSS, GDPR, HIPAA, NIST 800-53 |

The rule set is the actual asset. Writing detections from scratch is where SIEM projects
stall, and arriving with thousands of maintained decoders and rules already mapped to
compliance controls is most of what a commercial product is sold on.

## When to use it

- an open-source, self-hosted SIEM is required — no per-GB licence, and data stays in the
  environment
- **host-level** visibility matters: file integrity, host authentication, rootkits, processes.
  This is Wazuh's heritage and it is stronger there than cloud-native-only tools
- a compliance framework has to be evidenced, and the built-in mappings shorten the work
  substantially
- a mixed estate — VMs, bare metal and Kubernetes — where a single agent story is worth a lot
- learning how a SIEM works end to end. It is complete enough to be instructive and free enough
  to run

## When not to use it

- there is **nobody to respond to alerts**. This is the disqualifying condition for any SIEM,
  and it applies regardless of price — see [`../README.md`](../README.md#8-how-this-applies-to-pikakube)
- a small cluster where a managed service or an existing log platform already covers the
  requirement; Wazuh is several components and real operational work
- as a Kubernetes-native runtime security tool. Falco, Tetragon and Tracee in
  `2-cluster/runtime-security/` do syscall-level container detection far better; Wazuh's
  strength is the host and the correlation layer above them
- as an observability platform. Different retention, different access model, different question
  — see [`../README.md`](../README.md#siem-is-not-observability)
- when storage and memory are constrained. The indexer is OpenSearch-derived and has
  OpenSearch's appetite

## Notes

Original reference recorded for this tool:

> <https://github.com/wazuh/wazuh>

Nothing further was recorded, so the notes worth adding are about what adoption actually
involves.

**It is not one component.** A Wazuh deployment is a manager (or a cluster of them), an
indexer, a dashboard, and agents. Sizing is driven by the indexer, and it is the part that
surprises people — it is OpenSearch underneath, with the memory and disk profile that implies.
On a small cluster this is usually the reason the deployment is abandoned.

**The agent is the differentiator and the operational cost.** File integrity monitoring and
configuration assessment run on the endpoint, which is why the data is richer than a log
shipper's — and it also means an agent to deploy, update and monitor everywhere. In Kubernetes
that is a privileged DaemonSet, which is itself a component to think carefully about: a
security agent with host access is a high-value target.

**Its relationship with the rest of this repository.** Wazuh overlaps deliberately with several
folders — configuration assessment overlaps [`compliance/`](../../compliance/README.md),
vulnerability detection overlaps `3-container/scan/`, and container runtime monitoring overlaps
`2-cluster/runtime-security/`. It is generally weaker at each of those than the dedicated tool
and better at the thing none of them do, which is **correlating across all of them and keeping
the result**. Adopt it for that, not to replace them.

---

[← SIEM](../README.md)
