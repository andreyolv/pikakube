# Minimal resources so the configuration is valid on its own: no cloud
# provider, no credentials, nothing created outside the Terraform state.
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
