from flask import Flask
from flask_restful import Api
import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
from requests_html import HTMLSession

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
api = Api(app)

lupusIp = "IP of your alarm system"
username = "username"
password = "password"
xtoken = "your x-token"

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

@app.route('/setstate/<int:stateid>')
def setstate(stateid):
    session = requests.Session()
    session.get("http://{}/action/panelCondGet".format(lupusIp), verify=False, auth=HTTPBasicAuth(username, password))
    response = requests.post("https://{}/action/panelCondPost".format(lupusIp), headers={"content-type": "application/x-www-form-urlencoded", "x-token": xtoken}, data={"area": 1, "mode": stateid}, verify=False, auth=HTTPBasicAuth(username, password))
    return "{}".format(response.text)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
