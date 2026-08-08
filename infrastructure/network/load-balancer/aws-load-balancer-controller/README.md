[← Load balancer](../README.md)

# AWS Load Balancer Controller

<https://github.com/kubernetes-sigs/aws-load-balancer-controller>
<https://kubernetes-sigs.github.io/aws-load-balancer-controller/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

On EKS, `type: LoadBalancer` already works — the in-tree cloud provider creates a Classic or
Network Load Balancer. This controller replaces that with something far more capable:

- **`Ingress` → ALB** — an Application Load Balancer provisioned from the Ingress object, with host and path routing done by AWS rather than by a pod
- **`Service` → NLB** — a Network Load Balancer, with fine-grained control over its attributes
- **IP target mode** — the load balancer sends traffic **straight to pod IPs**, skipping the node hop and `kube-proxy`
- integration with ACM certificates, WAF, Shield and security groups through annotations

## When to use it

- running on **EKS**, and wanting AWS to terminate TLS with an ACM certificate — see [certificates](../../../security/2-cluster/certificates/README.md#7-managed-certificate-services-in-the-cloud), where this is exactly the case that makes ACM the right choice
- you want WAF or Shield in front of the cluster
- you want to remove the in-cluster ingress controller from the data path entirely

## When not to use it

- anywhere that is not AWS
- when TLS must terminate **inside** the cluster — ACM certificates cannot be exported, so an in-cluster ingress controller plus cert-manager is the alternative
- when portability matters; the annotations are AWS-specific and do not travel

## The trade

TLS and routing move out of the cluster and into AWS. Less to run, and less that is portable
— the routing rules now live in ALB configuration rather than in a manifest that works
anywhere.

---

[← Load balancer](../README.md)
