from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests
import json
import os
import numpy
import MySQLdb
import re

app = Flask(__name__)
@app.route('/webhook', methods=[ 'POST',"GET"])


def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
    
    

def processRequest(req):
    sessionID = req.get('responseId')
    result = req.get("queryResult")                                  
    result = req.get("queryResult")                                  
    intent = result.get("intent").get('displayName') 
    
    query_text = result.get("queryText")                   
    parameters = result.get("parameters")   
    
    fulfillmentText = ''
    
    
    if intent == "studentdetails":
        return {
            "fulfillmentMessages": [{
                "payload": {
                "message": "student details",
                "platform": "kommunicate",
                "metadata": {
                    "contentType": "300",
                    "templateId": "3",
                    "payload": [{
                    "type": "text",
                    "data": {
                    "label": "Name",
                    "placeholder": "Enter your name"
                    }
                    },
                        {
                            "type": "text",
                            
                            "Email": "Email"
                        }
                    ]
                }
            }
        },   
        {
            "payload": {
                "message": "form submitted",
                "platform": "kommunicate"
            }
        }
        ]
        }
    return 0    
            
    
    
if __name__ == '__main__':
    app.run(debug=False,port = 80)