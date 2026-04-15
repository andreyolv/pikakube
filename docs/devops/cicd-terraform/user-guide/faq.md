# FAQ
 
 ## Why keep the plan artifact from PR to merge?
 It ensures the exact reviewed plan is what gets applied, preventing divergence.
 
 ## What if the plan becomes stale before merge?
 Re-run the plan on the updated PR, review the new diff, and only then merge. The merge apply must use the latest reviewed artifact.
 
 ## How do we prevent concurrent applies?
 Use workflow concurrency groups and backend state locking.
 
 ## Can we allow local applies?
 Only as break-glass. Local applies should require explicit approval and a way to attach logs/output to the change record.
 
 ## What if state is locked?
 Investigate who holds the lock and follow the runbook for safe unlock.
 
 ## How do we roll back a bad apply?
 Revert the Git change and let the pipeline apply the revert. Avoid manual state manipulation unless absolutely necessary.
