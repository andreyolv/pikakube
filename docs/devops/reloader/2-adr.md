# ADR-00X: Automated Pod Rollouts Triggered by ConfigMap and Secret Changes

Status: Proposed 
Deciders: Andrey Oliveira 
Consulted: [DevOps Team, Platform Engineering] 
Date: 2025-11-14

Kyverno was initially evaluated as an alternative for enforcing reload policies. However, Kyverno requires significantly more setup, custom policies, and integration complexity. Reloader, on the other hand, is extremely lightweight, easy to deploy, and achieves the same goal with minimal configuration.

