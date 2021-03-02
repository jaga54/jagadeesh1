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
    req = request.get_json(silent=True, force=True)
    req1 = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res1 = processRequests(req1)
    res = json.dumps(res, indent=4)
    res1 = json.dumps(res1, indent=4)
    print(res)
    print(res1)
    r = make_response(res)
    r1 = make_response(res1)
    r.headers['Content-Type'] = 'application/json'
    r1.headers['Content-Type'] = 'application/json'
    return r , r1

def processRequest(req):
    sessionID = req.get('responseId')
    result = req.get("queryResult")                                  
    result = req.get("queryResult")                                  
    intent = result.get("intent").get('displayName')
    
    query_text = result.get("queryText")                   
    parameters = result.get("parameters")
    fulfillmentText = ''
    college = []


    if intent == "studentdetails": 
        stud_name = parameters.get("stud_name")
        email = parameters.get("email")
        mobile = parameters.get("mobile")
        city = parameters.get("city")
        country = parameters.get("country")
        db = InsertDataBaseDetails(stud_name,email,mobile,city,country)
        
        
        
    
    
    return 0
    
    
def processRequests(req1):
    sessionID = req1.get('responseId')
    result = req1.get("queryResult")                                  
    result = req.get("queryResult")                                  
    intent = result.get("intent").get('displayName')
    
    query_text = result.get("queryText")                   
    parameters = result.get("parameters")
    fulfillmentText = ''
    college = []
    if intent == "listcolleges":
        city = parameters.get("city")
        city = str(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
        cur = mydb.cursor()
        city = city
        if city == "chennai":
            sql = 'select cs_college_info.cs_collegename,cs_college_info.cs_col_phone,cs_college_info.cs_col_email \
                   from cs_city inner join cs_college_info\
                    on cs_city.cs_district = cs_college_info.cs_col_district where cs_city.cs_city="chennai"'     
            cur.execute(sql)
            myresult = cur.fetchall()
            for webhook in myresult:
                print("College_name, phone_num,college_email",webhook)
                college.append(webhook)
            fulfillmentText = 'list of colleges in chennai : College_name, phone_num,college_email {}'.format(college)
        
        elif  city == "Port Blair":
            sql = 'select cs_college_info.cs_collegename,cs_college_info.cs_col_phone,cs_college_info.cs_col_email \
                from cs_city inner join cs_college_info\
                on cs_city.cs_district = cs_college_info.cs_col_district where cs_city.cs_city="Port Blair"'     
            cur.execute(sql)
            myresult = cur.fetchall()
            for webhook in myresult:
                print("College_name, phone_num,college_email",webhook)
                college.append(webhook)
            fulfillmentText = 'list of colleges in Port Blair : College_name, phone_num,college_email {}'.format(college)  
    
    return {
            "fulfillmentText": fulfillmentText,
            "displayText": fulfillmentText,
            "source": fulfillmentText
    }

def InsertDataBaseDetails(stud_name,email,mobile,city,country):
    mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student1')
    cur = mydb.cursor()
    query = "INSERT INTO stud_details(stud_name, email,Phone_number,city,country) VALUES (%s,%s,%s, %s, %s )"
    val = (stud_name,email,mobile,city,country)
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
	