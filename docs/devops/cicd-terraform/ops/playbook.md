# Playbook
 
 ## Routine Operations
 - Onboard a new repo to the standard pipeline.
   - Confirm repo structure and environment model (workspaces/tfvars).
   - Configure backend pathing per environment.
   - Configure required variables and secrets inputs.
   - Enable plan-on-PR and apply-on-merge.
 - Rotate credentials/roles.
   - Validate OIDC/assume-role configuration.
   - Test non-prod apply after rotation.
 - Update Terraform version and providers.
   - Upgrade in staging first.
   - Validate provider lockfile and state migrations.
   - Roll out gradually to production repositories.
 - Manage concurrency and approvals.
   - Ensure protected environments require approvals.
   - Ensure concurrency groups are defined per repo+env.
 
 ## Safety
 - Validate changes in non-prod first.
 - Use canary repositories/modules for high-risk resources.
 - Prefer small PRs (reduce blast radius and speed up review).
 - Require explicit rollback plan for risky changes (state migrations, network/IAM changes).
