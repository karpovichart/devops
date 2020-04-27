from flask import Flask, render_template, request

import boto3

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
    return render_template("dashboard.html", instances = instances)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')