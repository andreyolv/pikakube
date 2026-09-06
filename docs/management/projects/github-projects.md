# Agile Activity Management with GitHub Projects

## Problem:
- Work Tracking Outside the Codebase: Activities were tracked in tools disconnected from the repositories, forcing the team to duplicate context between the board and the pull requests where the work actually happened.

- No Single Source of Truth: Priorities, sprint scope, and delivery status lived in spreadsheets and chat threads, making it hard to know what was in progress, who owned it, and what was blocked.

- Manual Status Updates: Moving cards between columns depended on people remembering to do it, so boards drifted out of sync with the real state of the code and stopped being trusted.

- Poor Visibility for Stakeholders: There was no consolidated view of the platform roadmap, sprint progress, or delivery history to share with other teams and leadership.

- Weak Traceability: It was difficult to trace a delivered feature or an incident fix back to its planning item, its discussion, and the commits that implemented it.

- Inconsistent Agile Practice: Each initiative used a different notion of backlog, sprint, and "done", preventing any comparison of throughput or predictability across projects.

## Solution:
- Kanban and Scrum Boards on GitHub Projects: Adopted GitHub Projects as the planning layer for platform activities, with a Kanban board for continuous flow demands (operations, support, incidents) and Scrum-style iterations for roadmap work.

- Issues as the Unit of Work: Standardized every activity as a GitHub Issue with issue templates, so bugs, tasks, and platform requests are created with the required context (impact, environment, acceptance criteria).

- Custom Fields for Planning: Modeled Status, Priority, Effort, Iteration, and Area as project fields, enabling sprint planning, capacity discussion, and prioritization without external tooling.

- Multiple Views over the Same Data: Configured board, table, and roadmap views with filters and grouping, so the team sees the sprint while stakeholders see the timeline and the delivery history from a single backlog.

- Automated Status Transitions: Used built-in project workflows and GitHub Actions to move items automatically when an issue is opened, when a pull request is linked, when a review is requested, and when the pull request is merged, keeping the board synchronized with the code.

- Traceability Between Planning and Code: Linked issues to pull requests and commits, so every delivery carries the reason it was made, the discussion that shaped it, and the change that implemented it.

- Cross-Repository Portfolio: Organization-level projects aggregate issues from all platform repositories, giving one backlog for infrastructure, data, and application work that would otherwise be fragmented per repository.

- Delivery Metrics: Used iteration and status history to follow throughput, work in progress, and aging items, supporting retrospectives with data instead of perception.

- Governance and Access: Centralized project permissions with the existing GitHub organization and team structure, avoiding an extra tool with its own users, licenses, and access review process.

## Skills:
- Agile Methodologies (Kanban / Scrum)
- Project and Backlog Management
- DevOps

## Tools:
- Github
- Github Projects
- Github Issues
- Github Actions
