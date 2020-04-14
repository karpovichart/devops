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

print('\n Welcome to setup script for NetCracker DevOps project \n')

#get keys and export as env vars
access_key = getpass("Enter AWS access key : ") 
secret_key = getpass("Enter AWS secret key : ") 

aws_vars = {
    'AWS_ACCESS_KEY_ID' : access_key ,
    'AWS_SECRET_ACCESS_KEY' : secret_key
}

os.environ.update(aws_vars)

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
    subprocess.call("mv " + "hosts.txt " + ansible_dir, shell=True)

    #move file with nginx load balancer config to ansible directory
    subprocess.call("mv " + "default " + ansible_dir, shell=True)
else:
    subprocess.run(['terraform', 'destroy', '-auto-approve'])