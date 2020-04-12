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

resource "aws_instance" "wordpress_server"{
    ami           = "ami-0b418580298265d5c"
    instance_type = "t2.micro"
    security_groups = [ aws_security_group.security_group.name ]
    key_name = aws_key_pair.key_pair_wordpress_server.key_name
    tags = {
        Name = "WordPress Server"
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

#EIP for aws_instances
resource "aws_eip" "static_ip_ci_cd_server" {
      instance = aws_instance.ci_cd_server.id
      vpc      = true
}

resource "aws_eip" "static_ip_wordpress_server" {
      instance = aws_instance.wordpress_server.id
      vpc      = true
}

resource "aws_eip" "static_ip_db_server" {
      instance = aws_instance.db_server.id
      vpc      = true
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

#key for wordpress_server
variable "key_name_wordpress_server" {
    type = string
    default = "key_name_wordpress_server"
}

resource "tls_private_key" "key_name_wordpress_server" {
    algorithm = "RSA" 
    rsa_bits = 4096
}
resource "aws_key_pair" "key_pair_wordpress_server" {
    key_name = var.key_name_wordpress_server
    public_key = tls_private_key.key_name_wordpress_server.public_key_openssh
}

output "key_name_wordpress_server" {
  value = tls_private_key.key_name_wordpress_server.private_key_pem
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

#IP addresses for resources
provider "template" {
    version = "~> 2.1"
}

data "template_file" "inventory" {
    template = file("inventory_template.tpl")
    vars = {
        ci_cd_server_public_ip = aws_eip.static_ip_ci_cd_server.public_ip
        wordpress_server_public_ip = aws_eip.static_ip_wordpress_server.public_ip
        db_server_public_ip = aws_eip.static_ip_db_server.public_ip
    }
}

provider "local" {
    version = "~> 1.4"
}

resource "local_file" "save_inventory" {
    content  = data.template_file.inventory.rendered
    filename = "hosts.txt"
}