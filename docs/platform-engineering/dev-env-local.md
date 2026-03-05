# Cost-Efficient Local Development Environment for Data Engineering Teams

## Problem:
- High Cloud Costs: Continuous usage of cloud-based Kubernetes environments for development tasks incurs significant expenses, especially for prototyping, testing, and debugging.
- Resource Waste: Running multiple development environments on Kubernetes clusters in the cloud results in idle resources and increased costs.

## Solution:
- Local Development Environment: Created a fully-functional local development environment capable of running Apache Airflow, JupyterLab, and Visual Studio Code (VSCode) containers, providing a seamless experience equivalent to the cloud-based Kubernetes setup.
- Cost Savings: Reduced cloud infrastructure costs by allowing developers to work on their local machines for prototyping, testing, and debugging, without relying on expensive cloud resources.
- Consistent Environment Configuration: Leveraged Docker Compose to orchestrate services locally, ensuring compatibility with the Helm chart used for Kubernetes deployments.
- Unified Toolset: Provided pre-configured Docker images to replicate the production environment, allowing developers to validate their pipelines and experiments locally before deploying to the cloud.

## Skills:
- DevOps

## Tools:
- Docker
