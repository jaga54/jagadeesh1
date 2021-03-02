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


    if intent == "studentdetails": 
        stud_name = parameters.get("stud_name")
        email = parameters.get("email")
        mobile = parameters.get("mobile")
        city = parameters.get("city")
        country = parameters.get("country")
        db = InsertDataBaseDetails(stud_name,email,mobile,city,country)
        
    else: 
        return 0
        
    if intent == "listcolleges":
        city = parameters.get("city")
        city = str(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        city = city
        sql = "select  DISTINCT  cs_city from cs_city"
        cur.execute(sql)
        myresult = cur.fetchall()
        var=[]

        for x in myresult:
            var.extend(x)

        for cities in var:
            if city == cities:
    
                sql = ('SELECT  cs_college_info.cs_collegename\
                        FROM cs_city left join cs_college_info on cs_city.cs_sno = cs_college_info.cs_col_city\
                        WHERE cs_city.cs_city = "%s" limit 5 ' %city )    
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.append(webhook)
                fulfillmentText = 'top colleges in {0} : College_name, phone_num,college_email {1}'.format(city,college)
                
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
	