from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests
import json
import os
import mysql.connector

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
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
    stud_name = parameters.get("stud_name")
    mobile = parameters.get("mobile")
    email = parameters.get("email")
    city = parameters.get("city")
    country = parameters.get("country")
    db = configureDataBase() 
    
    
    if intent == 'student_details':
        stud_name = parameters.get("stud_name")
        mobile = parameters.get("mobile")
        email = parameters.get("email")
        city = parameters.get("city")
        country = parameters.get("country")
        
        if(stud_name=="arun" or email == " asdf@asdf.com" or mobile =="1234567890" or city == "mumbai" or country =="India"):
            
            webhookresponse = ".Enter your name:" + str(fulfillmentText.get('name')) +"\t" + \
            "Enter your email address:" + str(fulfillmentText.get('email')) + "\t"+ \
            "Enter your mobile number:" + fulfillmentText.get('mobile')+ "\t"+ \
            "Enter your city:" + str(fulfillmentText.get('city')) + "\t"+ \
            "Enter your country:" + str(fulfillmentText.get('country')) + "\t"
            configureDataBase(webhookresponse)
        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            webhookresponse
                        ]

                    }
                },
                {
                    "text": {
                        "text": [
                           
                        ]

                    }
                }
            ]
        }    
            
    elif intent == "Default Welcome Intent" or intent == " Default Fallback Intent" or intent == " query":
        return result.get("fulfillmentText")   
       
def configureDataBase():
    # Open database connection
    db = mysql.connector.connect(host='localhost',
                             database='student',
                             user='root',
                             password='Chatbot')

    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database
    sqlstmt = "SELECT * FROM student WHERE stud_name = %(stud_name)s AND email = %(email)s and mobile = %(mobile)d and city = %(city)s and country = %(country)s"
    # Execute the SQL command
    cursor.execute(sqlstmt, {'stud_name': stud_name, 'email': email,'mobile': mobile, 'city': city, 'country':country})
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()  


if __name__ == '__main__':
   
    app.run(debug=False, host='0.0.0.0')