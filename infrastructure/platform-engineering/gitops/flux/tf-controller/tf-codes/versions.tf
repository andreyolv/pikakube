# Renovate test fixture.
#
# Every version below is deliberately pinned behind the current release so the
# `terraform` manager has something to propose on the first run. Constraints
# are concrete on purpose: Renovate skips open ranges such as ">= 1.0".
terraform {
  required_version = "1.5.7"

  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "3.5.1"
    }

    null = {
      source  = "hashicorp/null"
      version = "3.2.1"
    }

    local = {
      source  = "hashicorp/local"
      version = "2.4.0"
    }
  }
}
