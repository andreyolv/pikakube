# Observability

## What to Monitor
- Plan/apply failure rates (by repo, environment, and workflow version).
- Concurrency contention (queued runs, canceled runs, and lock wait time).
- Backend errors (state lock, `AccessDenied`, missing backend resources).
- Drift signals (apply failures caused by out-of-band changes).
- Lead time signals:
  - time from PR opened -> plan produced
  - time from merge -> apply completed
- Security signals:
  - role assumption failures
  - denied actions indicating least-privilege gaps

## Signals
- Frequent state lock failures or long lock wait time.
- Apply divergence from PR plan (plan artifact not found, re-plan happening unexpectedly).
- Repeated `AccessDenied` during apply (role policy regression).
- Increased rollback rate (reverts) after applies.
- Increased apply duration (provider/API slowness, large diffs, throttling).
