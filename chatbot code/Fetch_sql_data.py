from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests
import json
import os
import mysql.connector
import urllib
import numpy
import MySQLdb
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import os
import dialogflow

app = Flask(__name__)
@app.route('/webhook', methods=[ 'POST','GET'])


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
    college = []
    
    if intent == "cityofcolleges":
        city = parameters.get("city")
        city = str(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
        cur = mydb.cursor()
        if city == "Bengaluru":
            sql = 'SELECT College_Name FROM stud_details1 WHERE city ="Bengaluru"'     
            cur.execute(sql)
            myresult = cur.fetchall()
            for webhook in myresult:
                college.append(webhook)
                print(college)
            fulfillmentText = 'list of colleges in Bengaluru {}'.format(college)
            #fulfillmentText = 'college_name, NIRF_rank , NIRF_score , NAAC_Grade , city , District , State , campus_area = {}'.format(college)
        elif city == "Gharuan":
            sql = 'SELECT College_Name FROM stud_details1 WHERE city ="Gharuan"'
            cur.execute(sql)
            myresult = cur.fetchall()
            for webhook in myresult:
                college.append(webhook)
                print(webhook)
            fulfillmentText = 'list of colleges in Gharuan {}'.format(college)
        elif city == "chennai":
            sql = 'SELECT College_Name FROM stud_details1 WHERE city ="chennai"'
            cur.execute(sql)
            myresult = cur.fetchall()
            for webhook in myresult:
                college.append(webhook)
                print(webhook)
            fulfillmentText = 'list of colleges in chennai {}'.format(college)    
        elif city == "Belgaum":           
            sql = 'SELECT College_Name FROM stud_details1 WHERE city ="Belgaum"'
            cur.execute(sql)
            myresult = cur.fetchall()
            for webhook in myresult:
                college.append(webhook)
                print(webhook)
            fulfillmentText = 'list of colleges in Belgaum {}'.format(college)  
            
        else: 
            sql = 'SELECT College_Name FROM stud_details1 WHERE city ="Phagwara"'
            cur.execute(sql)
            myresult = cur.fetchall()
            for webhook in myresult:
                college.append(webhook)
                print(webhook)
            fulfillmentText = 'list of colleges in Phagwara {}'.format(college)
           

           

    return {
        "fulfillmentText": fulfillmentText,
        "displayText": fulfillmentText,
        "source": fulfillmentText
    }
        

if __name__ == '__main__':
   
    app.run(debug=False, host='0.0.0.0',port = 80)        