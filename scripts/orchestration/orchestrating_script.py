import os
from os.path import abspath, dirname, join, isfile
import subprocess
from getpass import getpass

#define paths
project_dir = dirname(dirname(dirname(abspath(__file__))))
terraform_dir = join(project_dir, 'terraform')
ansible_dir = join(project_dir, 'ansible')
ansible_keys_dir = join(ansible_dir, 'keys') + '/'

#set terraform workind directory
os.chdir(terraform_dir)

print('Welcome to setup script for NetCracker DevOps project')

if isfile('terraform.tfvars'):
    pass
else:
    #create terraform file with vars (AWS credentials)
    subprocess.call("touch terraform.tfvars", shell=True)

    #get keys and write them to terraform.tfvars file
    access_key = getpass("Enter access key : ") 
    secret_key = getpass("Enter secret key : ") 
    f = open("terraform.tfvars", "a")
    f.write('AWS_ACCESS_KEY = "{}" \n'.format(access_key))
    f.write('AWS_SECRET_KEY = "{}"'.format(secret_key))
    f.close()

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

    key_3_p1 = subprocess.Popen(['terraform', 'output', 'key_name_wordpress_server'], stdout=subprocess.PIPE)
    key_3_p2 = subprocess.Popen(["tee", "-a", "key_name_wordpress_server.pem"], stdin=key_3_p1.stdout, stdout=subprocess.PIPE)
    output3 = key_3_p2.communicate()[0]

    #setting access rights to keys
    subprocess.call("chmod 400 key_name_ci_cd_server.pem", shell=True)
    subprocess.call("chmod 400 key_name_db_server.pem", shell=True)
    subprocess.call("chmod 400 key_name_wordpress_server.pem", shell=True)

    #make new directory for keys 'ansible/keys'
    os.chdir(ansible_dir)
    subprocess.call(['mkdir', 'keys'])

    #move keys to new directory
    os.chdir(terraform_dir)
    subprocess.call("mv " + "*.pem " + ansible_keys_dir, shell=True)

    #move file with hosts to ansible directory
    subprocess.call("mv " + "hosts.txt " + ansible_dir, shell=True)
else:
    subprocess.run(['terraform', 'destroy', '-auto-approve'])