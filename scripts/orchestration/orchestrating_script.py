import os
from os.path import abspath, dirname, join, isfile
import subprocess
from getpass import getpass
import requests
import secrets
from requests.auth import HTTPBasicAuth
import time

#check installation and output versions
print('\n Terraform version: \n')
subprocess.call("terraform --version", shell=True)
print('\n Ansible version: \n')
subprocess.call("ansible --version", shell=True)

#define paths
user_dir = dirname(dirname(dirname(dirname(abspath(__file__)))))
project_dir = dirname(dirname(dirname(abspath(__file__))))
terraform_dir = join(project_dir, 'terraform')
ansible_dir = join(project_dir, 'ansible')
ansible_keys_dir = join(ansible_dir, 'keys') + '/'

#set user working directory
os.chdir(user_dir)

#move cred file to terraform dir
subprocess.call("mv terraform.tfvars " + terraform_dir, shell=True)

print('\n Welcome to setup script for NetCracker DevOps project \n')

print('Choose option: \n 1 - Create infrastructure and configure servers \n 2 - Destroy existing infrastructure')
select_action = input('Enter number: ')

if select_action=='1':

    #get password for ansible
    os.chdir(ansible_dir)
    ansible_password = getpass("Enter password to decrypt keys for Ansible : ")
    subprocess.call("echo " + ansible_password + "> " "pass.txt", shell=True)

    print('Choose mode: \n 1 - Single side (one Wordpress server) \n 2 - Multi side(two Wordpress servers with load balancer)')
    select_mode = input('Enter number: ')

    f = open('side_mode.txt','w')
    f.write(select_mode)
    f.close()

    if select_mode=='1':
         #set terraform working directory
        os.chdir(terraform_dir)

        #run terraform 
        subprocess.run(['terraform', 'init'])
        subprocess.run(['terraform', 'plan', '-target=module.single_side_mode'])
        subprocess.run(['terraform', 'apply', '-target=module.single_side_mode', '-auto-approve'])

        #make .pem files with keys
        key_1_p1 = subprocess.Popen(['terraform', 'output', 'single_side_mode_key_name_ci_cd_server'], stdout=subprocess.PIPE)
        key_1_p2 = subprocess.Popen(["tee", "-a", "key_name_ci_cd_server.pem"], stdin=key_1_p1.stdout, stdout=subprocess.PIPE)
        output1 = key_1_p2.communicate()[0]

        key_2_p1 = subprocess.Popen(['terraform', 'output', 'single_side_mode_key_name_db_server'], stdout=subprocess.PIPE)
        key_2_p2 = subprocess.Popen(["tee", "-a", "key_name_db_server.pem"], stdin=key_2_p1.stdout, stdout=subprocess.PIPE)
        output2 = key_2_p2.communicate()[0]

        key_3_p1 = subprocess.Popen(['terraform', 'output', 'single_side_mode_key_name_wordpress_server'], stdout=subprocess.PIPE)
        key_3_p2 = subprocess.Popen(["tee", "-a", "key_name_wordpress_server_1.pem"], stdin=key_3_p1.stdout, stdout=subprocess.PIPE)
        output3 = key_3_p2.communicate()[0]

        #output IPs
        ci_cd_server_public_ip = subprocess.run(['terraform','output', 'single_side_mode_ci_cd_server_public_ip'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
        wordpress_server_public_ip = subprocess.run(['terraform','output', 'single_side_mode_wordpress_server_public_ip'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()

        #setting access rights to keys
        subprocess.call("chmod 400 key_name_ci_cd_server.pem", shell=True)
        subprocess.call("chmod 400 key_name_db_server.pem", shell=True)
        subprocess.call("chmod 400 key_name_wordpress_server_1.pem", shell=True)

        #make new directory for keys 'ansible/keys'
        os.chdir(ansible_dir)
        subprocess.call(['mkdir', 'keys'])

        #move keys to new directory
        os.chdir(terraform_dir)
        subprocess.call("mv " + "*.pem " + ansible_keys_dir, shell=True)

        #move file with hosts to ansible directory
        subprocess.call("mv " + "hosts.ini " + ansible_dir, shell=True)

        os.chdir(ansible_dir)

        #create token for pipeline
        token = secrets.token_urlsafe(20)

        f = open('pipeline_token.txt','w')
        f.write(token)
        f.close()
        
        time.sleep(20)

        print('\n Start CI/CD server configuration \n')

        subprocess.call("ansible-playbook " + "pb_conf_ci_cd.yml -i hosts.ini --vault-password-file pass.txt", shell=True)

        time.sleep(20)

        main_build_url = 'http://' + ci_cd_server_public_ip + ':8080/jenkins/job/main/build?token=' + token
       # main_build = requests.get(main_build_url, auth=HTTPBasicAuth('user', 'password1'))
        main_build = requests.get(main_build_url, auth=HTTPBasicAuth('admin', 'qwerty'))

        if main_build.status_code == 201:
            print('\n Start pipeline build for application servers \n')
        else:
            print(main_build.text)

        time.sleep(10)

        open("file1", "w").close()

        while True:
            main_status_url = 'http://' + ci_cd_server_public_ip + ':8080/jenkins/job/main/1/consoleText?token=' + token
           # main_status = requests.get(main_status_url, auth=HTTPBasicAuth('user', 'password1'))
            main_status = requests.get(main_status_url, auth=HTTPBasicAuth('admin', 'qwerty'))

            f2 = open("file2","w")
            f2.write(main_status.text)
            f2.close()

            f1_read = open("file1","r")
            f1_read_text = f1_read.readlines()
            f1_read.close()

            f2_read = open("file2","r")
            f2_read_text = f2_read.readlines()
            f2_read.close()

            start = len(f1_read_text)
            new = f2_read_text[start:]
            
            if ''.join(new):
                print(''.join(new))

            f1_write = open("file1","w")
            f1_write.write(main_status.text)
            f1_write.close()

            if 'Finished: SUCCESS' in main_status.text:
                file = open("file1","r+")
                file.truncate(0)
                file.close()
                file = open("file2","r+")
                file.truncate(0)
                file.close()
                break
            elif 'Finished: FAILURE' in main_status.text:
                print('\n Something went wrong \n')
                file = open("file1","r+")
                file.truncate(0)
                file.close()
                file = open("file2","r+")
                file.truncate(0)
                file.close()
                break

        time.sleep(10)

        monitoring_build_url = 'http://' + ci_cd_server_public_ip + ':8080/jenkins/job/monitoring/build?token=' + token
       # monitoring_build = requests.get(monitoring_build_url, auth=HTTPBasicAuth('user', 'password1'))
        monitoring_build = requests.get(monitoring_build_url, auth=HTTPBasicAuth('admin', 'qwerty'))

        if monitoring_build.status_code == 201:
            print('\n Start pipeline build for monitoring app \n')
        else:
            print(monitoring_build.text)

        time.sleep(15)

        while True:
            monitoring_status_url = 'http://' + ci_cd_server_public_ip + ':8080/jenkins/job/monitoring/1/consoleText?token=' + token
           # monitoring_status = requests.get(monitoring_status_url, auth=HTTPBasicAuth('user', 'password1'))
            monitoring_status = requests.get(monitoring_status_url, auth=HTTPBasicAuth('admin', 'qwerty'))

            f2 = open("file2","w")
            f2.write(monitoring_status.text)
            f2.close()

            f1_read = open("file1","r")
            f1_read_text = f1_read.readlines()
            f1_read.close()

            f2_read = open("file2","r")
            f2_read_text = f2_read.readlines()
            f2_read.close()

            start = len(f1_read_text)
            new = f2_read_text[start:]
            
            if ''.join(new):
                print(''.join(new))

            f1_write = open("file1","w")
            f1_write.write(monitoring_status.text)
            f1_write.close()

            if 'Finished: SUCCESS' in monitoring_status.text:
                print('\n Infrastructure has been successfully deployed \n')
                print('\n Jenkins CI/CD server: ', ci_cd_server_public_ip + ':8080/jenkins')
                print('\n WordPress server: ', wordpress_server_public_ip)
                print('\n Monitoring App: ', ci_cd_server_public_ip + ':5000')
                break
            elif 'Finished: FAILURE' in monitoring_status.text:
                print('\n Something went wrong \n')
                break
        
    else:
        #set terraform working directory
        os.chdir(terraform_dir)

        #run terraform 
        subprocess.run(['terraform', 'init'])
        subprocess.run(['terraform', 'plan', '-target=module.multi_side_mode'])
        subprocess.run(['terraform', 'apply', '-target=module.multi_side_mode', '-auto-approve'])

        #make .pem files with keys
        key_1_p1 = subprocess.Popen(['terraform', 'output', 'key_name_ci_cd_server'], stdout=subprocess.PIPE)
        key_1_p2 = subprocess.Popen(["tee", "-a", "key_name_ci_cd_server.pem"], stdin=key_1_p1.stdout, stdout=subprocess.PIPE)
        output1 = key_1_p2.communicate()[0]

        key_2_p1 = subprocess.Popen(['terraform', 'output', 'key_name_db_server'], stdout=subprocess.PIPE)
        key_2_p2 = subprocess.Popen(["tee", "-a", "key_name_db_server.pem"], stdin=key_2_p1.stdout, stdout=subprocess.PIPE)
        output2 = key_2_p2.communicate()[0]

        key_3_1_p1 = subprocess.Popen(['terraform', 'output', 'key_name_wordpress_server_1'], stdout=subprocess.PIPE)
        key_3_1_p2 = subprocess.Popen(["tee", "-a", "key_name_wordpress_server_1.pem"], stdin=key_3_1_p1.stdout, stdout=subprocess.PIPE)
        output3_1 = key_3_1_p2.communicate()[0]
        
        key_3_2_p1 = subprocess.Popen(['terraform', 'output', 'key_name_wordpress_server_2'], stdout=subprocess.PIPE)
        key_3_2_p2 = subprocess.Popen(["tee", "-a", "key_name_wordpress_server_2.pem"], stdin=key_3_2_p1.stdout, stdout=subprocess.PIPE)
        output3_2 = key_3_2_p2.communicate()[0]

        key_4_p1 = subprocess.Popen(['terraform', 'output', 'key_name_load_balancer_server'], stdout=subprocess.PIPE)
        key_4_p2 = subprocess.Popen(["tee", "-a", "key_name_load_balancer_server.pem"], stdin=key_4_p1.stdout, stdout=subprocess.PIPE)
        output4 = key_4_p2.communicate()[0]

        ci_cd_server_public_ip = subprocess.run(['terraform','output', 'ci_cd_server_public_ip'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
        wordpress_server_1_public_ip = subprocess.run(['terraform','output', 'wordpress_server_1_public_ip'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
        wordpress_server_2_public_ip = subprocess.run(['terraform','output', 'wordpress_server_2_public_ip'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
        load_balancer_server_public_ip = subprocess.run(['terraform','output', 'load_balancer_server_public_ip'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()

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

        token = secrets.token_urlsafe(20)

        f = open('pipeline_token.txt','w')
        f.write(token)
        f.close()
        
        time.sleep(20)

        print('\n Start CI/CD server configuration \n')

        subprocess.call("ansible-playbook " + "pb_conf_ci_cd.yml -i hosts.ini --vault-password-file pass.txt", shell=True)

        time.sleep(20)

        main_build_url = 'http://' + ci_cd_server_public_ip + ':8080/jenkins/job/main/build?token=' + token
        #main_build = requests.get(main_build_url, auth=HTTPBasicAuth('user', 'password1'))
        main_build = requests.get(main_build_url, auth=HTTPBasicAuth('admin', 'qwerty'))

        if main_build.status_code == 201:
            print('\n Start pipeline build for application servers \n')
        else:
            print(main_build.text)

        time.sleep(10)

        open("file1", "w").close()

        while True:
            main_status_url = 'http://' + ci_cd_server_public_ip + ':8080/jenkins/job/main/1/consoleText?token=' + token
           # main_status = requests.get(main_status_url, auth=HTTPBasicAuth('user', 'password1'))
            main_status = requests.get(main_status_url, auth=HTTPBasicAuth('admin', 'qwerty'))

            f2 = open("file2","w")
            f2.write(main_status.text)
            f2.close()

            f1_read = open("file1","r")
            f1_read_text = f1_read.readlines()
            f1_read.close()

            f2_read = open("file2","r")
            f2_read_text = f2_read.readlines()
            f2_read.close()

            start = len(f1_read_text)
            new = f2_read_text[start:]
            
            if ''.join(new):
                print(''.join(new))

            f1_write = open("file1","w")
            f1_write.write(main_status.text)
            f1_write.close()

            if 'Finished: SUCCESS' in main_status.text:
                file = open("file1","r+")
                file.truncate(0)
                file.close()
                file = open("file2","r+")
                file.truncate(0)
                file.close()
                break
            elif 'Finished: FAILURE' in main_status.text:
                print('\n Something went wrong \n')
                file = open("file1","r+")
                file.truncate(0)
                file.close()
                file = open("file2","r+")
                file.truncate(0)
                file.close()
                break

        time.sleep(10)

        monitoring_build_url = 'http://' + ci_cd_server_public_ip + ':8080/jenkins/job/monitoring/build?token=' + token
       # monitoring_build = requests.get(monitoring_build_url, auth=HTTPBasicAuth('user', 'password1'))
        monitoring_build = requests.get(monitoring_build_url, auth=HTTPBasicAuth('admin', 'qwerty'))

        if monitoring_build.status_code == 201:
            print('\n Start pipeline build for monitoring app \n')
        else:
            print(monitoring_build.text)

        time.sleep(15)

        while True:
            monitoring_status_url = 'http://' + ci_cd_server_public_ip + ':8080/jenkins/job/monitoring/1/consoleText?token=' + token
        #   monitoring_status = requests.get(monitoring_status_url, auth=HTTPBasicAuth('user', 'password1'))
            monitoring_status = requests.get(monitoring_status_url, auth=HTTPBasicAuth('admin', 'qwerty'))

            f2 = open("file2","w")
            f2.write(monitoring_status.text)
            f2.close()

            f1_read = open("file1","r")
            f1_read_text = f1_read.readlines()
            f1_read.close()

            f2_read = open("file2","r")
            f2_read_text = f2_read.readlines()
            f2_read.close()

            start = len(f1_read_text)
            new = f2_read_text[start:]
            
            if ''.join(new):
                print(''.join(new))

            f1_write = open("file1","w")
            f1_write.write(monitoring_status.text)
            f1_write.close()

            if 'Finished: SUCCESS' in monitoring_status.text:
                print('\n Infrastructure has been successfully deployed \n')
                print('\n Jenkins CI/CD server: ', ci_cd_server_public_ip + ':8080/jenkins')
                print('\n WordPress 1 server: ', wordpress_server_1_public_ip)
                print('\n WordPress 2 server: ', wordpress_server_2_public_ip)
                print('\n Load Balancer server: ', load_balancer_server_public_ip)
                print('\n Monitoring App: ', ci_cd_server_public_ip + ':5000')
                break
            elif 'Finished: FAILURE' in monitoring_status.text:
                print('\n Something went wrong \n')
                break
else:
    os.chdir(terraform_dir)
    subprocess.run(['terraform', 'destroy', '-auto-approve'])
    print('\n Infrastructure has been destroyed \n')