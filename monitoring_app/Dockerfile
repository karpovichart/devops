FROM ubuntu:16.04
RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000:5000
CMD python3 app/app.py