from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests
import json
import os
import mysql.connector
import urllib

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
   
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
	
def processRequest(req):
    if req.get("result").get("action")!="student_details":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    stud_name = parameters.get("stud_name")
    text = "Thanks for visiting us." + str(stud_name)
    print("responses")
    print(text)
    
    return {
        "text":text,
        "displaytext":text,
        "source":"student_details"
    }    

if __name__ == '__main__':
    port = int(os.getenv("port",80))
    print("starting app on port %d" %(port))   
    app.run(debug=True,port = port, host='0.0.0.0')	