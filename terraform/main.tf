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

output "single_side_mode_key_name_ci_cd_server" {
    value = module.single_side_mode.key_name_ci_cd_server
    sensitive = true
}

output "single_side_mode_key_name_wordpress_server" {
    value = module.single_side_mode.key_name_wordpress_server
    sensitive = true
}

output "single_side_mode_key_name_db_server" {
    value = module.single_side_mode.key_name_db_server
    sensitive = true
}

output "single_side_mode_ci_cd_server_public_ip" {
    value = module.single_side_mode.ci_cd_server_public_ip
}

output "single_side_mode_wordpress_server_public_ip" {
    value = module.single_side_mode.wordpress_server_public_ip
}

#MODULE FOR MULTI SIDE MODE WITH SECOND WP SERVER + LOAD BALANCER

module "multi_side_mode" {
    source = "./multi_side"
}

output "key_name_ci_cd_server" {
    value = module.multi_side_mode.key_name_ci_cd_server
    sensitive = true
}

output "key_name_wordpress_server_1" {
    value = module.multi_side_mode.key_name_wordpress_server_1
    sensitive = true
}

output "key_name_wordpress_server_2" {
    value = module.multi_side_mode.key_name_wordpress_server_2
    sensitive = true
}

output "key_name_db_server" {
    value = module.multi_side_mode.key_name_db_server
    sensitive = true
}

output "key_name_load_balancer_server" {
    value = module.multi_side_mode.key_name_load_balancer_server
    sensitive = true
}

output "ci_cd_server_public_ip" {
    value = module.multi_side_mode.ci_cd_server_public_ip
}
output "wordpress_server_1_public_ip" {
    value = module.multi_side_mode.wordpress_server_1_public_ip
}
output "wordpress_server_2_public_ip" {
    value = module.multi_side_mode.wordpress_server_2_public_ip
}
output "load_balancer_server_public_ip" {
    value = module.multi_side_mode.load_balancer_server_public_ip
}