# Runbook

## Consumer Pipeline Failing
- Identify workflow version used by the consumer.
- Reproduce with the same inputs.
- Check for:
  - missing required inputs/secrets
  - permissions regressions (`permissions:`)
  - changed defaults in the workflow repo
- Roll back consumer to last known-good tag if needed.

## New Release Causing Incidents
- Pause adoption.
- Publish hotfix tag.
- Communicate mitigation steps to consumers.
- Identify whether the issue is:
  - workflow logic regression
  - dependency version drift
  - permission/token scope issue
