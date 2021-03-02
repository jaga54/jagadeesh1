from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests
import json
import os
import mysql.connector
import urllib
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

    if intent == "student_details":    
        stud_name = parameters.get("stud_name")
        email = parameters.get("email")
        mobile = parameters.get("mobile")
        city = parameters.get("city")
        country = parameters.get("country")
        
        webhook1 =  stud_name
        webhook2 =  email
        webhook3 = mobile
        webhook4 = city
        webhook5 = country
        
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
        cur = mydb.cursor()
        query = "INSERT INTO stud_details(stud_name, email,mobile,city,country) VALUES (%s,%s,%s, %s, %s )"
        val = (webhook1,webhook2,webhook3,webhook4,webhook5)
        cur.execute(query, val)
        result = cur.fetchall()
        for row in result:
            print(row[0], row[1], row[2], row[3], row[4])
            print("/n")
            
        mydb.commit()
        cur.close()
    return 0

if __name__ == '__main__':
   
    app.run(debug=False, host='0.0.0.0',port = 80)	