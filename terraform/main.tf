#variables
#defined in terraform.tfvars
variable "AWS_ACCESS_KEY" {
  
}

variable "AWS_SECRET_KEY" {
  
}

#provider
provider "aws" {
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
    region = "eu-central-1"
    version = "~> 2.54"
}

#MODULE FOR SINGLE SIDE MODE WITH ONE WP SERVER 

module "single_side_mode" {
    source = "./single_side"
}

#MODULE FOR MULTI SIDE MODE WITH SECOND WP SERVER + LOAD BALANCER

module "multi_side_mode" {
    source = "./multi_side"
}