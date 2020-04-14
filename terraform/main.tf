#provider
provider "aws" {
    region = "eu-central-1"
    version = "~> 2.54"
}

#resources
resource "aws_instance" "ci_cd_server"{
    ami           = "ami-0b418580298265d5c"
    instance_type = "t2.micro"
    security_groups = [ aws_security_group.security_group.name ]
    key_name = aws_key_pair.key_pair_ci_cd_server.key_name
	  user_data = <<EOF
#!/bin/bash
sudo apt update
sudo apt install openjdk-8-jdk openjdk-8-jre -y
EOF
    tags = {
        Name = "Jenkins Server"
    }
}

resource "aws_instance" "wordpress_server_1"{
    ami           = "ami-0b418580298265d5c"
    instance_type = "t2.micro"
    security_groups = [ aws_security_group.security_group.name ]
    key_name = aws_key_pair.key_pair_wordpress_server_1.key_name
    tags = {
        Name = "WordPress Server 1"
    }
}

resource "aws_instance" "wordpress_server_2"{
    ami           = "ami-0b418580298265d5c"
    instance_type = "t2.micro"
    security_groups = [ aws_security_group.security_group.name ]
    key_name = aws_key_pair.key_pair_wordpress_server_2.key_name
    tags = {
        Name = "WordPress Server 2"
    }
}

resource "aws_instance" "db_server"{
    ami           = "ami-0b418580298265d5c"
    instance_type = "t2.micro"
    security_groups = [ aws_security_group.security_group.name ]
    key_name = aws_key_pair.key_pair_db_server.key_name
    tags = {
        Name = "MySQL Server"
    }
}

resource "aws_instance" "load_balancer_server"{
    ami           = "ami-0b418580298265d5c"
    instance_type = "t2.micro"
    security_groups = [ aws_security_group.security_group.name ]
    key_name = aws_key_pair.key_pair_db_server.key_name
    tags = {
        Name = "Load Balancer Server"
    }
}

#EIP for aws_instances
resource "aws_eip" "static_ip_ci_cd_server" {
      instance = aws_instance.ci_cd_server.id
      vpc      = true
      tags = {
                Name = "Jenkins Server EIP"
            }
}

resource "aws_eip" "static_ip_wordpress_server_1" {
      instance = aws_instance.wordpress_server_1.id
      vpc      = true
      tags = {
                Name = "WordPress Server 1 EIP"
            }
}

resource "aws_eip" "static_ip_wordpress_server_2" {
      instance = aws_instance.wordpress_server_2.id
      vpc      = true
      tags = {
                Name = "WordPress Server 2 EIP"
            }
}

resource "aws_eip" "static_ip_db_server" {
      instance = aws_instance.db_server.id
      vpc      = true
      tags = {
                Name = "MySQL Server EIP"
            }
}

resource "aws_eip" "static_ip_load_balancer_server" {
      instance = aws_instance.load_balancer_server.id
      vpc      = true
      tags = {
                Name = "Load Balancer EIP"
            }
}

#security groups
resource "aws_security_group" "security_group" {
  name        = "DevOps project security_group"
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "DevOps project security_group"
  }
}

#SSH key-pair
provider tls {
  version = "~> 2.1"
}

#key for ci_cd_server
variable "key_name_ci_cd_server" {
    type = string
    default = "key_name_ci_cd_server"
}

resource "tls_private_key" "key_name_ci_cd_server" {
    algorithm = "RSA" 
    rsa_bits = 4096
}
resource "aws_key_pair" "key_pair_ci_cd_server" {
    key_name = var.key_name_ci_cd_server
    public_key = tls_private_key.key_name_ci_cd_server.public_key_openssh
}

output "key_name_ci_cd_server" {
  value = tls_private_key.key_name_ci_cd_server.private_key_pem
  sensitive = true
}

#key for wordpress_server 1
variable "key_name_wordpress_server_1" {
    type = string
    default = "key_name_wordpress_server_1"
}

resource "tls_private_key" "key_name_wordpress_server_1" {
    algorithm = "RSA" 
    rsa_bits = 4096
}
resource "aws_key_pair" "key_pair_wordpress_server_1" {
    key_name = var.key_name_wordpress_server_1
    public_key = tls_private_key.key_name_wordpress_server_1.public_key_openssh
}

output "key_name_wordpress_server_1" {
  value = tls_private_key.key_name_wordpress_server_1.private_key_pem
  sensitive = true
}

#key for wordpress_server 2
variable "key_name_wordpress_server_2" {
    type = string
    default = "key_name_wordpress_server_2"
}

resource "tls_private_key" "key_name_wordpress_server_2" {
    algorithm = "RSA" 
    rsa_bits = 4096
}
resource "aws_key_pair" "key_pair_wordpress_server_2" {
    key_name = var.key_name_wordpress_server_2
    public_key = tls_private_key.key_name_wordpress_server_2.public_key_openssh
}

output "key_name_wordpress_server_2" {
  value = tls_private_key.key_name_wordpress_server_2.private_key_pem
  sensitive = true
}

#key for db_server
variable "key_name_db_server" {
    type = string
    default = "key_name_db_server"
}

resource "tls_private_key" "key_name_db_server" {
    algorithm = "RSA" 
    rsa_bits = 4096
}
resource "aws_key_pair" "key_pair_db_server" {
    key_name = var.key_name_db_server
    public_key = tls_private_key.key_name_db_server.public_key_openssh
}

output "key_name_db_server" {
  value = tls_private_key.key_name_db_server.private_key_pem
  sensitive = true
}

#key for load_balancer_server
variable "key_name_load_balancer_server" {
    type = string
    default = "key_name_load_balancer_server"
}

resource "tls_private_key" "key_name_load_balancer_server" {
    algorithm = "RSA" 
    rsa_bits = 4096
}
resource "aws_key_pair" "key_pair_load_balancer_server" {
    key_name = var.key_name_load_balancer_server
    public_key = tls_private_key.key_name_load_balancer_server.public_key_openssh
}

output "key_name_load_balancer_server" {
  value = tls_private_key.key_name_load_balancer_server.private_key_pem
  sensitive = true
}

#IP addresses for resources
provider "template" {
    version = "~> 2.1"
}

data "template_file" "inventory" {
    template = file("inventory_template.tpl")
    vars = {
        ci_cd_server_public_ip = aws_eip.static_ip_ci_cd_server.public_ip
        wordpress_server_1_public_ip = aws_eip.static_ip_wordpress_server_1.public_ip
        wordpress_server_2_public_ip = aws_eip.static_ip_wordpress_server_2.public_ip
        db_server_public_ip = aws_eip.static_ip_db_server.public_ip
        load_balancer_server_public_ip = aws_eip.static_ip_load_balancer_server.public_ip
    }
}

provider "local" {
    version = "~> 1.4"
}

resource "local_file" "save_inventory" {
    content  = data.template_file.inventory.rendered
    filename = "hosts.txt"
}

#Config for NGINX load balancer
data "template_file" "nginx_default" {
    template = file("nginx_default_template.tpl")
    vars = {
        wordpress_server_1_public_ip = aws_eip.static_ip_wordpress_server_1.public_ip
        wordpress_server_2_public_ip = aws_eip.static_ip_wordpress_server_2.public_ip
    }
}

resource "local_file" "save_nginx_default" {
    content  = data.template_file.nginx_default.rendered
    filename = "default"
}