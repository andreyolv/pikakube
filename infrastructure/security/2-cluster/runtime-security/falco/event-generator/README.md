[← Falco](../README.md)

# event-generator

<https://github.com/falcosecurity/event-generator>
<https://github.com/falcosecurity/charts>

Deliberately performs suspicious actions so you can confirm Falco's rules actually fire.

---

## The problem it solves

A security control that has never triggered is indistinguishable from a security control that does
not work. Falco can be running, healthy, reporting no errors, and detecting nothing — because the
driver did not attach, because a rule was disabled during tuning, because the output path is broken,
or because `resourceFilters`-style exclusions ended up wider than intended.

Nothing in the deployment tells you. A quiet cluster and a broken agent look identical.

event-generator solves that by producing the activity the rules are written to catch: writing below
`/etc` in a container, spawning a shell, reading a service account token, running a package manager,
touching sensitive files, modifying binary directories. Each action maps to a Falco rule, so a
successful run should produce a predictable set of detections.

Three modes matter:

| Mode | What it does |
|---|---|
| `run` | performs the actions once and exits |
| `test` | performs the actions **and checks that Falco reported them**, via the gRPC API — a pass/fail result rather than "look at the logs" |
| `bench` | generates events at a high rate to measure throughput and drops |

The `test` mode is the one that turns this from a demo into a control: it closes the loop
automatically rather than leaving a human to correlate two log streams.

`bench` answers a different and underrated question — at what event rate does Falco start dropping
syscalls? A dropping agent is a blind agent, and on high-syscall workloads (Spark, Airflow, anything
process-heavy) that limit is reachable.

## When to use it

- **Immediately after deploying Falco.** Before trusting it, prove it sees something. This is the
  single best use of the tool.
- **After changing the driver.** Switching between kernel module and eBPF, or upgrading the kernel,
  changes whether Falco can see anything at all — and the failure is silent. The
  [Falco notes](../README.md) record exactly that failure mode.
- **After tuning.** Every exception narrows what Falco reports. Re-running the generator confirms
  you narrowed the intended rule and not three others.
- **To test the whole pipeline, not just detection.** If the alert is supposed to reach Slack or
  Prometheus, generate an event and check it arrives at the far end. Detection that does not reach a
  human is not detection.
- **In CI, on an ephemeral cluster.** `test` mode gives an exit code, so "is the runtime security
  stack working" becomes an automated check.
- **To size the agent.** `bench` mode plus the drop counters tells you whether the node can keep up.

## When not to use it

- **Continuously, in a loop, in production.** This is the important warning. The generator performs
  genuinely suspicious actions. Left looping, it produces a constant stream of true positives that
  train everyone to ignore the alert channel — and it makes a real detection indistinguishable from
  the noise. Run it, check, stop.
- **Without telling whoever watches the alerts.** Someone paging at 2am over an event you generated
  is a good way to lose credibility for the whole programme.
- **In a shared or production cluster, casually.** Some actions modify files and spawn processes.
  They are designed to be harmless, and "designed to be harmless" is not the same as "harmless in
  your environment".
- **As a substitute for tuning.** It proves the rules fire on synthetic activity. It says nothing
  about how many false positives your real workloads produce, which is the actual problem —
  [`../../README.md`](../../README.md#4-the-alert-volume-problem).
- **As a substitute for real attack simulation.** It exercises Falco's own rules. It does not tell
  you whether an actual attacker technique would be caught; that is a red-team question.

## Notes

There was no `doc.md` for this folder. What follows is the state of the deployment and how it relates
to the rest.

### How it is deployed here

`helm/helmrelease.yaml`, chart `event-generator` 0.3.1 in the `falco` namespace:

| Setting | Meaning |
|---|---|
| `dependsOn: falco` (namespace `falco`) | Flux will not install it until the Falco HelmRelease is ready — necessary, since generating events before Falco is watching proves nothing |
| `config.loop: false` | **the important one.** Run the actions once and stop, rather than continuously |

`loop: false` is the correct setting and the one to defend in review. The chart's looping mode exists
for demos and dashboards; in a cluster where anyone is expected to act on a Falco alert, a permanent
generator is an alert-fatigue machine.

Even with `loop: false`, this is a workload that deliberately trips security rules. It is deployed
here as part of a learning platform, and in a real cluster it belongs as a job someone runs, not as
a HelmRelease that Flux keeps reconciling.

### Reading the result

The generator's own log lists the actions it performed. Falco's output — the sidekick web UI in this
deployment — should show a corresponding detection for each.

If they do not match, the order to check is:

1. `kubectl logs daemonset/falco -n falco -c falco-driver-loader` — did the driver attach at all?
   With `driver.kind: modern-bpf` this should be a no-op, and anything else there is a signal.
2. Falco's own log — is the rule loaded, or was it disabled or overridden?
3. The output path — falcosidekick is enabled here, and if the event reached Falco but not the UI,
   the problem is routing, not detection.
4. The drop counters — a saturated agent silently misses events.

### Where it fits

This is the verification half of the Falco stack. [`../falco-exporter/`](../falco-exporter/README.md)
makes detections measurable and [`../falco-talon/`](../falco-talon/README.md) makes them actionable;
this is what proves there is anything to measure or act on.

The three companions together are what makes the Falco folder in this repository worth more than a
bare agent install — and this is the one that takes five minutes and prevents the most embarrassing
possible outcome, which is discovering during an incident that the agent was never seeing anything.

---

[← Falco](../README.md)
