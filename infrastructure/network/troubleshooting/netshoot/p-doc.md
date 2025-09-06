# Troubleshooting Network Issues in Kubernetes
## Problem:
- Need for Additional Pods: The process of diagnosing network issues often requires deploying additional pods in the Kubernetes cluster to install and use various network troubleshooting tools.
- Installation Overhead: Frequent need to install network tool dependencies such as ping, traceroute, tcpdump, and curl manually, which is time-consuming and inefficient.
- Complexity of Network Diagnostics: Network issues in Kubernetes clusters and cloud environments (such as DNS resolution failures, connectivity problems, and misconfigurations) can be difficult to diagnose and resolve without the right tools available within the environment.

## Solution:
- Network Diagnostics Enhancement: Deployed the Netshoot container, which includes a wide array of pre-installed network diagnostic tools like ping, traceroute, nslookup, tcpdump, curl, and dig, eliminating the need to install dependencies each time.
- Simplified Troubleshooting: By using Netshoot, network troubleshooting became more efficient as no additional pods or installations were required, providing an out-of-the-box solution for network diagnostics.
- DNS and Connectivity Visibility: Utilized nslookup and ping to quickly identify DNS resolution issues and connectivity failures between pods, services, and external resources.
- Issue Remediation: Applied corrective measures based on diagnostic results, such as fixing DNS issues, resolving pod communication failures, and adjusting firewall or security group settings for external access.

## Skills:
- Network
- DevOps

## Tools:
- Linux
