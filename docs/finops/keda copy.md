# Event-Driven Autoscaling in Kubernetes Using KEDA for Resource and Cost Optimization

## Problem:
- Limited Scaling Flexibility with HPA: Horizontal Pod Autoscaler (HPA) in Kubernetes is typically limited to scaling based on CPU and memory usage, which doesn't address the need for more flexible scaling based on other factors or triggers for certain workloads.
- Resource Optimization During Off-Hours: There is a need to optimize the usage of Kubernetes resources by automatically scaling down non-essential applications outside of business hours, reducing unnecessary resource consumption and costs.

## Solution:
- Efficient Resource Allocation with KEDA: KEDA ensures resources are allocated efficiently, scaling applications only when necessary, preventing over-provisioning, and reducing costs by avoiding resource waste.
- Cron-Based Scaling for Applications: Implemented KEDA (Kubernetes Event-Driven Autoscaling) to scale applications based on a cron schedule. Web frontend applications are only active between 8 AM and 8 PM, Monday to Friday, and are automatically scaled down during off-hours.
- Event-Driven Scaling for Worker Applications: For worker applications processing user requests, KEDA was used to request resources only when there are tasks to be executed. Instead of running a constant loop checking a database, KEDA scales applications based on events, such as detecting tasks in the "queued" state in a PostgreSQL scaler. 
- Custom Resource Requests for Workloads: KEDA allows scaling worker applications based on the data volume associated with each request. For example, worker pods are scaled to different sizes depending on the number of transporters involved in a request.
- Optimized Batch Task Execution for Resource Efficiency: For tasks where immediate execution is not cost-effective, KEDA is utilized to trigger task execution based on the request threshold in a Redis List scaler. Tasks are executed only when a sufficient number of requests accumulate in the queue, preventing frequent initializations and optimizing resource usage.

## Future Improvements:
- keda custom trigger 
- keda http

## Skills:
- DevOps
- FinOps

## Tools:
- KEDA (Kubernetes Event-driven Autoscaling)
- Kubernetes
- PostgreSQL
- Redis
