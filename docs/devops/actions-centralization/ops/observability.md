# Observability

## What to Monitor
- Reusable workflow adoption and version distribution.
- Failure rates by workflow version.
- Time to complete key pipelines (lead time per workflow type).
- Top failing workflows and most common failure reasons.
- Rollback frequency after new tags.

## Signals
- Increased failures after a new workflow release.
- Consumers stuck on old versions.
- Repeated permission errors (token scope regressions).
- Sudden increase in job duration (dependency changes, caching regressions).
