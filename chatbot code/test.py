from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for
from flask_cors import CORS, cross_origin
import requests
import json
import os
import numpy
import mysql.connector
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


    if intent == "Do you have a any colleges in your mind for Engineering?":
        text = parameters.get("college")
        text1=str(text)
        text2 = text1.upper()
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        
        sql = ('SELECT distinct cs_collegename FROM cs_college_info ')
        cur.execute(sql)
        myresult = cur.fetchall()
        var=[]

        for x in myresult:
            var.extend(x)

        for cities in var:
            if text2 == cities:
    
                sql = ('SELECT distinct cs_college_info.cs_collegename,cs_col_nirf.cs_rank,cs_col_nirf.cs_score,cs_col_nirf_placements.no_of_intake,cs_col_nirf_placements.no_of_placed ,cs_col_nirf_placements.median_salary_for_placed FROM cs_college_info \
                           left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id \
                               left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
                                   left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates \
                                       left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type \
                                           WHERE  cs_college_info.cs_collegename ="%s"' %text2)   
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.extend(webhook)
                        
                fulfillmentText = 'NIRF rank: {} :'.format(college[1]) 
                return {
                    "fulfillmentMessages": [
                    {
                        "platform": "ACTIONS_ON_GOOGLE",
                        "simpleResponses": {
                        "simpleResponses": [
                            {
                            "textToSpeech": "basic info"
                            }
                        ]
                        }
                    },
                    {
                        "platform": "ACTIONS_ON_GOOGLE",
                        "suggestions": {
                        "suggestions": [
                            {
                            "title": college[0]
             
                            }
                        ]
                        }
                    },
                    {
                        "platform": "ACTIONS_ON_GOOGLE",
                        "suggestions": {
                        "suggestions": [
                            {
                            "title": college[1]
             
                            }
                        ]
                        }
                    },
                    {
                        "platform": "ACTIONS_ON_GOOGLE",
                        "suggestions": {
                        "suggestions": [
                            {
                            "title": college[2]
                
                            }
                        ]
                        }
                    },
                    {
                        "platform": "ACTIONS_ON_GOOGLE",
                        "suggestions": {
                        "suggestions": [
                            {
                            "title": college[3]
             
                            }
                        ]
                        }
                    },
                    {
                        "platform": "ACTIONS_ON_GOOGLE",
                        "suggestions": {
                        "suggestions": [
                            {
                            "title": college[4]
             
                            }
                        ]
                        }
                    }
                    ]
                    }
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port = 80)      
       