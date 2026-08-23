# Kubernetes Runtime Threat Detection with Falco

## Problem:
- Blind Spot at Runtime: Admission controllers, posture scanners and image scanners all inspect *intent* — the manifest, the configuration, the image contents. A workload can satisfy every one of those checks and still be compromised at runtime, because the exploit arrives through the application after the container has started, not through the YAML that created it.

- No Visibility into Container Behavior: Without kernel-level observation there is no record of which processes a container executed, which sensitive files it opened, whether it read a service account token, or which outbound connections it made. When an incident happens, the evidence needed to answer "what did it do" was never collected.

- Detection Without Response: Security events that stay in a pod's log output are not actionable. Findings that reach nobody, and that trigger no reaction, provide no protection — teams end up learning about a compromise from somewhere other than their own platform.

## Solution:
- Kernel-Level Runtime Detection: Deployed Falco as a DaemonSet across cluster nodes using the modern eBPF (CO-RE) driver, which requires no kernel module compilation and remains portable across node images and kernel versions. Falco observes syscalls in the kernel and evaluates them against detection rules enriched with container and Kubernetes metadata, so an alert identifies the pod, namespace and image rather than only a process ID.

- Threat Detection Coverage: Enabled detection for the behaviors that indicate an in-progress compromise — a shell spawned inside a container, writes to sensitive system files, reads of Kubernetes service account tokens, package managers executed in running containers, privilege escalation, and unexpected outbound network connections.

- Centralized Event Routing: Configured Falcosidekick to collect detections and fan them out to external destinations, with its web UI for triage — turning per-node event streams into one place where security events are reviewed, instead of logs distributed across every node in the cluster.

- Integration with the Observability Stack: Enabled Falco's gRPC output so detections are consumed by exporters and response tooling, making runtime security events available as Prometheus metrics and to automated response actions. Runtime detection then shares the same alerting and dashboard path as the rest of the platform, rather than being an isolated system with its own notification channel.

- GitOps-Managed Deployment and Rule Tuning: Delivered Falco through Flux as a pinned HelmRelease, so the deployment, its driver choice and its configuration are versioned in Git and reproducible. Rule tuning — the ongoing work that keeps runtime security from becoming noise nobody reads — is reviewed as a pull request diff rather than applied by hand to a live cluster.

## Skills:
- Security
- DevSecOps
- Platform Engineering

## Tools:
- Falco
- Falcosidekick
- eBPF
- Kubernetes
- Flux
- Prometheus
