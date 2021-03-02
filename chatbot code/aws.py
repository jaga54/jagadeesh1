from flask_boto3 import Boto3
from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for
import requests
import json
import os
import numpy
import re

app = Flask(__name__)
BUCKET = "chatbot111333"
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
    
    
    # Welcome Intent:
    if intent == "Default Welcome Intent":
        return {
                        "payload": {
                        "google": {
                        "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                "textToSpeech": "Hey There 🙋 "   
                            }
                        },
                        {
                                "simpleResponse": {
                                "textToSpeech": "How you doin?"
                            }
                        },
                        {
                                "simpleResponse": {
                                "textToSpeech":"What can I help you with?"
                            }
                        }
                        ],
                        "suggestions": [
                            
                            {   
                                "title": "Suggest a College"     
                            },
                            {   
                                "title": "Suggest a Course"
                            },
                            {   
                                "title": "I want to know more about Admission Information"
                            },
                            {   
                                "title": "Compare colleges"
                            },
                            {   
                                "title": "Popular Entrance Exam"
                            }
                        ]  
                        }
                        }
                        }
                        }
                        
if __name__ == '__main__':
    app.run(debug=True)                        