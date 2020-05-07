# NetCracker Technology Education Center Spring 2020
## Field of study: DevOps 
## Project members: 
* https://github.com/karpovichart
* https://github.com/xbxjsnsb 
* https://github.com/blackberry22
## Overview 
This project allows you to automatically create the infrastructure for a web application using the example of CMS WordPress. The main features of the project include the use of a CI/CD server to configure all application servers, the creation of a separate application for monitoring servers, the use of an external database and load balancer for the application.
## Used tools:
* Terraform
* Ansible
* Jenkins
* Docker 
* AWS
* Python
* WordPress (Apache WebServer, MySQL Database, NGINX as load balancer)
## Preinstall
Before running the application, you must install:
* Terraform
* Ansible
* Python 3.6

This can be done manually or use the following Python script:
```python
import subprocess

#clone repository
subprocess.call("git clone https://github.com/karpovichart/devops.git", shell=True)

#install terraform
subprocess.call("wget https://releases.hashicorp.com/terraform/0.12.24/terraform_0.12.24_linux_amd64.zip", shell=True)
subprocess.call("sudo apt install unzip", shell=True)
subprocess.call("unzip terraform_0.12.24_linux_amd64.zip", shell=True)
subprocess.call("rm terraform_0.12.24_linux_amd64.zip", shell=True)
subprocess.call("sudo mv terraform /bin/", shell=True)

#install ansible
subprocess.call("sudo apt-add-repository ppa:ansible/ansible -y", shell=True)
subprocess.call("sudo apt-get update", shell=True)
subprocess.call("sudo apt-get install ansible -y", shell=True)

subprocess.call("python3 devops/scripts/orchestration/orchestrating_script.py", shell=True)
```
You must also have an AWS account with the user created in the IAM section. As a result, you need to create a terraform.tfvars file with the following contents:
```terraform
AWS_ACCESS_KEY = "xxxxxx"
AWS_SECRET_KEY = "xxxxxx"
```
## Deployment
Assumed that two files were created as described above:
* init.py (you can name it whatever you want)
* terraform.tfvars

Run script:
```bash
python3 init.py
```
Next, you need to enter values depending on the required tasks:
1. Choose deploy or destroy existing infrastructure
2. Enter ansible password
3. Choose mode (single side- one WordPress server, multi side - two WordPress servers with load balancer)

As a result, the script will output ip addresses for each server:
```bash
Infrastructure has been successfully deployed
Jenkins CI/CD server: x.x.x.x:8080/jenkins
WordPress 1 server: x.x.x.x
Load Balancer server: x.x.x.x
Monitoring App: x.x.x.x:5000
```
