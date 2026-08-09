[← Chaos engineering](../README.md)

# kube-monkey

<https://github.com/asobti/kube-monkey>

---

## The problem it solves

Netflix's Chaos Monkey, for Kubernetes: it terminates pods on a schedule during a defined
window.

Its distinguishing property is **opt-in**. A workload participates only if it carries the
annotation:

```yaml
metadata:
  labels:
    kube-monkey/enabled: enabled
    kube-monkey/identifier: my-app
    kube-monkey/mtbf: "2"        # mean time between failures, in days
```

That inverts the politics of chaos engineering, and the politics are usually the hard part.
Instead of a platform team terminating other people's pods, each team declares that theirs can
survive it — and the annotation becomes a small, visible claim about resilience.

## When to use it

- **teams should opt in** rather than be opted out
- a gradual rollout, where adoption grows as confidence does
- the annotation itself is useful documentation: which workloads claim to tolerate pod loss

## When not to use it

- cluster-wide pressure regardless of opt-in — [chaoskube](../chaoskube/README.md)
- fault types beyond pod termination — [Chaos Mesh](../chaos-mesh/README.md)
- you need recorded results and hypotheses — [LitmusChaos](../litmus/README.md)

## Why the opt-in model is worth considering

Chaos engineering usually fails for organisational reasons, not technical ones — someone
objects, and the programme quietly stops.

Making it opt-in removes the objection and turns participation into a signal. A workload
without the annotation is not protected; it is **undeclared**, and that gap is itself useful
information about where resilience has never been claimed.

---

[← Chaos engineering](../README.md)
