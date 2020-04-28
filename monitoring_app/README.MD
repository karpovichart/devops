Inside /monitoring_app dir run:

sudo docker build -t monitoring-app .

sudo docker run -d -p 5000:5000 monitoring-app

App runs on http://localhost:5000/