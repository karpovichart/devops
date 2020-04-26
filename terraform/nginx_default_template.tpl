upstream backend {
	server ${wordpress_server_1_public_ip};
	server ${wordpress_server_2_public_ip};
}

server {
	listen 80;

	location / {
		proxy_pass http://backend;
	}
}
