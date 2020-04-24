{*[ci_cd_server]*}
{*ci_cd_server_host ansible_host=${ci_cd_server_public_ip} ansible_user=ubuntu ansible_ssh_private_key_file=keys/key_name_ci_cd_server.pem*}

{*[wordpress_server_1]*}
{*wordpress_server_host_1 ansible_host=${wordpress_server_1_public_ip} ansible_user=ubuntu ansible_ssh_private_key_file=keys/key_name_wordpress_server_1.pem*}
{*[wordpress_server_2]*}
{*wordpress_server_host_2 ansible_host=${wordpress_server_2_public_ip} ansible_user=ubuntu ansible_ssh_private_key_file=keys/key_name_wordpress_server_2.pem*}

{*[db_server]*}
{*db_server_host ansible_host=${db_server_public_ip} ansible_user=ubuntu ansible_ssh_private_key_file=keys/key_name_db_server.pem*}

{*[load_balancer_server]*}
{*load_balancer_server_host ansible_host=${load_balancer_server_public_ip} ansible_user=ubuntu ansible_ssh_private_key_file=keys/key_name_load_balancer_server.pem*}
[ci_cd_server]
${ci_cd_server_public_ip}
[load_balancer_server]
${load_balancer_server_public_ip}
[wordpress_server_1]
${wordpress_server_1_public_ip}
[wordpress_server_2]
${wordpress_server_2_public_ip}
[db_server]
${db_server_public_ip}