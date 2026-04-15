# FAQ

## Why not use GitHub-hosted runners?
Some workflows must access internal services through private endpoints and/or must execute within a controlled private network for security and compliance.

## What does ARC do?
Actions Runner Controller manages runner lifecycle on Kubernetes, including registration and reconciliation.

## How does scaling work?
Runner Scale Sets adjust runner count based on workflow demand, within configured limits.

## Why use a custom runner image?
To include required tooling/dependencies ahead of time, improving performance and consistency.

## What should I do if my job is stuck in queue?
Check runner availability and labels, then consult `../ops/playbook.md`.
