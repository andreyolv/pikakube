[← Attack path](../README.md)

# kube-hunter

<https://github.com/aquasecurity/kube-hunter>

Context and comparison against the other tools: [../README.md](../README.md)

> **Not under active development.** The upstream repository states: *"kube-hunter is not
> under active development anymore. If you're interested in scanning Kubernetes clusters for
> known vulnerabilities, we recommend using Trivy."* Everything below is written on that
> basis. Do not build a pipeline around it.

---

## The problem it solves

kube-hunter probes a cluster for **known weaknesses that are visible from a given vantage
point**, and the vantage point is the whole idea. It does not read your manifests and it
does not ask the API server nicely. It behaves like an attacker who has just arrived and is
looking around:

| Mode | Vantage point | The question it answers |
|---|---|---|
| `--pod` | **inside a pod**, using the mounted ServiceAccount | "I have compromised one workload. What can I see and reach from here?" |
| `--remote <host>` | from outside, against a named host | "What is exposed on this control plane node?" |
| `--cidr <range>` | from outside, sweeping a network range | "What Kubernetes is reachable on this network at all?" |
| `--interface` | from outside, on every local interface | discovery on an unknown network |

The checks are the classic exposure list: anonymous access to the API server, an open
read/write **kubelet API** on 10250/10255, an unauthenticated etcd on 2379, an exposed
dashboard, cAdvisor, the read-only kubelet port, certificate and token disclosure, and
whether the mounted ServiceAccount token can do anything interesting.

The `--pod` mode is the one worth caring about. It is the only cheap way to answer "what
does a compromised container actually see", and the answer on a default cluster is
routinely more than people expect: a reachable kubelet, a token with real permissions, and
the cloud metadata endpoint.

## When to use it

- As a **one-off sanity check** from inside a pod, to see the cluster the way a compromised workload sees it
- On a lab or local cluster, as a teaching tool — the output maps cleanly onto the controls in `network-policies/`, `pod-security/` and `identity-access/`
- To confirm a specific exposure you already suspect (an open kubelet port, anonymous API access) without writing the probe yourself

## When not to use it

- **As a maintained control.** It is not under active development. New Kubernetes versions, new default hardening and new exposure classes will not be covered. Upstream points to [Trivy](https://github.com/aquasecurity/trivy) instead, and for benchmark-style checks the tools in `posture/` (kube-bench, kubescape) are the maintained path
- In CI, as a gate. A deprecated scanner producing an unmaintained check list is a false sense of coverage, and its findings will drift
- On a cluster you are not authorised to test. It actively probes ports and endpoints. In a shared or production environment this is an unannounced scan and will be treated as one
- As a posture or compliance tool. It reports reachable weaknesses, not conformance with CIS. Auditors want the second
- Expecting exploitation. It reports; it does not break in. `--active` mode does more intrusive probing and should be treated with real care

## Notes

The original note in this folder was the project link and nothing else:

- <https://github.com/aquasecurity/kube-hunter> — the upstream repository, from Aqua Security.

Points worth recording alongside it:

- **Deprecation, verified upstream.** The repository carries the notice quoted at the top of
  this page. Aqua's replacement recommendation is **Trivy**, which is a vulnerability and
  misconfiguration scanner rather than a network prober, so the replacement is not
  like-for-like: the `--pod` "what can I reach from here" perspective genuinely has no
  direct successor. That perspective is now better served by
  [KubeHound](../kubehound/README.md), which models reachability as a graph instead of
  probing for it.
- **The manifests in this folder run the `--pod` mode.**
  [`namespace.yaml`](namespace.yaml) creates a `kube-hunter` namespace and
  [`job.yaml`](job.yaml) runs a one-shot `Job` with `image: aquasec/kube-hunter:0.6.8` and
  `args: ["--pod"]`, `restartPolicy: Never`. Read the results with
  `kubectl logs -n kube-hunter job/kube-hunter`. Note that the Job runs with the
  **default ServiceAccount** of that namespace, so what it reports as reachable is what the
  *default* token can reach — which is the realistic baseline, and exactly the point.
- **The pinned version is old** (0.6.8) and, given the deprecation, is effectively the end
  of the line. Pin it deliberately rather than tracking `latest`.

---

[← Attack path](../README.md)
