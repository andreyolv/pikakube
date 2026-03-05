# Container Registry Insights and Image Lifecycle Management

## Problem:
- Limited Visibility: Container registries often lack critical insights, such as image sizes and total repository storage consumption. Without this visibility, managing and monitoring storage resources effectively becomes challenging.
- No Automated Image Lifecycle Management: Many registries do not provide built-in capabilities to automatically manage the lifecycle of unused or outdated images. This forces teams to rely on manual intervention or custom scripts, leading to inefficient storage usage and potential cost overruns.

## Solution:
- Registry Insights Tool: Developed a Python-based tool to analyze and report storage usage across container registries. The tool aggregates key metrics including: total size per repository, oldest and newest images, image count per repository, and average/maximum image sizes. These insights enable informed planning and resource optimization.
- Image Lifecycle Policies: Implemented automated policies to manage image retention, defining rules such as keeping a certain number of recent images or retaining images within a specified time frame. This approach ensures optimized storage usage while preserving necessary resources for active workloads, reducing operational overhead and improving efficiency.

## Skills:
- Data Engineering
- DevOps
- Cloud Computing

## Tools:
- Azure Container Registry
- Python
