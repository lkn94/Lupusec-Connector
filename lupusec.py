from flask import Flask
from flask_restful import Api
import requests
from requests.auth import HTTPBasicAuth
import json

app = Flask(__name__)
api = Api(app)

lupusIp = ""
username = ""
password = ""

@app.route('/')
def main():
    return "Lupusec Connector written in python by Lukas Knoeller <support@hobbyblogging.de>"

@app.route('/alarmstate')
def alarmstate():
    response = requests.get("http://{}/action/panelCondGet".format(lupusIp), verify=False, auth=HTTPBasicAuth(username, password))
    return (response.json())

@app.route('/sensor/<string:sensorid>')
def sensor(sensorid):
    response = requests.get("http://{}/action/deviceListGet".format(lupusIp), verify=False, auth=HTTPBasicAuth(username, password))
    text = response.text.replace("\t", "").replace("\n", "")
    textAsJson = json.loads(text);
    for sensor in textAsJson["senrows"]:
        if (sensor["sid"] == "RF:{}".format(sensorid)):
            return sensor;
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
