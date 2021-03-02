from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests
import json
import os
from flask_mysqldb import MySQL
import urllib

app = Flask(__name__)
@app.route('/webhook', methods=['GET', 'POST'])
@cross_origin()

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
 
        db = mysql.connector.connect(host='localhost',
                             database='student',
                             user='root',
                             password='Chatbot')
        cur = db.cursor()
        cur.execute("INSERT INTO stud_details(stud_name, mobile, email, city, country) VALUES (%s, %d, %s, %s, %s )", (stud_name, mobile, email, city, country))
        db.commit()
        cur.close()
        webhook = "Thanks you"
    return webhook
        
if __name__ == '__main__':
   
    app.run(debug=False, host='0.0.0.0', port = 80)