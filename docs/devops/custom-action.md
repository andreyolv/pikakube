# Airflow DAG Quality Assurance in CI/CD with Custom GitHub Action

## Problem:
- Quality Testing for Airflow DAGs: Integrating quality tests into the CI/CD pipeline for Airflow DAGs is crucial to identify errors early in the deployment process, preventing issues from reaching production.
- Production Deployment Restrictions: Ensure that only DAGs that meet the established quality standards are deployed to production, preventing not stantad and not governance quality DAGs.

## Solution:
- Custom GitHub Actions: Developed custom GitHub Actions to automatically run multiple quality tests on each Airflow DAG, detecting errors early and streamlining the testing process.
- Pytest for Policy Testing: Used Pytest to run tests for each quality policy, ensuring consistent and reliable checks across all DAGs.
- Mocking Variables and Connections: Implemented mock variables and connections to facilitate the testing process, eliminating the need for local storage and simplifying setup.
- Airflow Quality Policies: Validated key attributes such as import errors, executor configuration existence, DAG run timeout limits, valid executor configuration namespaces, presence of owners and tags, and defined CPU/memory requests in the executor configuration.
- Ensuring Compliance with Standards: Enforced governance and compliance by ensuring that only DAGs meeting established standards and quality criteria are deployed to production.

## Skills:
- DevOps
- Data Engineering

## Tools:
- Python
- Pytest
- Airflow
- Github Actions
