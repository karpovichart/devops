upstream web_backend {
	server ${wordpress_server_1_public_ip};
	server ${wordpress_server_2_public_ip};
}

server {
	listen 80;

	location / {
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_pass http://web_backend;
	}
}
