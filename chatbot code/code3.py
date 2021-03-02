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
    
    
    #Engineering college:
    if intent == "Engineering college":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Engineering Government college"
        fulfillmentText2 = "Top 10 Engineering Private colleges"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillmentText2 
                    }
                ]    
                }
                }
                }
                } 
                

        
   # Top 10 Engineering Government colleges in India                 
    if intent == "Form submitted_GVT_ENG":    
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT cs_collegename FROM cs_college_info where cs_col_category = "G" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
                        
        fulfillmentText = 'Top 10 Engineering Government colleges in India: '              
            
        if len(college) == 10: 
                
            return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[0]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[1]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[2]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[3]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[4]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[5]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[6]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[7]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[8]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[9]
                    }
                }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Engineering Colleges In India"
                            }
                ],
                
                "linkOutSuggestion":
                    {
                        "destinationName": "Webpage link for All India Top Engineering Governmentolleges",
                        "url": "https://"
                        }              
                }
                }
                }
                } 
               
# Top 10 Engineering Private colleges in India
    if intent == "Form submitted_PVT_ENG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT cs_collegename FROM cs_college_info where cs_col_category = "P" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
                        
        fulfillmentText = 'Top 10 Engineering Private colleges in India: '
                  
        if len(college) == 10: 
                
            return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[0]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[1]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[2]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[3]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[4]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[5]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[6]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[7]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[8]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[9]
                    }
                }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Engineering Colleges In India"
                            }
                ],
                
                "linkOutSuggestion":
                    {
                        "destinationName": "Webpage link for All India Top Engineering Private colleges",
                        "url": "https://"
                        }              
                }
                }
                }
                } 
                    
 # AreaWise Top Engineering Colleges In India        
    if intent == "AreaWise Top Engineering Colleges In India":
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
    
                sql = ('SELECT distinct cs_college_info.cs_collegename\
                        FROM cs_city left join cs_college_info on cs_city.cs_sno = cs_college_info.cs_col_city\
                        WHERE cs_city.cs_city = "%s" limit 5 ' %city )    
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.extend(webhook)    
                        
                fulfillmentText = 'Top colleges in {} :'.format(city)
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
                        ]   
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
                        ]  
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
                        ] 
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
                        ]
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
                        ] 
                        }
                        }
                        }
                        }
                        
 # Medical college:
    if intent == "Medical college":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Medical Government college"
        fulfillmentText2 = "Top 10 Medical Private colleges"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillmentText2 
                    }
                ]    
                }
                }
                }
                } 
                
# Top 10 Medical Government colleges in India                 
    if intent == "Form submitted_GVT_Medical":       
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT cs_collegename FROM cs_college_info where cs_col_category = "G" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
                        
        fulfillmentText = 'Top 10 medical Government colleges in India: '              
            
        if len(college) == 10: 
                
            return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[0]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[1]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[2]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[3]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[4]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[5]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[6]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[7]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[8]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[9]
                    }
                }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Medical Colleges In India"
                            }
                ],
                
                "linkOutSuggestion":
                    {
                        "destinationName": "Webpage link for All India Top Medical Government colleges",
                        "url": "https://"
                        }              
                }
                }
                }
                }             
# Top 10 Medical Private colleges in India                 
    if intent == "Form submitted_PVT_Medical":
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT cs_collegename FROM cs_college_info where cs_col_category = "G" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
                        
        fulfillmentText = 'Top 10 medical Private colleges in India: '              
            
        if len(college) == 10: 
                
            return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[0]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[1]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[2]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[3]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[4]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[5]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[6]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[7]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[8]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[9]
                    }
                }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Medical Colleges In India"
                            }
                ],
                
                "linkOutSuggestion":
                    {
                        "destinationName": "Webpage link for All India Top Medical Government colleges",
                        "url": "https://"
                        }              
                }
                }
                }
                } 
             
# AreaWise Top Medical Colleges In India        
    if intent == "AreaWise Top Medical Colleges In India":
        city = parameters.get("city") 
        city = str(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='medical')
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
    
                sql = ('SELECT distinct cs_college_info.cs_collegename\
                        FROM cs_city left join cs_college_info on cs_city.cs_sno = cs_college_info.cs_col_city\
                        WHERE cs_city.cs_city = "%s" limit 5 ' %city )    
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.extend(webhook)    
                        
                fulfillmentText = 'Top colleges in {} :'.format(city)
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
                        ]   
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
                        ]  
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
                        ] 
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
                        ]
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
                        ] 
                        }
                        }
                        }
                        }     

#Architecture college:
    if intent == "Architecture college":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Architecture Government college"
        fulfillmentText2 = "Top 10 Architecture Private colleges"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillmentText2 
                    }
                ]    
                }
                }
                }
                } 
                
                
# Top 10 Architecture Government colleges in India                 
    if intent == "Form submitted_GVT_Architecture":       
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT cs_collegename FROM cs_college_info where cs_col_category = "G" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
                        
        fulfillmentText = 'Top 10 Architecture Government colleges in India: '              
            
        if len(college) == 10: 
                
            return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[0]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[1]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[2]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[3]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[4]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[5]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[6]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[7]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[8]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[9]
                    }
                }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Architecture Colleges In India"
                            }
                ],
                
                "linkOutSuggestion":
                    {
                        "destinationName": "Webpage link for All India Top Architecture Government colleges",
                        "url": "https://"
                        }              
                }
                }
                }
                }             
# Top 10 Architecture Private colleges in India                 
    if intent == "Form submitted_PVT_Architecture":
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT cs_collegename FROM cs_college_info where cs_col_category = "G" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
                        
        fulfillmentText = 'Top 10 Architecture Private colleges in India: '              
            
        if len(college) == 10: 
                
            return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[0]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[1]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[2]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[3]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[4]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[5]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[6]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[7]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[8]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[9]
                    }
                }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Architecture Colleges In India"
                            }
                ],
                
                "linkOutSuggestion":
                    {
                        "destinationName": "Webpage link for All India Top Architecture Government colleges",
                        "url": "https://"
                        }              
                }
                }
                }
                } 
             
# AreaWise Top Architecture Colleges In India        
    if intent == "AreaWise Top Architecture Colleges In India":
        city = parameters.get("city") 
        city = str(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='architecture')
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
    
                sql = ('SELECT distinct cs_college_info.cs_collegename\
                        FROM cs_city left join cs_college_info on cs_city.cs_sno = cs_college_info.cs_col_city\
                        WHERE cs_city.cs_city = "%s" limit 5 ' %city )    
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.extend(webhook)    
                        
                fulfillmentText = 'Top colleges in {} :'.format(city)
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
                        ]   
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
                        ]  
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
                        ] 
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
                        ]
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
                        ] 
                        }
                        }
                        }
                        }
             
#Dental college:
    if intent == "Dental college":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Dental Government college"
        fulfillmentText2 = "Top 10 Dental Private colleges"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillmentText2 
                    }
                ]    
                }
                }
                }
                } 
                
# Top 10 Dental Government colleges in India
    if intent == "Form submitted_GVT_Dental": 
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT cs_collegename FROM cs_college_info where cs_col_category = "P" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
                        
        fulfillmentText = 'Top 10 Dental Government colleges in India: '
                  
        if len(college) == 10: 
                
            return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[0]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[1]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[2]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[3]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[4]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[5]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[6]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[7]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[8]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[9]
                    }
                }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Dental Colleges In India"
                            }
                ],
                
                "linkOutSuggestion":
                    {
                        "destinationName": "Webpage link for All India Top Dental Private colleges",
                        "url": "https://"
                        }              
                }
                }
                }
                }  
               
# Top 10 Engineering Private colleges in India
    if intent == "Form submitted_PVT_Dental": 
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT cs_collegename FROM cs_college_info where cs_col_category = "P" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
                        
        fulfillmentText = 'Top 10 Dental Private colleges in India: '
                  
        if len(college) == 10: 
                
            return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[0]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[1]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[2]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[3]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[4]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[5]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[6]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[7]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[8]
                    }
                },
                {
                        "simpleResponse": {
                        "textToSpeech": college[9]
                    }
                }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Dental Colleges In India"
                            }
                ],
                
                "linkOutSuggestion":
                    {
                        "destinationName": "Webpage link for All India Top Dental Private colleges",
                        "url": "https://"
                        }              
                }
                }
                }
                } 
                    
 # AreaWise Top Dental Colleges In India        
    if intent == "AreaWise Top Dental Colleges In India":
        city = parameters.get("city") 
        city = str(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='dental')
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
    
                sql = ('SELECT distinct cs_college_info.cs_collegename\
                        FROM cs_city left join cs_college_info on cs_city.cs_sno = cs_college_info.cs_col_city\
                        WHERE cs_city.cs_city = "%s" limit 5 ' %city )    
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.extend(webhook)    
                        
                fulfillmentText = 'Top colleges in {} :'.format(city)
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
                        ]   
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
                        ]  
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
                        ] 
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
                        ]
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
                        ] 
                        }
                        }
                        }
                        }        
                
                
    return 0
    
if __name__ == '__main__':
    app.run(debug=False,port = 80)