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
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='details')
        cur = mydb.cursor()
        query = "INSERT INTO studentdetails(name,email) VALUES (%s,%s)"
        val = (name,email)
        cur.execute(query, val)
        result = cur.fetchall()
        for row in result:
            print(row[0], row[1])
            print("/n")       
            
        mydb.commit()
        cur.close()
        return {}
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
    
def processRequest(req):
    print("Request:")
    print(json.dumps(req, indent=4))
    result = req.get("queryResult")
    if result.get("intent").get('displayName') == "Yes_Intent_Govt_Engineering":
        data = req
        res = student(data)
        
        
    elif result.get("intent").get('displayName') == "Form submitted_GVT_ENG":
        data = req
        res = result(data)
        
    else:
        return {}
    return res
    
def student(data):    
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
    app.run(debug=False,port = 80)
    
