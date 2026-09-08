# Cloud Resource Inventory and Orphaned Resource Reclamation with AWS Resource Explorer

## Problem:
- No Unified Resource Inventory: Resources were spread across multiple accounts and regions with no single place to list them, so answering "what do we actually run?" required opening the console region by region and service by service.

- Orphaned Resources Accumulating Cost: Deleted workloads left leftovers behind — unattached EBS volumes, unassociated Elastic IPs, idle NAT Gateways and load balancers, old snapshots and AMIs, empty ECR repositories, unused security groups and IAM roles — all billed monthly with nobody noticing.

- Idle Resources Without Owner: Provisioned-for-a-test resources stayed alive indefinitely because there was no tag, no owner, and no expiration, making it impossible to ask anyone for a decision about them.

- Resources Outside Infrastructure as Code: Manually created ("ClickOps") resources were invisible to Terraform, so the IaC state was not a reliable inventory and drift between what was declared and what existed kept growing.

- Fear of Deleting Something in Use: Without usage evidence and a reversible process, cleanup was postponed because the risk of breaking an unknown dependency was higher than the perceived saving.

- Cleanup as a One-Off Effort: When cleanup did happen, it was a manual campaign triggered by a cost spike, with no recurring routine, no record of what was removed, and no measurement of the savings achieved.

## Solution:
- Cross-Region and Cross-Account Inventory with AWS Resource Explorer: Enabled an aggregator index in the primary region with local indexes in every active region, providing a single searchable inventory of resources by type, region, account, and tag.

- Saved Views and Queries per Audit Intent: Created reusable Resource Explorer views and queries (untagged resources, resources by team tag, resources by type and region) so recurring audits became a query instead of an exploration.

- Resource Classification Taxonomy: Classified findings into orphaned (parent resource no longer exists), idle (no usage over an observation window), unmanaged (exists in the cloud but not in Terraform state), and unowned (missing ownership tags), because each class requires a different decision and a different owner.

- Usage Evidence Before Any Deletion: Correlated the inventory with CloudWatch metrics, Cost and Usage Report data queried via Athena, and Trusted Advisor / Compute Optimizer findings to prove a resource was unused before proposing its removal.

- Drift Detection Against Infrastructure as Code: Compared the Resource Explorer inventory with Terraform state to detect resources created outside the pipeline, either importing them into IaC or scheduling them for removal.

- Reversible Decommissioning Workflow: Standardized a quarantine flow — tag the candidate for removal, notify the owner with the cost and usage evidence, respect a grace period, snapshot or back up when applicable, and only then delete through Terraform — keeping every step auditable and reversible.

- Ownership Enforcement to Prevent New Waste: Reinforced the tagging standard with mandatory ownership and environment tags so newly created resources always have a responsible team, closing the loop that generated unowned resources in the first place.

- Recurring FinOps Routine: Turned the audit into a scheduled cycle inside the FinOps routine, with automation (Python/boto3 and scheduled GitHub Actions) generating the candidate list, opening tracking issues, and reporting monthly reclaimed spend per team.

- Savings Reporting and Accountability: Reported reclaimed cost separated by team and resource class, converting cleanup from an invisible maintenance chore into a measurable and repeatable cost reduction result.

## Skills:
- FinOps
- Cloud Engineering
- Cloud Governance
- DevOps

## Tools:
- AWS Resource Explorer
- AWS Resource Groups & Tag Editor
- AWS Cost Explorer & Cost and Usage Report
- AWS Trusted Advisor
- Amazon CloudWatch
- Amazon Athena
- Terraform
- Python (boto3)
- Github Actions
