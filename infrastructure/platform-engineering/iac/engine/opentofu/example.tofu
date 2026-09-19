# Renovate test fixture, and the smallest honest demonstration of the rule this
# folder's README asks for: pinned providers.
#
# The `.tofu` extension is what makes this file OpenTofu as far as Renovate is
# concerned. The HCL is identical to Terraform's — that compatibility is the
# whole point of the fork — so the extension is the only signal the updater
# has, and `.github/renovate.json5` keys the OpenTofu registry off it.
#
# Every version is deliberately pinned behind the current release so the
# `terraform` manager has something to propose. Constraints are concrete on
# purpose: Renovate skips open ranges such as ">= 1.0".
terraform {
  # Resolved against opentofu/opentofu releases, not hashicorp/terraform.
  # Renovate does not infer that from the file extension; the override lives
  # in the repository config.
  required_version = "1.8.0"

  required_providers {
    # Resolved against registry.opentofu.org, not registry.terraform.io.
    random = {
      source  = "hashicorp/random"
      version = "3.5.1"
    }

    null = {
      source  = "hashicorp/null"
      version = "3.2.1"
    }
  }
}

# No provider block, no backend, no cloud credentials: nothing here leaves the
# state file. A backend with locking and state encryption is the first thing to
# settle before this folder provisions anything for real.
resource "random_pet" "this" {
  length = 2
}

resource "null_resource" "this" {
  triggers = {
    name = random_pet.this.id
  }
}

output "name" {
  value = random_pet.this.id
}
