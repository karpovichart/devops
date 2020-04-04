import os
from os.path import abspath, dirname, join
import subprocess

#define paths
project_dir = dirname(dirname(dirname(abspath(__file__))))
terraform_dir = join(project_dir, 'terraform')
ansible_dir = join(project_dir, 'ansible')
ansible_keys_dir = join(ansible_dir, 'keys') + '/'

#set terraform workind directory
os.chdir(terraform_dir)

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

#make new directory for keys 'ansible/keys'
os.chdir(ansible_dir)
subprocess.call(['mkdir', 'keys'])

#move keys to new directory
os.chdir(terraform_dir)
subprocess.call("mv " + "*.pem " + ansible_keys_dir, shell=True)

#move file with hosts to ansible directory
subprocess.call("mv " + "hosts.txt " + ansible_dir, shell=True)