from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for,session 
import requests
import json
import os
import numpy
import mysql.connector
import MySQLdb
import re
import enum


app = Flask(__name__)

app.secret_key = 'super secret key'

#itemArray = {'name' : 'Soumitra', 'email' : 'soumitra@roytuts.com', 'phone' : '7896541230'}
itemArray = {'name' : 'Soumitra'}

with requests.Session() as s:
    res = s.get('https://httpbin.org/cookies/set/username/') 
    print('res: {}'.format(res.text))
    res = s.get('https://httpbin.org/cookies')
    print('res: {}'.format(res.text))
    print(s.cookies)   # <RequestsCookieJar[<Cookie abc=123 for httpbin.org/>]>
    print('actual cookies: {}'.format(s.cookies.get_dict()))  # actual cookies: {'abc': '123'}
    
with requests.Session() as s1:
    res = s1.get('https://httpbin.org/cookies/set/username/')
    print('res1: {}'.format(res.text))
    res = s1.get('https://httpbin.org/cookies')
    print('res: {}'.format(res.text))
    print(s1.cookies)   # <RequestsCookieJar[<Cookie abc=123 for httpbin.org/>]>
    print('actual cookies: {}'.format(s1.cookies.get_dict()))  # actual cookies: {'abc': '123'}    
    
@app.route('/form', methods=['POST','GET'])  
def form():
    if request.method == 'POST':
        name = request.form["Name"]
        phone = request.form["Phone"]
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='details1')  
        cur = mydb.cursor()
        query = "INSERT INTO studentdetails(name,phone) VALUES (%s,%s)"
        val = (name,phone)
        cur.execute(query, val)
        result = cur.fetchall()
        for row in result:
            print(row[0], row[1])
            print("/n")       
            
        mydb.commit()
        cur.close() 
        #session['username'] = True
        #print(session['username'])
    return "ok"  
        
@app.route('/result', methods=[ 'POST','GET'])
def result():   
    if request.method == 'POST':
        name = request.form["Name"]
        email = request.form["Email"]
        phone = request.form["Phone"]
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='details')
        cur = mydb.cursor()
        query = "INSERT INTO studentdetails(name,email,phone) VALUES (%s,%s,%s)"
        val = (name,email,phone)
        cur.execute(query, val)
        result = cur.fetchall()
        for row in result:
            print(row[0], row[1], row[2])
            print("/n")             
        mydb.commit()
        cur.close()
        #itemArray.update( [('name', name)] )
        itemArray['name'] = name
        print(itemArray['name'])
        res = s.cookies.set('username',name) 
        res1 = s1.cookies.set('username',name)
        print(res)
        print(res1)
        return 'ok'
          
@app.route('/webhook', methods=[ 'POST',"GET"])
def webhook():        
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r    

@app.route('/processRequest', methods=[ 'POST',"GET"])   
def processRequest(req):
   # session['fsubmit'] = ''
    #session['fsubmit'] = itemArray['name']
    #lobal session["fsubmit"]
    #session["fsubmit"] =""
    #fsubmit=session.get("fsubmit")
    sessionID = req.get('responseId')
    result = req.get("queryResult")                                  
    result = req.get("queryResult")                                  
    intent = result.get("intent").get('displayName') 
    query_text = result.get("queryText")                   
    parameters = result.get("parameters")   
    
    fulfillmentText = ''
    
    
    # Welcome Intent:
    if intent == "Default Welcome Intent":
        s.cookies.clear()
        s1.cookies.clear()
        return {
                        "payload": {
                        "google": {
                        "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                "textToSpeech": "Hey There 🙋‍♂️ "   
                            }
                        },
                        {
                                "simpleResponse": {
                                "textToSpeech": "How you doin?"
                            }
                        },
                        {
                                "simpleResponse": {
                                "textToSpeech":"What can I help you with?"
                            }
                        }
                        ],
                        "suggestions": [
                            
                            {   
                                "title": "College suggest"     
                            },
                            {   
                                "title": "Course suggest"
                            },
                            {   
                                "title": "Admission Information"
                            },
                            {   
                                "title": "College Comparison"
                            },
                            {   
                                "title": "Entrance Exam Details"
                            }
                        ]  
                        }
                        }
                        }
                        }
    
    #No_Intent_for_student_details:
    if intent == "No_Intent":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "You just missed it." + "\n" + "Anyway, you can reach us at +91 998767655 for further assistance.",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{                         
           "message":"submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/form"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
},
{
        "payload": {
            "message":'<iframe width="250" height="200" src="https://www.youtube.com/embed/cBRXWRJFaVc" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>' + "\n"+"https://www.youtube.com/channel/UCipkzWrLJU2H10VehqAGhcA",
            "platform": "kommunicate",
            "messageType": "html"
            }
        } 
   ]
}
  
    #Engineering college:
    if intent == "Engineering college":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Engineering Government college"
        fulfillmentText2 = "Top 10 Engineering Private colleges"
        fulfillmentText3 = "Do you have a any colleges in your mind for Engineering?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Welcome to the club Buddy 💪 "   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "Let's narrow our search "   
                            }
                        }
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillmentText2 
                    },
                    {   
                        "title": fulfillmentText3 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    if intent == "Yes_Intent_Govt_Engineering":  
        print(itemArray['name'])
        print(s.cookies.get('username'))
        print(s1.cookies.get('username'))
        if s.cookies.get('username')  == itemArray.get('name') :
            #print(session['fsubmit'])
            return {
        "fulfillmentMessages":[
        {
            "payload": {
                "message":"Form Submitted",
                "platform": "kommunicate"
            }
        }
        ]   
        }
        elif s1.cookies.get('username')  == itemArray.get('name') :
            #print(session['fsubmit'])
            return {
        "fulfillmentMessages":[
        {
            "payload": {
                "message":"Form Submitted",
                "platform": "kommunicate"
            }
        }
        ]   
        }
        else:
        #session["fsubmit"] != True:
            #session["fsubmit"] = True
            return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
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
        sql = ('select cs_college_info.cs_collegename , cs_col_nirf.cs_rank \
from cs_college_info \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
where cs_college_info.cs_col_category = "G" and cs_col_nirf.cs_rank >=1 group by cs_college_info.cs_collegename order by cs_col_nirf.cs_rank asc limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Thank you engineer! hope this is what you were looking for.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Ask for more, I'm excited to help you.",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "AreaWise Top Engineering Colleges In India",
            "message": "AreaWise Top Engineering Colleges In India"
            
        }
       ]
       
    }
         }
      }
   ]
}

# html form showed in the chatbot:
    if intent == "Yes_Intent_Prvt_Engineering":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
          
# Top 10 Engineering Private colleges in India
    if intent == "Form submitted_PVT_ENG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('select cs_college_info.cs_collegename , cs_col_nirf.cs_rank \
from cs_college_info \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
where cs_college_info.cs_col_category = "P" and cs_col_nirf.cs_rank >=1 group by cs_college_info.cs_collegename order by cs_col_nirf.cs_rank asc limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Thank you engineer! hope this is what you were looking for.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Ask for more, I'm excited to help you.",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "AreaWise Top Engineering Colleges In India",
            "message": "AreaWise Top Engineering Colleges In India"
            
        }
       ]
       
    }
         }
      }
   ]
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
                                       
                if len(college) == 5:  
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"these are the best colleges  from your favorite city.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4]) + "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                elif len(college) == 4: 
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"these are the best colleges  from your favorite city.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index2.html",value=college[0],value1=college[1],value2=college[2],value3=college[3])+ "\n" + "\n" + "Should we start from the top?👇",   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

                elif len(college) == 3:   
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"these are the best colleges  from your favorite city.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index3.html",value=college[0],value1=college[1],value2=college[2])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
                elif len(college) == 2:   
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"these are the best colleges  from your favorite city.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index4.html",value=college[0],value1=college[1])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
                elif len(college) == 1:  
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"these are the best colleges  from your favorite city.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index5.html",value=college[0])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#colleges for Engineering:
    if intent == "Do you have a any colleges in your mind for Engineering?": 
        text = parameters.get("college")
        text1=str(text)
        text2 = text1.upper()
        print(text2) 
        fulfillmentText1=''
        fulfillment2=''
        fulfillment3=''
        fulfillment4=''
        fulfillment5=''
        fulfillment6=''
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        sql =('SELECT distinct \
  cs_collegename \
  FROM cs_college_info ')
        cur.execute(sql)
        myresult = cur.fetchall()
        #print(myresult) 
        for webhook in myresult:
            college.extend(webhook) 
            
        for details in college:
            if text2 == details:
                
                mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
                cur = mydb.cursor()
                query=('SELECT distinct cs_college_info.cs_collegename,cs_col_nirf.cs_rank,cs_col_nirf.cs_score,cs_col_nirf_placements.no_of_intake,cs_col_nirf_placements.no_of_placed ,cs_col_nirf_placements.median_salary_for_placed \
FROM cs_college_info \
left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates \
left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type \
WHERE  cs_college_info.cs_collegename ="%s"' %text2)    
                cur.execute(query)
                myresult1 = cur.fetchall()
                #print(myresult1)
                for webhook1 in myresult1:
                    college1.extend(webhook1)
            #print(college1[0])        
                #fulfillmentText1 = "Basic Information"+"\n"+" College name: {name}".format(name=college1[0])
                #fulfillment2 = "NIRF rank: {name1}".format(name1=college1[1])
                #fulfillment3 = "NIRF score: {name2}".format(name2=college1[2])
                #fulfillment4 = "Intake: {name3}".format(name3=college1[3])
                #fulfillment5 = "Placed: {name4}".format(name4=college1[4])
                #fulfillment6 = "Median Salary: {name5}".format(name5=college1[5])
            return {
                        "payload": {
                        "google": {
                        "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                "textToSpeech": "NIRF rank: {}".format(college1[1])
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
        fulfillmentText3 = "Do you have a any colleges in your mind for Medical?"

        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Woohoo! Let me thank you first for the choice 🙏 "   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "You can make this world much healthier!"   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "Let me treat you for now 😎 💊"   
                            }
                        }
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillmentText2 
                    },
                    {   
                        "title": fulfillmentText3
                    }
                ]    
                }
                }
                }
                } 
                
# html form showed in the chatbot:
    if intent == "Yes_Intent_Govt_Medical":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}                
                
# Top 10 Medical Government colleges in India                 
    if intent == "Form submitted_GVT_Medical":       
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('select cs_college_info.cs_collegename , cs_col_nirf.cs_rank \
from cs_college_info \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
where cs_college_info.cs_col_category = "G" and cs_col_nirf.cs_rank >=1 group by cs_college_info.cs_collegename order by cs_col_nirf.cs_rank asc limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
        
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These are the colleges providing the best learning experience.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Ask for more, I'm excited to help you.",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "AreaWise Top Medical Colleges In India",
            "message": "AreaWise Top Medical Colleges In India"
            
        }
       ]
       
    }
         }
      }
   ]
}

# html form showed in the chatbot:
    if intent == "Yes_Intent_Prvt_Medical":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}

# Top 10 Medical Private colleges in India                 
    if intent == "Form submitted_PVT_Medical":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('select cs_college_info.cs_collegename , cs_col_nirf.cs_rank \
from cs_college_info \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
where cs_college_info.cs_col_category = "P" and cs_col_nirf.cs_rank >=1 group by cs_college_info.cs_collegename order by cs_col_nirf.cs_rank asc limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These are the colleges providing the best learning experience.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Ask for more, I'm excited to help you.",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "AreaWise Top Medical Colleges In India",
            "message": "AreaWise Top Medical Colleges In India"
            
        }
       ]
       
    }
         }
      }
   ]
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
                        
                if len(college) == 5:  
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Doc, heres the list top colleges in your city 👨‍⚕️",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4]) + "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                elif len(college) == 4: 
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Doc, heres the list top colleges in your city 👨‍⚕️",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index2.html",value=college[0],value1=college[1],value2=college[2],value3=college[3])+ "\n" + "\n" + "Should we start from the top?👇",   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

                elif len(college) == 3:   
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Doc, heres the list top colleges in your city 👨‍⚕️",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index3.html",value=college[0],value1=college[1],value2=college[2])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
                elif len(college) == 2:   
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Doc, heres the list top colleges in your city 👨‍⚕️",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index4.html",value=college[0],value1=college[1])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
                elif len(college) == 1:  
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Doc, heres the list top colleges in your city 👨‍⚕️",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index5.html",value=college[0])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
#Architecture college:
    if intent == "Architecture college":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Architecture Government college"
        fulfillmentText2 = "Top 10 Architecture Private colleges"
        fulfillmentText3 = "Do you have a any colleges in your mind for Architecture?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                 {
                       "simpleResponse": {
                       "textToSpeech": "Ok, so you're an artist ✏️, that's incredible!"   
                            }
                        },
                 {
                       "simpleResponse": {
                       "textToSpeech":"Help me narrow the results. "   
                            }
                        }         
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillmentText2 
                    },
                    {   
                        "title": fulfillmentText3
                    }
                ]    
                }
                }
                }
                } 
                
# html form showed in the chatbot:
    if intent == "Yes_Intent_Govt_Architecture":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
                
# Top 10 Architecture Government colleges in India                 
    if intent == "Form submitted_GVT_Architecture":       
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('select cs_college_info.cs_collegename , cs_col_nirf.cs_rank \
from cs_college_info \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
where cs_college_info.cs_col_category = "G" and cs_col_nirf.cs_rank >=1 group by cs_college_info.cs_collegename order by cs_col_nirf.cs_rank asc limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"The list of top colleges suiting your interest👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Ask for more, I'm excited to help you.",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "AreaWise Top Architecture Colleges In India",
            "message": "AreaWise Top Architecture Colleges In India"
            
        }
       ]
       
    }
         }
      }
   ]
}

# html form showed in the chatbot:
    if intent == "Yes_Intent_Prvt_Architecture":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}

# Top 10 Architecture Private colleges in India                 
    if intent == "Form submitted_PVT_Architecture":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('select cs_college_info.cs_collegename , cs_col_nirf.cs_rank \
from cs_college_info \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
where cs_college_info.cs_col_category = "P" and cs_col_nirf.cs_rank >=1 group by cs_college_info.cs_collegename order by cs_col_nirf.cs_rank asc limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11])    
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"The list of top colleges suiting your interest👇️",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Ask for more, I'm excited to help you.",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "AreaWise Top Architecture Colleges In India",
            "message": "AreaWise Top Architecture Colleges In India"
            
        }
       ]
       
    }
         }
      }
   ]
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
                        
                if len(college) == 5:  
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These colleges make the best architect in your favorite city. Go get a seat artist! ✌️",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                elif len(college) == 4: 
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These colleges make the best architect in your favorite city. Go get a seat artist! ✌️",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index2.html",value=college[0],value1=college[1],value2=college[2],value3=college[3])+ "\n" + "\n" + "Should we start from the top?👇",   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

                elif len(college) == 3:   
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These colleges make the best architect in your favorite city. Go get a seat artist! ✌️",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index3.html",value=college[0],value1=college[1],value2=college[2])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
                elif len(college) == 2:   
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These colleges make the best architect in your favorite city. Go get a seat artist! ✌️",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index4.html",value=college[0],value1=college[1])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
                elif len(college) == 1:  
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These colleges make the best architect in your favorite city. Go get a seat artist! ✌️",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index5.html",value=college[0])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
#Dental college:
    if intent == "Dental college":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Dental Government college"
        fulfillmentText2 = "Top 10 Dental Private colleges"
        fulfillmentText3 = "Do you have a any colleges in your mind for Dental?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "You can make this world smile 😃"    
                            }
                        },
               {
                      "simpleResponse":{
                      "textToSpeech":"Now how can I make you smile?😎😉."   
                           }
                       }
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillmentText2 
                    },
                    {   
                        "title": fulfillmentText3 
                    }
                ]    
                }
                }
                }
                } 
                
# html form showed in the chatbot:
    if intent == "Yes_Govrt_Dental":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}                
                
# Top 10 Dental Government colleges in India
    if intent == "Form submitted_GVT_Dental": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('select cs_college_info.cs_collegename , cs_col_nirf.cs_rank \
from cs_college_info \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
where cs_college_info.cs_col_category = "G" and cs_col_nirf.cs_rank >=1 group by cs_college_info.cs_collegename order by cs_col_nirf.cs_rank asc limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])     
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"They say these colleges spread smile all around 😇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Ask for more, I'm excited to help you.",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "AreaWise Top Dental Colleges In India",
            "message": "AreaWise Top Dental Colleges In India"
            
        }
       ]
       
    }
         }
      }
   ]
}

# html form showed in the chatbot:
    if intent == "Yes_Intent_pvrt_Dental":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
               
# Top 10 dental Private colleges in India
    if intent == "Form submitted_PVT_Dental": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('select cs_college_info.cs_collegename , cs_col_nirf.cs_rank \
from cs_college_info \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
where cs_college_info.cs_col_category = "P" and cs_col_nirf.cs_rank >=1 group by cs_college_info.cs_collegename order by cs_col_nirf.cs_rank asc limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"They say these colleges spread smile all around 😇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Ask for more, I'm excited to help you.",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "AreaWise Top Dental Colleges In India",
            "message": "AreaWise Top Dental Colleges In India"
            
        }
       ]
       
    }
         }
      }
   ]
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
                        
                if len(college) == 5:  
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These guys spread smiles in your favorite city.",
            "platform": "kommunicate"
        }
    },
    {
        "payload": {
            "message":"Join the mission 😃",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                elif len(college) == 4: 
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These guys spread smiles in your favorite city.",
            "platform": "kommunicate"
        }
    },
    {
        "payload": {
            "message":"Join the mission 😃",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index2.html",value=college[0],value1=college[1],value2=college[2],value3=college[3])+ "\n" + "\n" + "Should we start from the top?👇",   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

                elif len(college) == 3:   
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These guys spread smiles in your favorite city.",
            "platform": "kommunicate"
        }
    },
    {
        "payload": {
            "message":"Join the mission 😃",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index3.html",value=college[0],value1=college[1],value2=college[2])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
                elif len(college) == 2:   
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These guys spread smiles in your favorite city.",
            "platform": "kommunicate"
        }
    },
    {
        "payload": {
            "message":"Join the mission 😃",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index4.html",value=college[0],value1=college[1])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
                elif len(college) == 1:  
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These guys spread smiles in your favorite city.",
            "platform": "kommunicate"
        }
    },
    {
        "payload": {
            "message":"Join the mission 😃",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index5.html",value=college[0])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
#Pharmacy college:
    if intent == "Pharmacy college":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Pharmacy Government college"
        fulfillmentText2 = "Top 10 Pharmacy Private colleges"
        fulfillmentText3 = "Do you have a any colleges in your mind for Pharmacy?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech":"On a way to be a legal drug lord, huh?💊"   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech":"Here are some options that might interest you👇."   
                            }
                        }  
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillmentText2 
                    },
                    {   
                        "title": fulfillmentText3 
                    }
                ]    
                }
                }
                }
                } 
                
# html form showed in the chatbot:
    if intent == "Yes_Govrt_Pharmacy":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}                
                
# Top 10 Pharmacy Government colleges in India
    if intent == "Form submitted_GVT_Pharmacy": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('select cs_college_info.cs_collegename , cs_col_nirf.cs_rank \
from cs_college_info \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
where cs_college_info.cs_col_category = "G" and cs_col_nirf.cs_rank >=1 group by cs_college_info.cs_collegename order by cs_col_nirf.cs_rank asc limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"👇 👇 best colleges to choose from!!",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com"+ "\n" + "\n" + "Ask for more, I'm excited to help you.",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "AreaWise Top Pharmacy Colleges In India",
            "message": "AreaWise Top Pharmacy Colleges In India"
            
        }
       ]
       
    }
         }
      }
   ]
}

# html form showed in the chatbot:
    if intent == "Yes_Intent_pvrt_Pharmacy":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
               
# Top 10 Pharmacy Private colleges in India
    if intent == "Form submitted_PVT_Pharmacy": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('select cs_college_info.cs_collegename , cs_col_nirf.cs_rank \
from cs_college_info \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
where cs_college_info.cs_col_category = "P" and cs_col_nirf.cs_rank >=1 group by cs_college_info.cs_collegename order by cs_col_nirf.cs_rank asc limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"👇 👇 best colleges to choose from!!",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com"+ "\n" + "\n" + "Ask for more, I'm excited to help you.",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "AreaWise Top Pharmacy Colleges In India",
            "message": "AreaWise Top Pharmacy Colleges In India"
            
        }
       ]
       
    }
         }
      }
   ]
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
                        
                if len(college) == 5:  
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These guys deal with drugs in your city.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                elif len(college) == 4: 
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These guys deal with drugs in your city.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index2.html",value=college[0],value1=college[1],value2=college[2],value3=college[3])+ "\n" + "\n" + "Should we start from the top?👇",   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                elif len(college) == 3:   
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These guys deal with drugs in your city.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index3.html",value=college[0],value1=college[1],value2=college[2])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}                      
                elif len(college) == 2:   
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These guys deal with drugs in your city.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index4.html",value=college[0],value1=college[1])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}                           
                elif len(college) == 1:  
                    return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These guys deal with drugs in your city.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("index5.html",value=college[0])+ "\n" + "\n" + "Should we start from the top?👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#COURSE SUGGEST:
#UG courses:
    #Engineering courses UG:
    if intent == "Engineering courses":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Engineering 👨🏽‍🎓 Trending courses"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Welcome to the club Buddy 💪 "   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "Let's narrow our search "   
                            }
                        }
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    if intent == "Yes_Engineering_UG":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
             
   # Top 10 Engineering Trending courses_UG in India                 
    if intent == "Form_submitted_Eng_Courses_UG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT distinct \
  cs_courselists.cs_coursename \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        #fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"🎼🎼 we will never go out trend 🎼🎼",
            "platform": "kommunicate"
        }
    },
    {
        "payload": {
            "message":"Here the most trending courses you could pursue!!",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":"choose one 👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[377],
            "message": college[377]
            
        },
        {
            "title": college[378],
            "message": college[378]
            
        },
        {
            "title": college[376],
            "message": college[376]
            
        },
        {
            "title": college[375],
            "message": college[375]
            
        },
        {
            "title": college[374],
            "message": college[374]
            
        },
        {
            "title": college[373],
            "message": college[373]
            
        },
        {
            "title": college[367],
            "message": college[367]
            
        },
        {
            "title": college[366],
            "message": college[366]
            
        },
        {
            "title": college[365],
            "message": college[365]
            
        },
        {
            "title": college[364],
            "message": college[364]
            
        }
       ]
       
    }
         }
      }
   ]
}

# UG Engineering Trending course with colleges:
#Information Technology with Specialization in Cloud Technology and Information Security_UG
    if intent == "Information_Technology_with Specialization_in Cloud Technology and Information Security_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[447]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1 and cs_courselists.cs_sno = {city} limit 5'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#CSE with specialization in Network SecurityUG
    if intent == "CSE with specialization in Network Security_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[448]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1 and cs_courselists.cs_sno = {city} limit 5'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#CSE with specialization in Web Technology_UG
    if intent == "CSE with specialization in Web Technology_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[446]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1 and cs_courselists.cs_sno = {city} limit 5'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#CSE with specialization in IoT& Cyber Security_UG
    if intent == "CSE with specialization in IoT& Cyber Security_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[445]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1 and cs_courselists.cs_sno = {city} limit 5'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#CSE with specialization in AI & Machine Learning_UG
    if intent == "CSE with specialization in AI & Machine Learning_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[444]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1 and cs_courselists.cs_sno = {city} limit 5'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#Manufacturing Process and Automation Engineering_UG
    if intent == "Manufacturing Process and Automation Engineering_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[443]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1 and cs_courselists.cs_sno = {city} limit 5'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#Computer Science and Engineering (Artificial Intelligence)_UG
    if intent == "Computer Science and Engineering (Artificial Intelligence)_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[435]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1 and cs_courselists.cs_sno = {city} limit 5'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#Chemical Technology with Specialization in Paint Technology_UG
    if intent == "Chemical Technology with Specialization in Paint Technology_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[434]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1 and cs_courselists.cs_sno = {city} limit 5'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#Chemical Technology with Specialization in Plastic Technology_UG
    if intent == "Chemical Technology with Specialization in Plastic Technology_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[433]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1 and cs_courselists.cs_sno = {city} limit 5'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#Chemical Technology with Specialization in Leather Technology_UG
    if intent == "Chemical Technology with Specialization in Leather Technology_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[432]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1 and cs_courselists.cs_sno = {city} limit 5'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
#Medical courses UG:
    if intent == "Medical courses":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Medical 👨🏾‍⚕️ Trending courses"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Woohoo! Let me thank you first for the choice 🙏 "   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "You can make this world much healthier!"   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "Let me treat you for now 😎 💊"   
                            }
                        }
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    if intent == "Yes_Medical_UG":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
             
   # Top 10 medical Trending courses_UG in India                 
    if intent == "Form_submitted_Medical_courses_UG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT \
 cs_courselists.cs_coursename \
  FROM cs_trending_courses \
  left JOIN cs_courselists ON cs_trending_courses.course_id = cs_courselists.cs_sno\
  where cs_trending_courses.degree_type_id = 1')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Lets go with the trend! Here's the list of what you asked for 👇👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com"  + "\n" + "Let's get deeper 👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[0],
            "message": college[0]
            
        },
        {
            "title": college[1],
            "message": college[1]
            
        },
        {
            "title": college[2],
            "message": college[2]
            
        },
        {
            "title": college[3],
            "message": college[3]
            
        },
        {
            "title": college[4],
            "message": college[4]
            
        },
        {
            "title": college[5],
            "message": college[5]
            
        },
        {
            "title": college[6],
            "message": college[6]
            
        },
        {
            "title": college[7],
            "message": college[7]
            
        },
        {
            "title": college[8],
            "message": college[8]
            
        },
        {
            "title": college[9],
            "message": college[9]
            
        }
       ]
       
    }
         }
      }
   ]
}

#Architecture courses UG:
    if intent == "Architecture courses":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Architecture 👨🏾‍🎓 Trending courses"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Ok, so you're an artist ✏️, that's incredible!"   
                            }
                        },
                 {
                       "simpleResponse": {
                       "textToSpeech":"Help me narrow the results. "   
                            }
                        }    
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    if intent == "Yes_architecture_UG":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
             
   # Top 10 Architecture Trending courses_UG in India                 
    if intent == "Form_submitted_Architecture_courses_UG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT \
 cs_courselists.cs_coursename \
  FROM cs_trending_courses \
  left JOIN cs_courselists ON cs_trending_courses.course_id = cs_courselists.cs_sno\
  where cs_trending_courses.degree_type_id = 1')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Even courses are fancy now. Like your dreams🎨. Here are some👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Choose one👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[0],
            "message": college[0]
            
        },
        {
            "title": college[1],
            "message": college[1]
            
        },
        {
            "title": college[2],
            "message": college[2]
            
        },
        {
            "title": college[3],
            "message": college[3]
            
        },
        {
            "title": college[4],
            "message": college[4]
            
        },
        {
            "title": college[5],
            "message": college[5]
            
        },
        {
            "title": college[6],
            "message": college[6]
            
        },
        {
            "title": college[7],
            "message": college[7]
            
        },
        {
            "title": college[8],
            "message": college[8]
            
        },
        {
            "title": college[9],
            "message": college[9]
            
        }
       ]
       
    }
         }
      }
   ]
}

#Dental courses UG:
    if intent == "Dental courses":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Dental 👨🏾‍⚕️ Trending courses"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "You can make this world smile 😃"    
                            }
                        },
               {
                      "simpleResponse":{
                      "textToSpeech":"Now how can I make you smile?😎😉."   
                           }
                       }
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    if intent == "Yes_dental_UG":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
             
   # Top 10 Dental Trending courses_UG in India                 
    if intent == "Form_submitted_Dental_courses_UG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT \
 cs_courselists.cs_coursename \
  FROM cs_trending_courses \
  left JOIN cs_courselists ON cs_trending_courses.course_id = cs_courselists.cs_sno\
  where cs_trending_courses.degree_type_id = 1')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"All these trending courses are smiling at you🤓 which one would you pick?",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Choose one👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[0],
            "message": college[0]
            
        },
        {
            "title": college[1],
            "message": college[1]
            
        },
        {
            "title": college[2],
            "message": college[2]
            
        },
        {
            "title": college[3],
            "message": college[3]
            
        },
        {
            "title": college[4],
            "message": college[4]
            
        },
        {
            "title": college[5],
            "message": college[5]
            
        },
        {
            "title": college[6],
            "message": college[6]
            
        },
        {
            "title": college[7],
            "message": college[7]
            
        },
        {
            "title": college[8],
            "message": college[8]
            
        },
        {
            "title": college[9],
            "message": college[9]
            
        }
       ]
       
    }
         }
      }
   ]
}

#Pharmacy courses UG:
    if intent == "Pharmacy courses":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Pharmacy 👨🏾‍⚕️ Trending courses"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                 {
                       "simpleResponse": {
                       "textToSpeech":"On a way to be a legal drug lord, huh?💊"   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech":"Here are some options that might interest you👇."   
                            }
                        }  
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    if intent == "Yes_pharmacy_UG":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
             
   # Top 10 Pharmacy Trending courses_UG in India                 
    if intent == "Form_submitted_Pharmacy_courses_UG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT \
 cs_courselists.cs_coursename \
  FROM cs_trending_courses \
  left JOIN cs_courselists ON cs_trending_courses.course_id = cs_courselists.cs_sno\
  where cs_trending_courses.degree_type_id = 1')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Now there are trendy ways to save the world 🌍, strange isn't? Take a look at this 👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Choose one👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[0],
            "message": college[0]
            
        },
        {
            "title": college[1],
            "message": college[1]
            
        },
        {
            "title": college[2],
            "message": college[2]
            
        },
        {
            "title": college[3],
            "message": college[3]
            
        },
        {
            "title": college[4],
            "message": college[4]
            
        },
        {
            "title": college[5],
            "message": college[5]
            
        },
        {
            "title": college[6],
            "message": college[6]
            
        },
        {
            "title": college[7],
            "message": college[7]
            
        },
        {
            "title": college[8],
            "message": college[8]
            
        },
        {
            "title": college[9],
            "message": college[9]
            
        }
       ]
       
    }
         }
      }
   ]
}

#PG courses:
    #Engineering courses PG:
    if intent == "Engineering courses_PG":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Engineering 👨🏽‍🎓 Trending courses"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Welcome to the club Buddy 💪 "   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "Let's narrow our search "   
                            }
                        }
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    if intent == "Yes_Engineering_PG":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
             
   # Top 10 Engineering Trending courses_PG in India                 
    if intent == "Form_submitted_Engineering_courses_PG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT distinct \
  cs_courselists.cs_coursename \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        #fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"🎼🎼 we will never go out trend 🎼🎼",
            "platform": "kommunicate"
        }
    },
    {
        "payload": {
            "message":"Here the most trending courses you could pursue!!",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":"choose one 👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[967],
            "message": college[967]
            
        },
        {
            "title": college[966],
            "message": college[966]
            
        },
        {
            "title": college[965],
            "message": college[965]
            
        },
        {
            "title": college[963],
            "message": college[963]
            
        },
        {
            "title": college[958],
            "message": college[958]
            
        },
        {
            "title": college[957],
            "message": college[957]
            
        },
        {
            "title": college[956],
            "message": college[956]
            
        },
        {
            "title": college[936],
            "message": college[936]
            
        },
        {
            "title": college[928],
            "message": college[928]
            
        },
        {
            "title": college[927],
            "message": college[927]
            
        }
       ]
       
    }
         }
      }
   ]
}

# PG Engineering Trending course with colleges:
#Electronics and Telecommunication specilization with Communication Network_PG
    if intent == "Electronics and Telecommunication specilization with Communication Network_PG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1081]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city} limit 10'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#Civil Engg. with specialization in Infrastructure Engineering & Management_PG
    if intent == "Civil Engg. with specialization in Infrastructure Engineering & Management_PG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1080]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city} limit 10'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#Electrical Engg. with pecialization in Power System_PG
    if intent == "Electrical Engg. with pecialization in Power System_PG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1079]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city} limit 10'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#CSE with M.Tech specialization in Information Technology_PG
    if intent == "CSE with M.Tech specialization in Information Technology_PG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1077]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city} limit 10'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#ECE with Specialization in  Communication & Signal Processing_PG
    if intent == "ECE with Specialization in  Communication & Signal Processing_PG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1072]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city} limit 10'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#ECE with M.Tech Specialization in Power and Control_PG
    if intent == "ECE with M.Tech Specialization in Power and Control_PG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1071]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city} limit 10'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#ECE with M.Tech Specialization in Microwave and Communication Engineering_PG
    if intent == "ECE with M.Tech Specialization in Microwave and Communication Engineering_PG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1070]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city} limit 10'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#Wireless Networks & Applications (Specialising in IoT, AI, 5G, Blockchain)_PG
    if intent == "Wireless Networks & Applications (Specialising in IoT, AI, 5G, Blockchain)_PG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1041]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city} limit 10'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#CSE – Full Stack with Virtusa_PG
    if intent == "CSE – Full Stack with Virtusa_PG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1033]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city} limit 10'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#Chemical Technology with Specialization in Biochemical Engineering_PG
    if intent == "Chemical Technology with Specialization in Biochemical Engineering_PG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courses_nw.course_id \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1032]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city} limit 10'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) == 5:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3],value4=college1[4]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
        elif len(college1) == 4: 
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges1.html",value=college1[0],value1=college1[1],value2=college1[2],value3=college1[3]),   
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

        elif len(college1) == 3:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges2.html",value=college1[0],value1=college1[1],value2=college1[2]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                        
        elif len(college1) == 2:   
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges3.html",value=college1[0],value1=college1[1]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}
                            
        elif len(college1) == 1:  
            return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trendingcolleges4.html",value=college1[0]),
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"
            
        }
       ]
       
    }
         }
      }
   ]
}

#Medical courses PG:
    if intent == "Medical courses_PG":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Medical 👨🏾‍⚕️ Trending courses"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Woohoo! Let me thank you first for the choice 🙏 "   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "You can make this world much healthier!"   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "Let me treat you for now 😎 💊"   
                            }
                        }
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    if intent == "Yes_medical_PG":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
             
   # Top 10 medical Trending courses_PG in India                 
    if intent == "Form_submitted_Medical_courses_PG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT \
 cs_courselists.cs_coursename \
  FROM cs_trending_courses \
  left JOIN cs_courselists ON cs_trending_courses.course_id = cs_courselists.cs_sno\
  where cs_trending_courses.degree_type_id = 2')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Lets go with the trend! Here's the list of what you asked for 👇👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Let's get deeper 👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[0],
            "message": college[0]
            
        },
        {
            "title": college[1],
            "message": college[1]
            
        },
        {
            "title": college[2],
            "message": college[2]
            
        },
        {
            "title": college[3],
            "message": college[3]
            
        },
        {
            "title": college[4],
            "message": college[4]
            
        },
        {
            "title": college[5],
            "message": college[5]
            
        },
        {
            "title": college[6],
            "message": college[6]
            
        },
        {
            "title": college[7],
            "message": college[7]
            
        },
        {
            "title": college[8],
            "message": college[8]
            
        },
        {
            "title": college[9],
            "message": college[9]
            
        }
       ]
       
    }
         }
      }
   ]
}

#Architecture courses PG:
    if intent == "Architecture courses_PG":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Architecture 👨🏾‍🎓 Trending courses"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Ok, so you're an artist ✏️, that's incredible!"   
                            }
                        },
                 {
                       "simpleResponse": {
                       "textToSpeech":"Help me narrow the results. "   
                            }
                        }    
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    if intent == "Yes_architecture_PG":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
             
   # Top 10 Architecture Trending courses_PG in India                 
    if intent == "Form_submitted_Architecture_courses_PG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT \
 cs_courselists.cs_coursename \
  FROM cs_trending_courses \
  left JOIN cs_courselists ON cs_trending_courses.course_id = cs_courselists.cs_sno\
  where cs_trending_courses.degree_type_id = 2')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Even courses are fancy now. Like your dreams🎨. Here are some👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Choose one👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[0],
            "message": college[0]
            
        },
        {
            "title": college[1],
            "message": college[1]
            
        },
        {
            "title": college[2],
            "message": college[2]
            
        },
        {
            "title": college[3],
            "message": college[3]
            
        },
        {
            "title": college[4],
            "message": college[4]
            
        },
        {
            "title": college[5],
            "message": college[5]
            
        },
        {
            "title": college[6],
            "message": college[6]
            
        },
        {
            "title": college[7],
            "message": college[7]
            
        },
        {
            "title": college[8],
            "message": college[8]
            
        },
        {
            "title": college[9],
            "message": college[9]
            
        }
       ]
       
    }
         }
      }
   ]
}

#Dental courses PG:
    if intent == "Dental courses_PG":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Dental 👨🏾‍⚕️ Trending courses"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "You can make this world smile 😃"    
                            }
                        },
               {
                      "simpleResponse":{
                      "textToSpeech":"Now how can I make you smile?😎😉."   
                           }
                       }       
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    if intent == "Yes_dental_PG":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
             
   # Top 10 Dental Trending courses_PG in India                 
    if intent == "Form_submitted_Dental_courses_PG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT \
 cs_courselists.cs_coursename \
  FROM cs_trending_courses \
  left JOIN cs_courselists ON cs_trending_courses.course_id = cs_courselists.cs_sno\
  where cs_trending_courses.degree_type_id = 2')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"All these trending courses are smiling at you🤓 which one would you pick?",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Choose one👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[0],
            "message": college[0]
            
        },
        {
            "title": college[1],
            "message": college[1]
            
        },
        {
            "title": college[2],
            "message": college[2]
            
        },
        {
            "title": college[3],
            "message": college[3]
            
        },
        {
            "title": college[4],
            "message": college[4]
            
        },
        {
            "title": college[5],
            "message": college[5]
            
        },
        {
            "title": college[6],
            "message": college[6]
            
        },
        {
            "title": college[7],
            "message": college[7]
            
        },
        {
            "title": college[8],
            "message": college[8]
            
        },
        {
            "title": college[9],
            "message": college[9]
            
        }
       ]
       
    }
         }
      }
   ]
}

#Pharmacy courses PG:
    if intent == "Pharmacy courses_PG":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Pharmacy 👨🏾‍⚕️ Trending courses"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech":"On a way to be a legal drug lord, huh?💊"   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech":"Here are some options that might interest you👇."   
                            }
                        }  
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    if intent == "Yes_pharmacy_PG":
        return {
   "fulfillmentMessages":[
    {
         "payload":{
  "message": "Lets proceed. Here's your form, please fill it",
  "platform": "kommunicate",
  "metadata": {
    "contentType": "300",
    "templateId": "12",
    "payload": [
      {
        "type": "text",
        "data": {
          "label": "Name",
          "placeholder": "Enter your name",
           "validation": {
            "regex": "[A-Za-z0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Email",
          "placeholder": "Enter your email",
          "validation": {
          "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$",
          "errorText": "Invalid Email"
        }
        }
      },
      {
        "type": "text",
        "data": {
          "label": "Phone",
          "placeholder": "Enter your phone",
          "validation": {
            "regex": "[0-9]",
            "errorText": "Field is mandatory"
          }
        }
      },
      {
        "type": "submit",
        "data": {
          "action":{
            "message": "Form Submitted",
            "requestType": "POST",
            "formAction": "https://18668f55f593.ngrok.io/result"
          },
          "type": "submit",
          "name": "Submit"
        }
      }
    ]
  }
}
}
   ]
}
             
   # Top 10 Pharmacy Trending courses_PG in India                 
    if intent == "Form_submitted_Pharmacy_courses_PG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT \
 cs_courselists.cs_coursename \
  FROM cs_trending_courses \
  left JOIN cs_courselists ON cs_trending_courses.course_id = cs_courselists.cs_sno\
  where cs_trending_courses.degree_type_id = 2')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Now there are trendy ways to save the world 🌍, strange isn't? Take a look at this 👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com" + "\n" + "\n" + "Choose one👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[0],
            "message": college[0]
            
        },
        {
            "title": college[1],
            "message": college[1]
            
        },
        {
            "title": college[2],
            "message": college[2]
            
        },
        {
            "title": college[3],
            "message": college[3]
            
        },
        {
            "title": college[4],
            "message": college[4]
            
        },
        {
            "title": college[5],
            "message": college[5]
            
        },
        {
            "title": college[6],
            "message": college[6]
            
        },
        {
            "title": college[7],
            "message": college[7]
            
        },
        {
            "title": college[8],
            "message": college[8]
            
        },
        {
            "title": college[9],
            "message": college[9]
            
        }
       ]
       
    }
         }
      }
   ]
}


                               
    return 0
    
if __name__ == '__main__':
    app.run(debug=False,port = 80)