# Network Observability in Kubernetes with Retina and Hubble

## Problem:
- Lack of Network-Level Visibility: Kubernetes lacks built-in tools for deep visibility into network communication between workloads, making it difficult to troubleshoot connectivity issues or enforce security policies.
- No Contextual Flow Insights: Existing network tools provided raw metrics or packet captures but lacked Kubernetes context (e.g., pod, namespace, service).
- Blind Spots in Inter-Pod Traffic: Especially in large multi-tenant clusters, it was challenging to monitor east-west traffic across namespaces and applications.
- Slow Incident Response: Debugging network latency or denied connections involved time-consuming manual investigation across logs, network policies, and firewall rules.
- Limited Developer Insights: Developers had little access to how their applications communicated over the network, reducing their ability to optimize or secure workloads.

## Solution:
- Deployed Retina with Hubble UI: Implemented Microsoft’s Retina to capture and export enriched network flow logs from Kubernetes workloads, with Hubble UI for visualization.
- eBPF-Based Visibility: Used eBPF to capture real-time L3/L4 flow data without sidecars or intrusive agents, ensuring performance and scalability.
- Lightweight Alternative to Cilium: Chose Retina as a lightweight alternative to Cilium when the requirement is limited to observability and not full service mesh, security policies, or advanced networking. Unlike Cilium, Retina works with any CNI, offering flexibility to integrate network observability into existing clusters without requiring CNI replacement.
- Application-Aware Monitoring: Achieved full visibility of pod-to-pod, service-to-service, and namespace-to-namespace communication with Kubernetes context, enabling faster debugging and traffic analysis.
- Improved Security Posture: Identified unused or excessive network permissions, aiding in the creation of least-privilege network policies.
- Integrated with Prometheus and Grafana: Exposed flow metrics through ServiceMonitors and custom dashboards, providing real-time insights into network latency, connection errors, and throughput.

## Skills:
- 

## Tools:
- 

