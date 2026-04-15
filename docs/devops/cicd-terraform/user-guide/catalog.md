# Catalog

## What exists
- Standard reusable GitHub Actions workflows for Terraform.
- Backend and tagging conventions.
- Concurrency and approval conventions per environment.
- Plan artifact integrity pattern (PR -> merge).

## How to consume
- Adopt the standard repo structure.
- Configure backend paths and roles.
- Enable plan artifact integrity.
- Configure environment inputs (workspace/tfvars) consistently.
- Validate with a non-prod PoC before enabling production applies.
