# GitHub Repository Templating for Automated Project Setup with Backstage
## Problem:
- Manual Repository Creation: Manually creating new repositories is time-consuming and error-prone, slowing down the process of initiating new projects and creating inconsistencies across repositories.
- Repository Template Management: The need to create and maintain GitHub repository templates to streamline project creation and standardize repository structures across multiple teams. This required templates tailored for various project types, ensuring consistency in configurations, documentation, and Github Actions pipelines.

## Solution:
- GitHub Repository Templates with Cookiecutter: Implemented Cookiecutter, a Python command-line utility, to automate the creation of GitHub repository templates. Developed a set of reusable templates, each pre-configured with best practices, project structures, documentation, and tooling relevant to different types of projects (e.g., data engineering pipelines, data scienice).
- Template Customization: Allowed teams to customize the templates based on project-specific requirements, ensuring a flexible yet standardized setup for different use cases.
- Integration with Backstage: Integrated the repository creation process into Backstage, enabling teams to request new repositories via a user-friendly interface. This streamlined the workflow and minimized manual intervention, further reducing the risk of inconsistencies.

## Skills:
- DevOps
- Platform Engineering

## Tools:
- Python
- Cookiecutter
- Github
- Backstage