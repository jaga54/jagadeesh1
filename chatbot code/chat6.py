from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests
import json
import os
import mysql.connector
import urllib
import numpy
import MySQLdb


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
		conn = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student1')
        cur = conn.cursor()
		cursor = cur.execute("INSERT INTO stud_details(stud_name, mobile,email,city,country) VALUES (%s,%d,%s, %s, %s )"%(stud_name,int(mobile),email,city,country))
		for row in cursor:
			print "stud_name = ", row[0]
			print "mobile = ", row[1]
			print "email = ", row[2]
			print "city = ", row[3]
			print "country = ", row[4], "\n"

		conn.commit()
		conn.close()
	return 0
	
if __name__ == '__main__':
   
    app.run(debug=False, host='0.0.0.0',port = 80)	
		
	