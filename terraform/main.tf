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

#resources
resource "aws_instance" "ci_cd_server"{
    ami           = "ami-0b418580298265d5c"
    instance_type = "t2.micro"
    security_groups = [ aws_security_group.security_group.name ]
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
    tags = {
        Name = "WordPress Server"
    }
}

resource "aws_instance" "db_server"{
    ami           = "ami-0b418580298265d5c"
    instance_type = "t2.micro"
    security_groups = [ aws_security_group.security_group.name ]
    tags = {
        Name = "MySQL Server"
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
