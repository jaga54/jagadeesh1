from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests
import json
import os
import mysql.connector
import urllib

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
    intent = result.get("intent").get('displayName')
    query_text = result.get("queryText")
    parameters = result.get("parameters")

    if intent == "student_details":    
        stud_name = parameters.get("stud_name")
        mobile = parameters.get("mobile")
        email = parameters.get("email")
        city = parameters.get("city")
        country = parameters.get("country")
        
        webhook = "stud_name:" + str(stud_name) + "mobile:" + int(mobile) + "email:" + str(email) + "city:" + city + "country" + country
        print(webhook)
       #configureDataBase(webhook)
    return 0
        
def configureDataBase(a,b,c,d,e):
    mydb = mysql.connector.connect(host='localhost',user='root',password='Chatbot',database='student')
    cur = mydb.cursor()
    numbers = cur.execute("select * from stud_details")
    num = numbers.fetchall()
    
    for row in num:
        cur.execute("INSERT INTO stud_details VALUES (%s, %d, %s, %s, %s )",(configureDataBase(row[0],row[1],row[2],row[3],row[4]))
        mydb.commit()
        cur.close()

if __name__ == '__main__':
   
    app.run(debug=False, host='0.0.0.0',port = 80)    