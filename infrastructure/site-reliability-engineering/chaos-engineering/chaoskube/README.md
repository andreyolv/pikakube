[← Chaos engineering](../README.md)

# chaoskube

<https://github.com/linki/chaoskube>

---

## The problem it solves

It kills a random pod every *N* minutes. That is the entire tool.

The value is not the fault — it is the **continuous pressure**. Resilience decays quietly: a
Deployment drops to one replica, someone adds a `hostPath`, a service starts caching state in
memory. Nothing alerts, and the system stays fine until the day a pod actually dies.

Running chaoskube means that day is today, and every day, in daylight.

Selectors bound it: namespace, labels, annotations, and the time window when it may act — so
"weekdays, business hours, staging only" is a configuration rather than a policy document.

## When to use it

- **continuous** low-effort verification that pods can be lost
- keeping resilience honest without designing experiments
- a first step for a team new to chaos engineering, where the platforms are too much

## When not to use it

- you need a hypothesis and a recorded result — [LitmusChaos](../litmus/README.md)
- faults beyond pod termination — [Chaos Mesh](../chaos-mesh/README.md)
- teams should opt **in** rather than be opted out — [kube-monkey](../kubemonkey/README.md) uses annotations
- there is no alerting yet, in which case this produces outages instead of learning

## The honest framing

Deliberately trivial, and that is the feature. It answers one question — *can this system lose
a pod?* — continuously, with almost nothing to operate.

It is not a substitute for designed experiments. It is the background pressure that stops the
answer from silently becoming "no".

---

[← Chaos engineering](../README.md)
