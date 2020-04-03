import os
import subprocess

#set workind directory
os.chdir("/home/egor/devops/terraform")

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

#move kyes to new directory
subprocess.call("mkdir /home/egor/devops/ansible/keys/", shell=True)
subprocess.call("mv *.pem /home/egor/devops/ansible/keys/", shell=True)

#move file with hosts to new directory
subprocess.call("mv hosts.txt /home/egor/devops/ansible", shell=True)