from flask import Flask, render_template, request, url_for, send_from_directory, jsonify, redirect
import datetime
import time
from IPy import IP
from database.db import initialize_db
from api import *
from database.models import Data, App, Domain

with open('config.json', 'r') as fp:
    creds = json.load(fp)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if int(App.objects().count()) == 0:
        App(name=creds['name'], site=creds['site'], key=creds['key'], email=creds['mail'], user=creds['user']).save()
    return render_template('main.html')


import re


@app.route('/search', methods=['GET', 'POST'])
def get_ip():
    if str(request.form['ip']).replace('.', '').isdigit():
        response = ip_address(request.form['ip'])
        if 'continent' not in response['data']['attributes']:
            continent = "None"
        else:
            continent = response['data']['attributes']['continent']
        if 'country' not in response['data']['attributes']:
            country = "None"
        else:
            country = response['data']['attributes']['country']
        if 'regional_internet_registry' not in response['data']['attributes']:
            registry = "None"
        else:
            registry = response['data']['attributes']['regional_internet_registry']
        if 'last_analysis_stats' not in response['data']['attributes']:
            stats = {"harmless": 0, "malicious": 0, "suspicious": 0, "timeout": 0, "undetected": 0}
        else:
            stats = response['data']['attributes']['last_analysis_stats']
        results = {}
        for k, v in response['data']['attributes']['last_analysis_results'].items():
            if '.' in k:
                k = k.replace('.', '-')
            results.update({k: v['result']})
        Data(ip=request.form['ip'],
             continent=continent,
             country=country,
             exec_date=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
             last_analysis_results=results,
             last_analysis_stats=stats,
             regional_internet_registry=registry,
             whois=response['data']['attributes']['whois']
             ).save()

        data = Data.objects(ip=request.form['ip']).order_by('-id').first()
        return render_template('showIP.html', result=data)

    else:
        response = domain(request.form['ip'])
        results = {}
        categories = {}
        for k, v in response['data']['attributes']['categories'].items():
            if '.' in k:
                k = k.replace('.', '-')
            categories.update({k: v})
        for k, v in response['data']['attributes']['last_analysis_results'].items():
            if '.' in k:
                k = k.replace('.', '-')
            results.update({k: v['result']})
        if 'last_analysis_stats' not in response['data']['attributes']:
            stats = {"harmless": 0, "malicious": 0, "suspicious": 0, "timeout": 0, "undetected": 0}
        else:
            stats = response['data']['attributes']['last_analysis_stats']
        Domain(domain=request.form['ip'],
               exec_date=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
               categories=categories,
               last_analysis_results=results,
               last_analysis_stats=stats,
               registrar=response['data']['attributes']['registrar'],
               whois=response['data']['attributes']['whois']
               ).save()
        data = Domain.objects(domain=request.form['ip']).order_by('-id').first()
        return render_template('showDomain.html', result=data)


@app.route('/details/<ip>', methods=['GET', 'POST'])
def show_details(ip):
    data = Data.objects(ip=ip)[0]
    return render_template('showIP.html', result=data)


@app.route('/domain_details/<domain>', methods=['GET', 'POST'])
def show_domain_details(domain):
    data = Domain.objects(domain=domain)[0]
    return render_template('showDomain.html', result=data)


@app.route('/domain_history', methods=['GET'])
def show_domain_history():
    domain = Domain.objects().order_by('-id')
    domain_temp = json.loads(domain.to_json())
    for data in domain_temp:
        epoch = str(data['exec_date']['$date'])[:10]
        data['exec_date'].update({'$date': datetime.datetime.fromtimestamp(int(epoch))})
    return render_template('show_domain_history.html', result=domain_temp)


@app.route('/ip_history', methods=['GET'])
def show_ip_history():
    data = Data.objects().order_by('-id')
    temp_list = json.loads(data.to_json())
    for data in temp_list:
        epoch = str(data['exec_date']['$date'])[:10]
        data['exec_date'].update({'$date': datetime.datetime.fromtimestamp(int(epoch))})

    return render_template('show_ip_history.html', result=temp_list)


@app.route('/deleteD/<id>', methods=['GET', 'POST'])
def delete(id):
    Domain.objects(id=id).delete()
    return redirect(url_for('show_domain_history'))


@app.route('/deleteI/<id>', methods=['GET', 'POST'])
def deleteI(id):
    Data.objects(id=id).delete()
    return redirect(url_for('show_ip_history'))


@app.route('/addEnv', methods=['POST'])
def add_env():
    App(name=request.form['env'], site=request.form['site'], key=request.form['key']).save()
    return {'response': 'Environment Added'}


@app.route('/env', methods=['GET'])
def environment():
    data = App.objects()
    return render_template('credentials.html', result=json.loads(data.to_json()))


app.config['MONGODB_SETTINGS'] = {'host': 'mongodb://localhost/data'}

initialize_db(app)

if __name__ == '__main__':
    app.run(port=4242)
