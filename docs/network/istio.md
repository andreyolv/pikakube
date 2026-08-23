# Kubernetes Service-to-Service Traffic Security and Control with Istio

## Problem:
- Unencrypted and Unauthenticated East-West Traffic: Pod-to-pod communication inside the cluster is plaintext by default, and any pod can reach any other pod. Network Policies restrict connectivity at L3/L4 by IP and label, but they cannot authenticate the workload on the other end of a connection, so there is no cryptographic proof of which service is calling which.

- Resilience Logic Duplicated in Applications: Retries, timeouts, circuit breaking and connection pooling are implemented inside each application, in a different language and library per service. Behaviour is inconsistent, changing it requires a code release, and a service that misbehaves under load takes its callers down with it.

- No Consistent Visibility Between Services: Latency, error rate and request volume per service dependency are unavailable without instrumenting every application. When a request is slow, there is no shared view of which hop in the call chain is responsible.

- Risky Releases: Shifting a percentage of traffic to a new version requires application-level flags or ingress-level workarounds, so releases tend to be all-or-nothing and rollbacks are slow.

## Solution:
- Service Mesh for East-West Traffic: Deployed Istio to manage service-to-service communication inside the cluster, with `istiod` as the control plane and Envoy proxies as the data plane. North-south ingress remains with Gateway API and Envoy Gateway — the mesh governs traffic between services, not the cluster edge.

- Automatic mTLS with Workload Identity: Enabled mutual TLS between meshed workloads, with certificates issued and rotated automatically per service account. Traffic is encrypted in transit and each connection carries a cryptographic workload identity, which is the property IP-based rules cannot provide. Enforced strict mode so plaintext connections between meshed services are refused rather than silently accepted.

- Authorization Based on Identity, Not Address: Applied authorization policies that allow specific service identities to call specific services and methods, denying everything else. This complements Network Policies rather than replacing them: the network layer restricts reachability, and the mesh decides which identity is permitted to make the call.

- Traffic Management Outside Application Code: Moved retries, timeouts, outlier detection and load balancing configuration into mesh resources, applied uniformly to every service regardless of language. Circuit breaking removes a failing dependency from rotation automatically, containing failures instead of propagating them.

- Progressive Delivery: Used weighted traffic splitting to release new versions gradually — canary and blue/green — with the ability to shift traffic back immediately, turning a release into a reversible operation instead of a deployment event.

- Observability Without Instrumenting Applications: Collected per-service request rate, error rate and latency metrics from the proxies into Prometheus, visualized as service-level dashboards and a live dependency graph. The proxies also emit spans for distributed tracing, with applications forwarding trace context headers so the call chain remains connected end to end.

- Reduced Overhead with Ambient Mode: Evaluated Istio's sidecar-less data plane, where a per-node component provides mTLS and L4 authorization for all workloads and dedicated L7 proxies are deployed only for the services that need policy or traffic management. This removes a sidecar container from every pod and lowers the resource cost of enrolling workloads that only need encryption and identity.

## Skills:
- Platform Engineering
- Security
- DevOps

## Tools:
- Istio
- Envoy
- Kubernetes
- Prometheus
- Grafana
