# FAQ
 
 ## Why not copy workflows into each repo?
 Copying leads to drift and high maintenance cost. Centralization enables consistent governance.
 
 ## How do I avoid breaking changes?
 Pin versions and upgrade intentionally after reviewing release notes.
 
 ## Why pin to tags/SHA instead of a branch?
 Branches are mutable and can change without notice. Pinning makes upgrades explicit and rollback possible.
 
 ## Can teams customize workflows?
 Yes, via inputs and by composing reusable workflows with repository-specific steps.
 
 ## Who owns incidents caused by a workflow release?
 The workflow repo owners own the release quality, and consumer repo owners own when they upgrade.
