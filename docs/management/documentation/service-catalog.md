# Platform Service Catalog with GitHub Issue Templates and Projects

## Problem:
- Undocumented Service Offering: The platform team's services existed only as tribal knowledge, so users did not know what could be requested, what was supported, and what was explicitly out of scope.

- Requests Arriving Through Every Channel: Demands came by direct message, chat threads, meetings, and hallway conversations, with no queue, no history, and no guarantee that a request would survive the day it was made.

- Incomplete Request Context: Each request had to be followed by several rounds of questions (environment, dataset, expected volume, access level, justification), delaying the delivery and consuming time from both sides.

- No Prioritization Criteria: Without a common intake, everything looked urgent and priority was decided by whoever insisted more, instead of by impact, effort, and platform roadmap.

- No Demand Visibility: There was no data about which services were requested most, how long each one took, or where the team's capacity was actually being spent, making capacity planning and automation investment guesswork.

- Undefined Ownership and Lifecycle: Services had no declared owner, no lead time expectation, and no deprecation path, so obsolete offerings kept being requested and new ones were never announced.

## Solution:
- Service Catalog as the Single Front Door: Documented every platform and DataOps service (project onboarding, orchestration namespace, streaming topic, data lake area, database provisioning, cluster and tool access, ingestion pipeline, dashboard publication) with description, target audience, prerequisites, owner, expected lead time, and scope boundaries.

- Catalog Entries Backed by Issue Forms: Modeled each catalog item as a GitHub Issue Form, so the request itself collects the fields that service needs, with required inputs and dropdowns replacing free-text tickets and follow-up questions.

- Requests as Cards on GitHub Projects: Routed submitted forms into a GitHub Project board, where each request becomes a card with custom fields (Service, Requesting Team, Priority, Effort, Status, Iteration), giving the intake a visible queue and a triage ritual.

- Automated Triage and Routing: Used labels applied by the templates plus GitHub Actions and project workflows to add items to the board, assign the service owner, and move cards automatically as the work is picked up, linked to a pull request, and delivered.

- Documentation as Code Publication: Published the catalog with the rest of the platform documentation, with each service page linking directly to its request form, keeping the description of the service and the way to request it in the same place and under review in Git.

- Explicit Service Levels and Expectations: Declared for each service what is delivered, what is not, and the expected lead time, replacing informal promises with an agreement users can read before asking.

- Demand Metrics to Drive Automation: Used the board history to measure request volume and lead time per service, and turned the most frequent and most repetitive items into self-service automations and golden paths instead of recurring manual work.

- Catalog Governance and Review: Reviewed the catalog periodically to add new services, update owners, and formally deprecate offerings, so the catalog stays a description of what the platform actually supports.

- No Additional Tooling: Kept intake, tracking, and documentation inside GitHub, reusing the existing organization, teams, and permissions instead of introducing another platform with its own licenses and access reviews.

## Skills:
- Platform Engineering
- Service Management
- Documentation as Code
- Project and Backlog Management
- DevOps

## Tools:
- Github
- Github Issues & Issue Forms
- Github Projects
- Github Actions
- MkDocs
