from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from flask_assistant import Assistant, ask,tell
import requests
import json
import os
import numpy
import MySQLdb
import re

app = Flask(__name__)
assist = Assistant(app, route='/webhook')
#@app.route('/webhook', methods=[ 'POST',"GET"])

@assist.action('cities')
def processRequest():
    
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
                    college.extend(webhook)    

                fulfillmentText = 'top colleges in {} :'.format(city)
                
                
                lst = []
                mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
                cur = mydb.cursor()
                query = "select cs_collegename , cs_college_page_url from cs_college_info "
                cur.execute(query)
                result = cur.fetchall()

                for i in result:
                    lst.extend(i)
                    
                #Dictionary format using to get the key value of college_page_url
                res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
                res_dct         
                url = res_dct[college[0]] 
                url1 = res_dct[college[1]] 
            
                if len(college) == 5:  
                
                    return {
                        "payload": {
                        "google": {
                        "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                "textToSpeech": fulfillmentText
                            }
                        }
                        ],
                        "suggestions": [
                            {   
                                "title": college[0] 
                            },
                            {   
                                "title": college[1] 
                            },
                            {   
                                "title": college[2] 
                            },
                            {   
                                "title": college[3] 
                            },
                            {   
                                "title": college[4] 
                            }
                        ],
                        "linkOutSuggestion":
                        {
                            "destinationName": college[0] + " link ",
                            "url": url
                            }    
                        }
                        }
                        }
                        }
                        
                elif len(college) == 4:  
                
                    return {
                        "payload": {
                        "google": {
                        "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                "textToSpeech": fulfillmentText
                            }
                        }
                        ],
                        "suggestions": [
                            {   
                                "title": college[0] 
                            },
                            {   
                                "title": college[1] 
                            },
                            {   
                                "title": college[2] 
                            },
                            {   
                                "title": college[3] 
                            }
                        ],
                        "linkOutSuggestion":
                        {
                            "destinationName": college[0] + " link ",
                            "url": url
                            } 
                        
                        }
                        }
                        }
                        } 

                elif len(college) == 3:  
                
                    return {
                        "payload": {
                        "google": {
                        "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                "textToSpeech": fulfillmentText
                            }
                        }
                        ],
                        "suggestions": [
                            {   
                                "title": college[0] 
                            },
                            {   
                                "title": college[1] 
                            },
                            {   
                                "title": college[2] 
                            }
                        ],
                        "linkOutSuggestion":
                        {
                            "destinationName": college[0] + " link ",
                            "url": url
                            } 
                        
                        }
                        }
                        }
                        }
                        
                elif len(college) == 2:  
                
                    return {
                        "payload": {
                        "google": {
                        "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                "textToSpeech": fulfillmentText
                            }
                        }
                        ],
                        "suggestions": [
                            {   
                                "title": college[0] 
                            },
                            {   
                                "title": college[1] 
                            }
                        ],
                        "linkOutSuggestion":
                        {
                            "destinationName": college[0] + " link ",
                            "url": url
                            } 
                        
                        }
                        }
                        }
                        } 
                            
                elif len(college) == 1:  
                
                    return {
                        "payload": {
                        "google": {
                        "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                "textToSpeech": fulfillmentText
                            }
                        }
                        ],
                        "suggestions": [
                            {   
                                "title": college[0] 
                            }
                        ],
                        "linkOutSuggestion":
                        {
                            "destinationName": college[0] + " link ",
                            "url": url
                            } 
                        
                        }
                        }
                        }
                        }        
                                    
                        
               
    return 0                 
             

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port = 80)      



















                    