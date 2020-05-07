from flask import Flask, render_template, request

import boto3

import os

app = Flask(__name__)

region = 'eu-central-1'

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/dashboard',methods = ['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        access_key = request.form.get('access_key')
        secret_key = request.form.get('secret_key')
        session = boto3.Session(
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key,
            region_name = region
        )
        ec2 = session.resource('ec2')
        instances = ec2.instances.all()
        
        logs = open("/opt/share/logs.txt", "r")
        logs_lines = logs.readlines()
        logs.close()
        logs_table = []
        for line in logs_lines:
            logs_table.append(line.split(' '))

    return render_template("dashboard.html", instances = instances, logs_table = logs_table)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')