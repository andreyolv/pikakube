# Playbook
 
 ## Routine Operations
 - Release new workflow versions.
   - validate changes in a canary consumer repo
   - publish tag and release notes
 - Communicate breaking changes and upgrade notes.
   - document required input/secret changes
   - include rollback instructions
 - Review consumer adoption and support migrations.
   - track version distribution
   - prioritize upgrades for repos with high incident rates
 
 ## Safety
 - Use canary consumers for new versions.
 - Require pinned versions for all consumers.
 - Avoid changing defaults in a way that can silently break consumers.
