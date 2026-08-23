# Kubernetes Ingress Traffic on AWS with AWS Load Balancer Controller

## Problem:
- Load Balancers Provisioned Outside the Workload Lifecycle: Application Load Balancers, listeners, target groups and rules were created manually or in a separate infrastructure pipeline, disconnected from the Kubernetes resources they served. Exposing an application required coordination between two teams, and load balancers were left orphaned and billing after the workload behind them was gone.

- Limited Control with the In-Tree Cloud Provider: The default `type: LoadBalancer` integration provisions a basic load balancer with no L7 capability — no path or host routing, no certificate management, no web application firewall — pushing teams toward one load balancer per service and workarounds for anything more complex.

- Extra Hop and Lost Client Identity: Traffic reaching nodes on a NodePort and being forwarded again by kube-proxy adds a network hop, unbalances traffic across pods, and obscures the original client IP, which weakens both latency and any control that depends on knowing who the caller is.

- Cost of One Load Balancer per Application: With each Ingress provisioning its own load balancer, cost grew linearly with the number of exposed applications, and every new public endpoint expanded the externally reachable surface of the account.

## Solution:
- Kubernetes-Native Load Balancer Provisioning: Deployed the AWS Load Balancer Controller to reconcile Kubernetes resources into AWS load balancers — Ingress into Application Load Balancers and `Service` of type LoadBalancer into Network Load Balancers — so the load balancer, its listeners, target groups and rules are created, updated and deleted as part of the workload's own lifecycle.

- Direct-to-Pod Traffic with IP Target Mode: Configured target groups to register pod IPs directly rather than node ports, removing the extra hop, distributing connections evenly across pods, and preserving the client IP. Target health then follows pod readiness, and deregistration delay is tuned so rolling updates drain connections instead of dropping them.

- Consolidated Ingress with Shared Load Balancers: Grouped Ingress resources from multiple applications and namespaces onto a single shared load balancer with explicit rule ordering, reducing fixed cost per application and limiting the number of public endpoints, while each team continues to own its own Ingress definition.

- Managed TLS Termination: Attached ACM certificates to the load balancer listeners, with automatic renewal handled by AWS and HTTP-to-HTTPS redirection and a modern TLS policy enforced at the edge, removing certificate handling from the applications.

- Least-Privileged Controller Identity: Authenticated the controller with a scoped IAM role bound to its Kubernetes service account, rather than relying on node instance profile permissions, so the privilege to create and modify load balancers belongs to one workload instead of every pod on the node.

- Security Controls at the Edge: Associated a WAF web ACL with the load balancer, managed inbound security groups, and used internal and internet-facing schemes with subnet discovery by tag, so an application is exposed to the internet only when that is what the manifest actually declares.

- Automated DNS and IaC Integration: Combined the controller with ExternalDNS so DNS records follow the provisioned load balancer automatically, and used target group binding to attach load balancers provisioned by Terraform to Kubernetes services — supporting the case where load balancer lifecycle is owned by infrastructure code while routing to pods stays with Kubernetes.

## Skills:
- Platform Engineering
- DevOps
- Cloud Engineering

## Tools:
- AWS Load Balancer Controller
- Amazon EKS
- AWS ACM
- AWS WAF
- Kubernetes
- ExternalDNS
