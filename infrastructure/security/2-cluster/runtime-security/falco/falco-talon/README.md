[← Falco](../README.md)

# falco-talon

<https://github.com/falcosecurity/falco-talon>
<https://github.com/falcosecurity/charts>

The response engine. Falco detects; Talon does something about it — kill the pod, apply a
NetworkPolicy, label it for quarantine, capture forensics.

---

## The problem it solves

Detection without response is a dashboard.

A Falco alert reaches Slack at 03:14. It is read at 09:00. In the intervening six hours the process
that spawned a shell has done whatever it was going to do. The detection was correct, timely and
useless.

This is the structural weakness of the whole [`../../`](../../README.md) layer: the tools are very
good at noticing and have no opinion about what happens next. In most organisations "what happens
next" is a human, and humans are slow, asleep, and outnumbered by alerts.

Falco Talon closes the gap. It subscribes to Falco's gRPC event stream and runs **actions** against
matched events:

| Action | What it does |
|---|---|
| `kubernetes:terminate` | delete the offending pod |
| `kubernetes:networkpolicy` | apply a deny-all NetworkPolicy so the pod can talk to nothing |
| `kubernetes:label` | label the pod or node, so other tooling can react |
| `kubernetes:exec` / `script` | run a command inside the container |
| `kubernetes:download` / `tcpdump` | capture a file or traffic before killing it — forensics first |
| `aws:lambda`, `calico:networkpolicy`, and others | hand off to external systems |

Rules are declarative: match on Falco rule name, priority, tags, namespace or output fields, then
run one or more actions. A `notifiers` block reports what it did, which matters — an automated
action nobody was told about is worse than no action.

Two design details that make it usable rather than terrifying:

- **`response.actionners` can be limited**, so Talon is only allowed to do the things you granted.
- **Chained actions**, so "capture a tcpdump, then apply a NetworkPolicy, then terminate" is one
  rule. Killing the evidence before collecting it is the classic mistake.

## When to use it

- **For unambiguous detections.** A process writing to `/etc/shadow` inside a container has no benign
  explanation. Those rules are where automated response is straightforwardly correct.
- **When the response is reversible or contained.** Deleting a pod in a Deployment is cheap — the
  ReplicaSet makes another. Applying a NetworkPolicy is reversible. Those are safe automations.
- **To contain rather than remediate.** Isolating a pod with a deny-all NetworkPolicy and labelling
  it for investigation is a better default than terminating it: the attacker loses network access,
  and the evidence stays alive for a human to look at.
- **To collect forensics automatically.** By the time a human logs in, the pod is often gone. A rule
  that captures a tcpdump or a file before acting preserves what the investigation needs.
- **Out of hours.** The gap between detection and response is widest at 03:00, which is when the
  automation is worth most.

## When not to use it

- **Before the rules are tuned.** This is the one that matters. Automated response on an untuned
  Falco is an outage generator: the default rules fire on `kubectl exec`, on init containers running
  package managers, on data workloads spawning processes. Wiring termination to those means killing
  production pods for legitimate activity. Tune first — [`../../README.md`](../../README.md#tuning-is-the-job)
  — then automate the small set of rules you would trust without review.
- **On ambiguous rules.** "Outbound connection to an unusual port" has a hundred benign causes. A
  false positive in detection is an alert someone dismisses; a false positive in enforcement is an
  outage with no obvious cause, because the application log shows a signal, not "a security policy
  killed you".
- **On stateful workloads.** Terminating a database pod, a Kafka broker or a Spark driver is not the
  cheap operation it is for a stateless replica. Scope rules by namespace and workload type.
- **With broad RBAC.** Talon needs permission to delete pods and create NetworkPolicies across the
  cluster, which makes it a very attractive target: compromising Talon means being able to delete
  workloads at will. Grant the narrowest actionners and namespaces that satisfy the rules.
- **Silently.** Every automated action must produce a notification saying what was done and why.
  Otherwise the first anyone knows is a mysteriously restarted workload.
- **Instead of fixing the cause.** Killing the pod repeatedly is not remediation. If a rule fires
  regularly, either the workload is wrong or the rule is.

## Notes

There was no `doc.md` for this folder. What follows is the state of the deployment and how it relates
to the rest.

### How it is deployed here

`helm/helmrelease.yaml`, chart `falco-talon` 0.3.0 in the `falco` namespace:

| Element | State |
|---|---|
| `dependsOn: falco` (namespace `falco`) | correct — it consumes Falco's gRPC stream |
| `values:` | **empty.** The block exists with only the two documentation comments under it |

That empty values block is the honest state of runtime security in this repository: **detection is
wired, response is installed but not configured.** Talon with no rules subscribes to the event stream
and does nothing with any of it.

This is not a criticism of the ordering — installing the response engine before writing rules is
fine, and writing response rules before Falco is tuned would be actively wrong. But it should not be
mistaken for a working control. Right now a Falco detection in this cluster reaches the falcosidekick
web UI and stops there.

### What it needs to become real

In order:

1. **Tune Falco.** Run for a period, sort alerts by frequency, exempt the benign ones narrowly.
   Nothing below is safe until the alert stream is credible.
2. **Pick two or three unambiguous rules.** The ones with no benign explanation on this platform.
3. **Start with containment, not termination.** `kubernetes:label` first — it changes nothing and
   proves the matching works. Then `kubernetes:networkpolicy`. Termination last, and only for
   stateless workloads.
4. **Configure a notifier**, so every action is announced. Falco's own output has no target
   configured here either, so this is the same gap in two places.
5. **Scope the RBAC and the actionners** to exactly what those rules need.

### The gRPC dependency

Talon works only because the Falco HelmRelease sets `falco.grpc.enabled` and
`falco.grpc_output.enabled`. [falco-exporter](../falco-exporter/README.md) depends on the same two
settings. Turning either off during a values cleanup breaks both companions, quietly.

### Where it fits

Of the three Falco companions, this is the one that changes what the layer *is*.
[`../event-generator/`](../event-generator/README.md) proves detection works and
[`../falco-exporter/`](../falco-exporter/README.md) measures it — both useful, neither changes the
outcome of an incident. Talon is the difference between a tool that tells you what happened and a
control that does something about it.

It is also the one component in this subtree where getting it wrong causes an outage rather than
noise, which is why it is deployed unconfigured and should stay that way until Falco's rules are
tuned.

---

[← Falco](../README.md)
