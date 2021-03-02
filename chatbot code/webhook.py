from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from flask_assistant import Assistant, ask,tell
import requests
import json
import os
import numpy
import MySQLdb
import re

app = Flask(__name__)
assist = Assistant(app,route='/webhook')

@assist.action('hello')
def hello():
    if intent =="Yes_Intent_Govt_Medical":
    
    
        return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "platform":"kommunicate",
            "message":render_template('details.html')
         }
      }
   ]
}

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port = 80)
