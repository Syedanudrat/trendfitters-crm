terraform {
  backend "s3" {
    bucket       = "trendfitters-crm-terraform-state-781485980116"
    key          = "trendfitters-crm/dev/terraform.tfstate"
    region       = "ap-south-1"
    use_lockfile = true
    encrypt      = true
  }
}