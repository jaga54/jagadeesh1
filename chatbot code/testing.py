from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for,session
from flask_cors import CORS, cross_origin
import requests
import json
import os
import numpy
import mysql.connector
import MySQLdb
import re


app = Flask(__name__)

@app.route('/sample', methods=['POST','GET'])  
def sample(): 
    if "username" in session:
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Form Submitted",
            "platform": "kommunicate"
        }
    }
       ]   
    }
    #else:
        

@app.route('/result', methods=[ 'POST','GET'])
def result(): 
    
    if request.method == 'POST':
        name = request.form["Name"]
        email = request.form["Email"]
        phone = request.form["Phone"]
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='details')
        cur = mydb.cursor()
        query = "INSERT INTO studentdetails(name,email,phone) VALUES (%s,%s,%s)"
        val = (name,email,phone)
        cur.execute(query, val)
        result = cur.fetchall()         
        mydb.commit()
        cur.close()
        session['username'] = name
        print(session['username'])
        return redirect(url_for('sample')) 
    return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form submitted",
            "requestType": "POST",
            "formAction": ""
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
} 

@app.route('/form', methods=['POST','GET'])  
def form():
    if request.method == 'POST':
        name = request.form["Name"]
        phone = request.form["Phone"]
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='details1')  
        cur = mydb.cursor()
        query = "INSERT INTO studentdetails(name,phone) VALUES (%s,%s)"
        val = (name,phone)
        cur.execute(query, val)
        result = cur.fetchall()
        for row in result:
            print(row[0], row[1])
            print("/n")       
            
        mydb.commit()
        cur.close() 
    return "ok"  
        

                  
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
    name =0
    sessionID = req.get('responseId')
    result = req.get("queryResult")                                  
    result = req.get("queryResult")                                  
    intent = result.get("intent").get('displayName') 
    query_text = result.get("queryText")                   
    parameters = result.get("parameters")   
    
    fulfillmentText = ''
    
    
    
# html form showed in the chatbot:
    if intent == "Yes_Intent_Govt_Engineering": 
        if name != 1:
            #session["name"] = 1
            return redirect(url_for('result'))
        
                
                               
    return 0
    
if __name__ == '__main__':
    app.run(debug=False,port = 80)