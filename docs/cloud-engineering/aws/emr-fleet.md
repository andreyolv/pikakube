# Cost-Resilient EMR Clusters with Instance Fleets and Spot Diversification

## Problem:
- Rigid Capacity with Instance Groups: EMR clusters provisioned with instance groups depended on a single instance type per node role, so any shortage of that type in the selected Availability Zone caused provisioning failures or long waits.

- Spot Interruptions Killing Jobs: Concentrating Spark executors on one Spot instance type made the cluster highly exposed to interruption events, causing job failures, retries, and unpredictable pipeline SLAs.

- Cost Pressure on Batch Processing: Running the whole cluster on On-Demand capacity to guarantee stability made large Spark batch workloads one of the most expensive items of the data platform.

- Manual Instance Type Selection: Choosing instance types by hand for each workload was slow, quickly became outdated as new generations were released, and did not account for real-time Spot capacity and pricing.

- Single Availability Zone Constraint: Clusters pinned to one subnet could not take advantage of spare capacity in other Availability Zones, reducing both resilience and access to cheaper Spot pools.

- Unclear Sizing Model: Capacity was reasoned about in "number of nodes", which does not reflect the actual vCPU and memory delivered when mixing heterogeneous instance types.

## Solution:
- Instance Fleets Adoption: Migrated EMR clusters from instance groups to instance fleets, allowing each node role (master, core, task) to be satisfied by a list of candidate instance types instead of a single one.

- Diversified Spot Pools: Declared multiple instance types and generations per fleet, spreading executors across many Spot capacity pools so a single pool interruption no longer compromises the job.

- Mixed Purchase Model: Kept master and core nodes on On-Demand for HDFS and application-master stability, while running task nodes on Spot, capturing the largest share of savings on the elastic part of the cluster.

- Capacity-Optimized Allocation Strategy: Configured the allocation strategy so EMR provisions Spot capacity from the deepest available pools instead of only the cheapest ones, significantly reducing interruption rates for long-running Spark jobs.

- Target Capacity in Units: Modeled fleet sizing with target capacity units weighted per instance type (based on vCPU/memory), so the cluster provisions the required processing power regardless of the mix of instance types actually obtained.

- Multi-Subnet, Multi-AZ Provisioning: Configured fleets with subnets across multiple Availability Zones, letting EMR place the cluster where capacity and price are best at launch time.

- Provisioning Timeout and Fallback: Defined Spot provisioning timeouts with an On-Demand fallback action, guaranteeing that critical pipelines still start when Spot capacity is unavailable instead of hanging or failing.

- Infrastructure as Code: Codified cluster and fleet definitions in Terraform, versioning instance type lists, weights, and allocation strategies so changes are reviewed and reproducible across environments.

- Cost and Interruption Visibility: Tracked cluster cost per job and Spot interruption events, using the data to refine instance type lists and to prove the savings achieved against the previous On-Demand baseline.

## Skills:
- Cloud Engineering
- Data Engineering
- FinOps

## Tools:
- AWS EMR
- AWS EC2 Spot
- Apache Spark
- Terraform
