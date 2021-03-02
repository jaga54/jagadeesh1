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

#webhook
    if intent == "Yes_Intent_Govt_Engineering":
        if request.method == 'POST':
            Name = request.form.get("Name")
            Email = request.form.get("Email")
            Mobile = request.form.get("Mobile")
            
            mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
            cur = mydb.cursor()
            query = "INSERT INTO stud_details(stud_name, email,Phone_number) VALUES (%s,%s,%s)"
            val = (Name,Email,Mobile)
            cur.execute(query, val)
            result = cur.fetchall()
            for row in result:
                print(row[0], row[1], row[2], row[3], row[4])
                print("/n")
            
            mydb.commit()
            cur.close()
            fulfillment = render_template("index.html")
            return {
        "fulfillmentMessages":[
            {
                "payload":{
                "messageType":"html",
                "platform":"kommunicate",
                "message":fulfillment
            }
        } 
    ]
    }
            
             
   # Top 10 Engineering Government colleges in India                 
    if intent == "Form submitted_GVT_ENG":  
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
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
                        "textToSpeech": "1."+college[0] + "\n"+"2." + college[1]+ "\n" +"3." +college[2]+ "\n"+ "4."+ college[3]+ "\n"+"5." + college[4]+ "\n"+"6." + college[5]+ "\n"+"7." + college[6]+ "\n" +"8."+ college[7]+ "\n" +"9."+ college[8]+ "\n"+"10." + college[9]+"\n"+"http://demo.vvtsolutions.in/cstooldev/HTML/index-1.html"
                    }
                }
                ],
                 "suggestions":[
                            {   
                                "title": "AreaWise Top Engineering Colleges In India"
                            }
                ]
                }
                }
                }
                } 
               
# Top 10 Engineering Private colleges in India
    if intent == "Form submitted_PVT_ENG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
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
                        "textToSpeech": "1."+college[0] + "\n"+"2." + college[1]+ "\n" +"3." +college[2]+ "\n"+ "4."+ college[3]+ "\n"+"5." + college[4]+ "\n"+"6." + college[5]+ "\n"+"7." + college[6]+ "\n" +"8."+ college[7]+ "\n" +"9."+ college[8]+ "\n"+"10." + college[9]+"\n"+"http://demo.vvtsolutions.in/cstooldev/HTML/index-1.html"
                    }
                    }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Engineering Colleges In India"
                            }
                ]             
                }
                }
                }
                } 
                    
 # AreaWise Top Engineering Colleges In India        
    if intent == "AreaWise Top Engineering Colleges In India":
        city = parameters.get("city") 
        city = str(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." + str(college[1])+ "\n"+"3." + str(college[2])+ "\n"+"4." + str(college[3])+ "\n"+ "5." +str(college[4])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." +str( college[1])+ "\n"+"3." + str(college[2])+ "\n"+"4." + str(college[3])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." +str( college[1])+ "\n"+"3." +str( college[2])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." + str(college[1])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+ str(college[0])
                            }
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
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
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
                        "textToSpeech": "1."+college[0] + "\n"+"2." + college[1]+ "\n" +"3." +college[2]+ "\n"+ "4."+ college[3]+ "\n"+"5." + college[4]+ "\n"+"6." + college[5]+ "\n"+"7." + college[6]+ "\n" +"8."+ college[7]+ "\n" +"9."+ college[8]+ "\n"+"10." + college[9]+"\n"+"http://demo.vvtsolutions.in/cstooldev/HTML/index-1.html"
                    }
                }
                ],
                 "suggestions":[
                            {   
                                "title": "AreaWise Top Medical Colleges In India"
                            }
                ]
                }
                }
                }
                } 
# Top 10 Medical Private colleges in India                 
    if intent == "Form submitted_PVT_Medical":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
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
                        "textToSpeech": "1."+college[0] + "\n"+"2." + college[1]+ "\n" +"3." +college[2]+ "\n"+ "4."+ college[3]+ "\n"+"5." + college[4]+ "\n"+"6." + college[5]+ "\n"+"7." + college[6]+ "\n" +"8."+ college[7]+ "\n" +"9."+ college[8]+ "\n"+"10." + college[9]+"\n"+"http://demo.vvtsolutions.in/cstooldev/HTML/index-1.html"
                    }
                    }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Medical Colleges In India"
                            }
                ]             
                }
                }
                }
                }  
             
# AreaWise Top Medical Colleges In India        
    if intent == "AreaWise Top Medical Colleges In India":
        city = parameters.get("city") 
        city = str(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." + str(college[1])+ "\n"+"3." + str(college[2])+ "\n"+"4." + str(college[3])+ "\n"+ "5." +str(college[4])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." +str( college[1])+ "\n"+"3." + str(college[2])+ "\n"+"4." + str(college[3])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." +str( college[1])+ "\n"+"3." +str( college[2])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." + str(college[1])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+ str(college[0])
                            }
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
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
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
                        "textToSpeech": "1."+college[0] + "\n"+"2." + college[1]+ "\n" +"3." +college[2]+ "\n"+ "4."+ college[3]+ "\n"+"5." + college[4]+ "\n"+"6." + college[5]+ "\n"+"7." + college[6]+ "\n" +"8."+ college[7]+ "\n" +"9."+ college[8]+ "\n"+"10." + college[9]+"\n"+"http://demo.vvtsolutions.in/cstooldev/HTML/index-1.html"
                    }
                    }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Architecture Colleges In India"
                            }
                ]             
                }
                }
                }
                }               
# Top 10 Architecture Private colleges in India                 
    if intent == "Form submitted_PVT_Architecture":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
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
                        "textToSpeech": "1."+college[0] + "\n"+"2." + college[1]+ "\n" +"3." +college[2]+ "\n"+ "4."+ college[3]+ "\n"+"5." + college[4]+ "\n"+"6." + college[5]+ "\n"+"7." + college[6]+ "\n" +"8."+ college[7]+ "\n" +"9."+ college[8]+ "\n"+"10." + college[9]+"\n"+"http://demo.vvtsolutions.in/cstooldev/HTML/index-1.html"
                    }
                    }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Architecture Colleges In India"
                            }
                ]             
                }
                }
                }
                }  
             
# AreaWise Top Architecture Colleges In India        
    if intent == "AreaWise Top Architecture Colleges In India":
        city = parameters.get("city") 
        city = str(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." + str(college[1])+ "\n"+"3." + str(college[2])+ "\n"+"4." + str(college[3])+ "\n"+ "5." +str(college[4])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." +str( college[1])+ "\n"+"3." + str(college[2])+ "\n"+"4." + str(college[3])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." +str( college[1])+ "\n"+"3." +str( college[2])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." + str(college[1])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+ str(college[0])
                            }
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
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
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
                        "textToSpeech": "1."+college[0] + "\n"+"2." + college[1]+ "\n" +"3." +college[2]+ "\n"+ "4."+ college[3]+ "\n"+"5." + college[4]+ "\n"+"6." + college[5]+ "\n"+"7." + college[6]+ "\n" +"8."+ college[7]+ "\n" +"9."+ college[8]+ "\n"+"10." + college[9]+"\n"+"http://demo.vvtsolutions.in/cstooldev/HTML/index-1.html"
                    }
                    }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Dental Colleges In India"
                            }
                ]             
                }
                }
                }
                }   
               
# Top 10 dental Private colleges in India
    if intent == "Form submitted_PVT_Dental": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
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
                        "textToSpeech": "1."+college[0] + "\n"+"2." + college[1]+ "\n" +"3." +college[2]+ "\n"+ "4."+ college[3]+ "\n"+"5." + college[4]+ "\n"+"6." + college[5]+ "\n"+"7." + college[6]+ "\n" +"8."+ college[7]+ "\n" +"9."+ college[8]+ "\n"+"10." + college[9]+"\n"+"http://demo.vvtsolutions.in/cstooldev/HTML/index-1.html"
                    }
                    }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Dental Colleges In India"
                            }
                ]             
                }
                }
                }
                }  
                    
 # AreaWise Top Dental Colleges In India        
    if intent == "AreaWise Top Dental Colleges In India":
        city = parameters.get("city") 
        city = str(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." + str(college[1])+ "\n"+"3." + str(college[2])+ "\n"+"4." + str(college[3])+ "\n"+ "5." +str(college[4])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." +str( college[1])+ "\n"+"3." + str(college[2])+ "\n"+"4." + str(college[3])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." +str( college[1])+ "\n"+"3." +str( college[2])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." + str(college[1])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+ str(college[0])
                            }
                        }
                        ] 
                        }
                        }
                        }
                        }
#Pharmacy college:
    if intent == "Pharmacy college":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Pharmacy Government college"
        fulfillmentText2 = "Top 10 Pharmacy Private colleges"
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
                
# Top 10 Pharmacy Government colleges in India
    if intent == "Form submitted_GVT_Pharmacy": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT cs_collegename FROM cs_college_info where cs_col_category = "P" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
                        
        fulfillmentText = 'Top 10 Pharmacy Government colleges in India: '
                  
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
                        "textToSpeech": "1."+college[0] + "\n"+"2." + college[1]+ "\n" +"3." +college[2]+ "\n"+ "4."+ college[3]+ "\n"+"5." + college[4]+ "\n"+"6." + college[5]+ "\n"+"7." + college[6]+ "\n" +"8."+ college[7]+ "\n" +"9."+ college[8]+ "\n"+"10." + college[9]+"\n"+"http://demo.vvtsolutions.in/cstooldev/HTML/index-1.html"
                    }
                    }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Pharmacy Colleges In India"
                            }
                ]             
                }
                }
                }
                } 
               
# Top 10 Pharmacy Private colleges in India
    if intent == "Form submitted_PVT_Pharmacy": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT cs_collegename FROM cs_college_info where cs_col_category = "P" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
                        
        fulfillmentText = 'Top 10 Pharmacy Private colleges in India: '
                  
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
                        "textToSpeech": "1."+college[0] + "\n"+"2." + college[1]+ "\n" +"3." +college[2]+ "\n"+ "4."+ college[3]+ "\n"+"5." + college[4]+ "\n"+"6." + college[5]+ "\n"+"7." + college[6]+ "\n" +"8."+ college[7]+ "\n" +"9."+ college[8]+ "\n"+"10." + college[9]+"\n"+"http://demo.vvtsolutions.in/cstooldev/HTML/index-1.html"
                    }
                    }
                ],
                 "suggestions":[ 
                            {   
                                "title": "AreaWise Top Pharmacy Colleges In India"
                            }
                ]             
                }
                }
                }
                } 
                    
 # AreaWise Top Pharmacy Colleges In India        
    if intent == "AreaWise Top Pharmacy Colleges In India":
        city = parameters.get("city") 
        city = str(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." + str(college[1])+ "\n"+"3." + str(college[2])+ "\n"+"4." + str(college[3])+ "\n"+ "5." +str(college[4])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." +str( college[1])+ "\n"+"3." + str(college[2])+ "\n"+"4." + str(college[3])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." +str( college[1])+ "\n"+"3." +str( college[2])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+str(college[0]) + "\n"+"2." + str(college[1])
                            }
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
                        },
                            {
                            "simpleResponse": {
                            "textToSpeech": "1."+ str(college[0])
                            }
                        }
                        ] 
                        }
                        }
                        }
                        }
                
                
    return 0
    
if __name__ == '__main__':
    app.run(debug=False,port = 80)