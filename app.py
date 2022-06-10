from flask import Flask, request, jsonify
import json 
from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy
)
import os, uuid

app = Flask(__name__)
app.config["DEBUG"] = True 

CONNECTION_STR = os.getenv("CONNECTION_STRING")

CONNECTION_STR = os.environ['SERVICE_BUS_CONNECTION_STR']
SESSION_QUEUE_NAME = os.environ["SERVICE_BUS_SESSION_QUEUE_NAME"]
SESSION_ID = os.environ['SERVICE_BUS_SESSION_ID']

@app.route('/', methods=['GET'])
def home():
    output = "<h1>Welcome to Ahsan's bug destroyer.</h1>"
    return output

@app.route("/api", methods=['POST'])
def triage_bugs():

    #Validating the API request
    if not request.json or not 'title' in request.json or not 'city' in request.json or not 'priority' in request.json\
    or request.json['priority'] not in {"High", "Medium", "Low"}\
    or request.json['city'] not in {"London", "Manchester", "Sheffield", "Southampton"}:
        QUEUE_NAME = "invalidrequests"
        sendMessage(CONNECTION_STR,QUEUE_NAME,str(request.json))

    elif request.json['priority'] == "High":
        QUEUE_NAME = "highpriority"
        sendMessage(CONNECTION_STR,QUEUE_NAME,str(request.json))

    else:
        QUEUE_NAME = "generalbugs"
        sendMessage(CONNECTION_STR,QUEUE_NAME,str(request.json))

    return request.json

if __name__ == "__main__":
    app.run()