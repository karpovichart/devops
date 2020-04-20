import os
from os.path import abspath, dirname, join, isfile
import subprocess
from getpass import getpass

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

#check installation and output versions
print('\n Terraform version \n')
subprocess.call("terraform --version", shell=True)
print('\n Ansible version \n')
subprocess.call("ansible --version", shell=True)

#define paths
project_dir = dirname(dirname(dirname(abspath(__file__))))
terraform_dir = join(project_dir, 'terraform')
ansible_dir = join(project_dir, 'ansible')
ansible_keys_dir = join(ansible_dir, 'keys') + '/'

#set terraform workind directory
os.chdir(terraform_dir)

print('\n Welcome to setup script for NetCracker DevOps project \n')

#get keys and export as env vars
access_key = getpass("Enter AWS access key : ") 
secret_key = getpass("Enter AWS secret key : ") 

aws_vars = {
    'AWS_ACCESS_KEY_ID' : access_key ,
    'AWS_SECRET_ACCESS_KEY' : secret_key
}

os.environ.update(aws_vars)

#get password for ansible
os.chdir(ansible_dir)
ansible_password = getpass("Enter password to decrypt keys for Ansible : ")
subprocess.call("echo " + ansible_password + "> " "pass.txt", shell=True)

os.chdir(terraform_dir)

print('Choose option: \n 1 - terraform apply \n 2 - terraform destroy')
select = input('Enter number: ')

if select=='1':
    #run terraform 
    subprocess.run(['terraform', 'init'])
    subprocess.run(['terraform', 'plan'])
    subprocess.run(['terraform', 'apply', '-auto-approve'])

    #make .pem files with keys
    key_1_p1 = subprocess.Popen(['terraform', 'output', 'key_name_ci_cd_server'], stdout=subprocess.PIPE)
    key_1_p2 = subprocess.Popen(["tee", "-a", "key_name_ci_cd_server.pem"], stdin=key_1_p1.stdout, stdout=subprocess.PIPE)
    output1 = key_1_p2.communicate()[0]

    key_2_p1 = subprocess.Popen(['terraform', 'output', 'key_name_db_server'], stdout=subprocess.PIPE)
    key_2_p2 = subprocess.Popen(["tee", "-a", "key_name_db_server.pem"], stdin=key_2_p1.stdout, stdout=subprocess.PIPE)
    output2 = key_2_p2.communicate()[0]

    key_3_1_p1 = subprocess.Popen(['terraform', 'output', 'key_name_wordpress_server_1'], stdout=subprocess.PIPE)
    key_3_1_p2 = subprocess.Popen(["tee", "-a", "key_name_wordpress_server_1.pem"], stdin=key_3_1_p1.stdout, stdout=subprocess.PIPE)
    output3 = key_3_1_p2.communicate()[0]
    
    key_3_2_p1 = subprocess.Popen(['terraform', 'output', 'key_name_wordpress_server_2'], stdout=subprocess.PIPE)
    key_3_2_p2 = subprocess.Popen(["tee", "-a", "key_name_wordpress_server_2.pem"], stdin=key_3_2_p1.stdout, stdout=subprocess.PIPE)
    output3 = key_3_2_p2.communicate()[0]

    key_4_p1 = subprocess.Popen(['terraform', 'output', 'key_name_load_balancer_server'], stdout=subprocess.PIPE)
    key_4_p2 = subprocess.Popen(["tee", "-a", "key_name_load_balancer_server.pem"], stdin=key_4_p1.stdout, stdout=subprocess.PIPE)
    output2 = key_4_p2.communicate()[0]

    ci_cd_server_public_ip = subprocess.run(['terraform','output', 'ci_cd_server_public_ip'], stdout=subprocess.PIPE).stdout.decode('utf-8')

    #setting access rights to keys
    subprocess.call("chmod 400 key_name_ci_cd_server.pem", shell=True)
    subprocess.call("chmod 400 key_name_db_server.pem", shell=True)
    subprocess.call("chmod 400 key_name_wordpress_server_1.pem", shell=True)
    subprocess.call("chmod 400 key_name_wordpress_server_2.pem", shell=True)
    subprocess.call("chmod 400 key_name_load_balancer_server.pem", shell=True)

    #make new directory for keys 'ansible/keys'
    os.chdir(ansible_dir)
    subprocess.call(['mkdir', 'keys'])

    #move keys to new directory
    os.chdir(terraform_dir)
    subprocess.call("mv " + "*.pem " + ansible_keys_dir, shell=True)

    #move file with hosts to ansible directory
    subprocess.call("mv " + "hosts.ini " + ansible_dir, shell=True)

    #move file with nginx load balancer config to ansible directory
    subprocess.call("mv " + "default " + ansible_dir, shell=True)

    os.chdir(ansible_dir)

    print('\n CI/CD server configuration \n')

    subprocess.call("ansible-playbook " + "pb_conf_ci_cd.yml", shell=True)

    subprocess.call("wget " + ci_cd_server_public_ip + ":8080/jenkins/jnlpJars/jenkins-cli.jar", shell=True)
    subprocess.call("java -jar jenkins-cli.jar -s " + ci_cd_server_public_ip + ":8080/jenkins " + "-auth user5:password123 build test1", shell=True)

else:
    subprocess.run(['terraform', 'destroy', '-auto-approve'])