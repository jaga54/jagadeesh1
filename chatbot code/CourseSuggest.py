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
    return "ok"

@app.route('/testing', methods=['GET', 'POST'])
def testing():
    if request.method == "POST" :
        if request.json["inst_no"]:
            data = request.json["inst_no"]
        #data1 = request.json["inst_name"]
            print(data)
        #print(data1)
            d=[]
            col12=[]
            col23=[]
            college=[]
            mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
            cur = mydb.cursor() 
        #Jossa college type
            cur.execute('SELECT distinct  josaa_college.j_sno  FROM josaa_ranking \
		left join josaa_col_category on josaa_ranking.j_category = josaa_col_category.j_sno \
		left join josaa_college on josaa_ranking.j_college = josaa_college.j_sno \
		WHERE josaa_col_category.j_col_category  = "%s"' %data)
        
            college1 = cur.fetchall()
            for i in college1:
                col12.extend(i)
        #print(col12)
            cur.execute('SELECT distinct  josaa_college.j_col_name  FROM josaa_ranking \
		left join josaa_col_category on josaa_ranking.j_category = josaa_col_category.j_sno \
		left join josaa_college on josaa_ranking.j_college = josaa_college.j_sno \
		WHERE josaa_col_category.j_col_category  = "%s"' %data)
            college2 = cur.fetchall() 
            for i in college2:
                col23.extend(i)  
        #print(col23)     

            i =0 
            final ='<option value="">SELECT</option>'
            l = len(col12) 
            while i<l:
                attach ='<option value="{no}">{college}</option>'.format(no=col12[i],college=col23[i])
                final = final+'\n' + attach
            #print(final)
                i=i+1   
            return (final)        
    
@app.route('/test', methods=['GET', 'POST'])
def test(): 
    if request.method == "POST" and request.json["inst_name"]:
        #data1 = request.json["inst_no"]
        data2 = request.json["inst_name"]
        print(data2)
        col88=[]
        col55=[]
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor() 
        #Jossa college name
        cur.execute('SELECT distinct josaa_course.j_sno  FROM josaa_ranking \
		left join josaa_round on josaa_ranking.j_round = josaa_round.j_sno \
		left join josaa_col_category on josaa_ranking.j_category = josaa_col_category.j_sno \
		left join josaa_college on josaa_ranking.j_college = josaa_college.j_sno \
		left join josaa_course on josaa_ranking.j_acedemic = josaa_course.j_sno \
		WHERE josaa_college.j_sno ="%s" '%data2)
        college1 = cur.fetchall()
        for i in college1:
            col88.extend(i)
        #print(col88)
        cur.execute('SELECT distinct josaa_course.j_course  FROM josaa_ranking \
		left join josaa_round on josaa_ranking.j_round = josaa_round.j_sno \
		left join josaa_col_category on josaa_ranking.j_category = josaa_col_category.j_sno \
		left join josaa_college on josaa_ranking.j_college = josaa_college.j_sno \
		left join josaa_course on josaa_ranking.j_acedemic = josaa_course.j_sno \
		WHERE josaa_college.j_sno ="%s" '%data2)
        college2 = cur.fetchall() 
        for i in college2:
            col55.extend(i)  
        #print(col55)     
        i =0 
        final ='<option value="">SELECT</option>'
        l = len(col88) 
        while i<l:
            attach ='<option value="{no}">{college}</option>'.format(no=col88[i],college=col55[i])
            final = final+'\n' + attach
            #print(final)
            i=i+1   
        return (final)     
    
def processRequest(req):
    sessionID = req.get('responseId')
    result = req.get("queryResult")                                  
    result = req.get("queryResult")                                  
    intent = result.get("intent").get('displayName') 
    query_text = result.get("queryText")                   
    parameters = result.get("parameters")   
    
    fulfillmentText = ''
    
    
    # Welcome Intent:
    if intent == "Default Welcome Intent":
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
                                "title": "Suggest a College"     
                            },
                            {   
                                "title": "Suggest a Course"
                            },
                            {   
                                "title": "I want to know more about Admission Information"
                            },
                            {   
                                "title": "Compare colleges"
                            },
                            {   
                                "title": "Popular Entrance Exam"
                            }
                        ]  
                        }
                        }
                        }
                        }
                        
# Main_Menu Intent:
    elif intent == "Main_Menu":
        return {
                        "payload": {
                        "google": {
                        "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                "textToSpeech": "Here we go again. "   
                            }
                        },
                        {
                                "simpleResponse": {
                                "textToSpeech": "Let's start over🧐"
                            }
                        }
                        ],
                        "suggestions": [
                            
                            {   
                                "title": "Suggest a College"     
                            },
                            {   
                                "title": "Suggest a Course"
                            },
                            {   
                                "title": "I want to know more about Admission Information"
                            },
                            {   
                                "title": "Compare colleges"
                            },
                            {   
                                "title": "Popular Entrance Exam"
                            }
                        ]  
                        }
                        }
                        }
                        }
    
# Josaa_cutoff Intent:
    elif intent == "Josaa_cutoff":
        c=[]
        d=[]
        e=[]
        f=[]
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        # josaa round
        cur.execute("SELECT distinct josaa_round.j_round FROM josaa_ranking \
						left join josaa_round on josaa_ranking.j_round = josaa_round.j_sno")
        rounds = cur.fetchall()
        for i in rounds:
            c.extend(i)
        
        #Jossa college type
        cur.execute("SELECT distinct  josaa_col_category.j_col_category FROM josaa_ranking \
    left join josaa_col_category on josaa_ranking.j_category = josaa_col_category.j_sno LIMIT 4")
        rounds12 = cur.fetchall()
        for i in rounds12:
            d.extend(i)
        
        #Jossa college name
        cur.execute("SELECT distinct  josaa_college.j_col_name  FROM josaa_ranking \
    left join josaa_college on josaa_ranking.j_college = josaa_college.j_sno")
        rounds13 = cur.fetchall()
        for i in rounds13:
            e.extend(i)   

        #Jossa Academic program
        cur.execute("SELECT distinct josaa_course.j_course  FROM josaa_ranking \
    left join josaa_course on josaa_ranking.j_acedemic = josaa_course.j_sno")
        rounds14 = cur.fetchall()
        for i in rounds14:
            f.extend(i)  
            
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
            "message":render_template("josaa.html", c =  c, d=d, e=e, f=f),
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

    
#No_Intent_for_student_details:
    elif intent == "No_Intent":
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
            "formAction": "https://cc80d242f398.ngrok.io/form"
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
    elif intent == "Engineering college":
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
    elif intent == "Yes_Intent_Govt_Engineering":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form submitted_GVT_ENG": 
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
    elif intent == "Yes_Intent_Prvt_Engineering":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form submitted_PVT_ENG": 
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
    elif intent == "AreaWise Top Engineering Colleges In India":
        city = parameters.get("city") 
        city = str(city)
        print(city)
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
    elif intent == "Do you have a any colleges in your mind for Engineering?":  
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        sql =('SELECT distinct \
  cs_collegename \
  FROM cs_college_info ')
        cur.execute(sql)    
        myresult = cur.fetchall()
        #print(myresult) 
        for webhook in myresult:
            college.extend(webhook) 
            
        for details in college:
            if city == details:
                college1 = []
                mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
                cur = mydb.cursor()
                sql1=('SELECT distinct cs_college_info.cs_collegename,cs_col_nirf.cs_rank,cs_col_nirf.cs_score,cs_col_nirf_placements.no_of_intake,cs_col_nirf_placements.no_of_placed ,cs_col_nirf_placements.median_salary_for_placed \
FROM cs_college_info \
left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates \
left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type \
WHERE  cs_college_info.cs_collegename ="%s"' %city)    
                cur.execute(sql1)
                myresult1 = cur.fetchall()
                #print(myresult1)
                for webhook1 in myresult1:
                    college1.extend(webhook1)
            #print(college1[0])        
                fulfillmentText1 = "Basic Information"+"\n"+"College name: {name}".format(name=college1[0])
                fulfillment2 = "NIRF rank: {name1}".format(name1=college1[1])
                fulfillment3 = "NIRF score: {name2}".format(name2=college1[2])
                fulfillment4 = "Intake: {name3}".format(name3=college1[3])
                fulfillment5 = "Placed: {name4}".format(name4=college1[4])
                fulfillment6 = "Median Salary: {name5}".format(name5=college1[5])
                return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Yeah! We got it😎",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentText1+"\n"+fulfillment2+"\n"+fulfillment3+"\n"+fulfillment4+"\n"+fulfillment5+"\n"+fulfillment6,
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
         {
            "title": "Main Menu",
            "message": "Main Menu"   
        },
        {
            "title": "Josaa cutoff",
            "message": "Josaa cutoff"   
        }
       ]
       
    }
         }
      }
   ]
}                      
                    
 # Medical college:
    elif intent == "Medical college":
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
    elif intent == "Yes_Intent_Govt_Medical":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form submitted_GVT_Medical":       
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
    elif intent == "Yes_Intent_Prvt_Medical":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form submitted_PVT_Medical":
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
    elif intent == "AreaWise Top Medical Colleges In India":
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

#colleges for Medical:
    elif intent == "Do you have a any colleges in your mind for Medical?":  
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        sql =('SELECT distinct \
  cs_collegename \
  FROM cs_college_info ')
        cur.execute(sql)
        myresult = cur.fetchall()
        #print(myresult) 
        for webhook in myresult:
            college.extend(webhook) 
            
        for details in college:
            if city == details:
                college1 = []
                mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
                cur = mydb.cursor()
                sql1=('SELECT distinct cs_college_info.cs_collegename,cs_col_nirf.cs_rank,cs_col_nirf.cs_score,cs_col_nirf_placements.no_of_intake,cs_col_nirf_placements.no_of_placed ,cs_col_nirf_placements.median_salary_for_placed \
FROM cs_college_info \
left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates \
left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type \
WHERE  cs_college_info.cs_collegename ="%s"' %city)    
                cur.execute(sql1)
                myresult1 = cur.fetchall()
                #print(myresult1)
                for webhook1 in myresult1:
                    college1.extend(webhook1)
            #print(college1[0])        
                fulfillmentText1 = "Basic Information"+"\n"+"College name: {name}".format(name=college1[0])
                fulfillment2 = "NIRF rank: {name1}".format(name1=college1[1])
                fulfillment3 = "NIRF score: {name2}".format(name2=college1[2])
                fulfillment4 = "Intake: {name3}".format(name3=college1[3])
                fulfillment5 = "Placed: {name4}".format(name4=college1[4])
                fulfillment6 = "Median Salary: {name5}".format(name5=college1[5])
                return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Yeah! We got it😎",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentText1+"\n"+fulfillment2+"\n"+fulfillment3+"\n"+fulfillment4+"\n"+fulfillment5+"\n"+fulfillment6,
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
    elif intent == "Architecture college":
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
    elif intent == "Yes_Intent_Govt_Architecture":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form submitted_GVT_Architecture":       
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
    elif intent == "Yes_Intent_Prvt_Architecture":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form submitted_PVT_Architecture":
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
    elif intent == "AreaWise Top Architecture Colleges In India":
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

#colleges for Architecture:
    elif intent == "Do you have a any colleges in your mind for Architecture?":  
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        sql =('SELECT distinct \
  cs_collegename \
  FROM cs_college_info ')
        cur.execute(sql)
        myresult = cur.fetchall()
        #print(myresult) 
        for webhook in myresult:
            college.extend(webhook) 
            
        for details in college:
            if city == details:
                college1 = []
                mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
                cur = mydb.cursor()
                sql1=('SELECT distinct cs_college_info.cs_collegename,cs_col_nirf.cs_rank,cs_col_nirf.cs_score,cs_col_nirf_placements.no_of_intake,cs_col_nirf_placements.no_of_placed ,cs_col_nirf_placements.median_salary_for_placed \
FROM cs_college_info \
left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates \
left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type \
WHERE  cs_college_info.cs_collegename ="%s"' %city)    
                cur.execute(sql1)
                myresult1 = cur.fetchall()
                #print(myresult1)
                for webhook1 in myresult1:
                    college1.extend(webhook1)
            #print(college1[0])        
                fulfillmentText1 = "Basic Information"+"\n"+"College name: {name}".format(name=college1[0])
                fulfillment2 = "NIRF rank: {name1}".format(name1=college1[1])
                fulfillment3 = "NIRF score: {name2}".format(name2=college1[2])
                fulfillment4 = "Intake: {name3}".format(name3=college1[3])
                fulfillment5 = "Placed: {name4}".format(name4=college1[4])
                fulfillment6 = "Median Salary: {name5}".format(name5=college1[5])
                return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Yeah! We got it😎",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentText1+"\n"+fulfillment2+"\n"+fulfillment3+"\n"+fulfillment4+"\n"+fulfillment5+"\n"+fulfillment6,
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
    elif intent == "Dental college":
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
    elif intent == "Yes_Govrt_Dental":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form submitted_GVT_Dental": 
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
    elif intent == "Yes_Intent_pvrt_Dental":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form submitted_PVT_Dental": 
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
    elif intent == "AreaWise Top Dental Colleges In India":
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
#colleges for Dental:
    elif intent == "Do you have a any colleges in your mind for Dental?":  
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        sql =('SELECT distinct \
  cs_collegename \
  FROM cs_college_info ')
        cur.execute(sql)
        myresult = cur.fetchall()
        #print(myresult) 
        for webhook in myresult:
            college.extend(webhook) 
            
        for details in college:
            if city == details:
                college1 = []
                mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
                cur = mydb.cursor()
                sql1=('SELECT distinct cs_college_info.cs_collegename,cs_col_nirf.cs_rank,cs_col_nirf.cs_score,cs_col_nirf_placements.no_of_intake,cs_col_nirf_placements.no_of_placed ,cs_col_nirf_placements.median_salary_for_placed \
FROM cs_college_info \
left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates \
left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type \
WHERE  cs_college_info.cs_collegename ="%s"' %city)    
                cur.execute(sql1)
                myresult1 = cur.fetchall()
                #print(myresult1)
                for webhook1 in myresult1:
                    college1.extend(webhook1)
            #print(college1[0])        
                fulfillmentText1 = "Basic Information"+"\n"+"College name: {name}".format(name=college1[0])
                fulfillment2 = "NIRF rank: {name1}".format(name1=college1[1])
                fulfillment3 = "NIRF score: {name2}".format(name2=college1[2])
                fulfillment4 = "Intake: {name3}".format(name3=college1[3])
                fulfillment5 = "Placed: {name4}".format(name4=college1[4])
                fulfillment6 = "Median Salary: {name5}".format(name5=college1[5])
                return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Yeah! We got it😎",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentText1+"\n"+fulfillment2+"\n"+fulfillment3+"\n"+fulfillment4+"\n"+fulfillment5+"\n"+fulfillment6,
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
    elif intent == "Pharmacy college":
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
    elif intent == "Yes_Govrt_Pharmacy":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form submitted_GVT_Pharmacy": 
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
    elif intent == "Yes_Intent_pvrt_Pharmacy":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form submitted_PVT_Pharmacy": 
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
    elif intent == "AreaWise Top Pharmacy Colleges In India":
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
#colleges for Pharmacy:
    elif intent == "Do you have a any colleges in your mind for Pharmacy?":  
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
        cur = mydb.cursor()
        college = []
        sql =('SELECT distinct \
  cs_collegename \
  FROM cs_college_info ')
        cur.execute(sql)
        myresult = cur.fetchall()
        #print(myresult) 
        for webhook in myresult:
            college.extend(webhook) 
            
        for details in college:
            if city == details:
                college1 = []
                mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
                cur = mydb.cursor()
                sql1=('SELECT distinct cs_college_info.cs_collegename,cs_col_nirf.cs_rank,cs_col_nirf.cs_score,cs_col_nirf_placements.no_of_intake,cs_col_nirf_placements.no_of_placed ,cs_col_nirf_placements.median_salary_for_placed \
FROM cs_college_info \
left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id \
left join cs_col_nirf on cs_college_info.cs_sno = cs_col_nirf.cs_college \
left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates \
left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type \
WHERE  cs_college_info.cs_collegename ="%s"' %city)    
                cur.execute(sql1)
                myresult1 = cur.fetchall()
                #print(myresult1)
                for webhook1 in myresult1:
                    college1.extend(webhook1)
            #print(college1[0])        
                fulfillmentText1 = "Basic Information"+"\n"+"College name: {name}".format(name=college1[0])
                fulfillment2 = "NIRF rank: {name1}".format(name1=college1[1])
                fulfillment3 = "NIRF score: {name2}".format(name2=college1[2])
                fulfillment4 = "Intake: {name3}".format(name3=college1[3])
                fulfillment5 = "Placed: {name4}".format(name4=college1[4])
                fulfillment6 = "Median Salary: {name5}".format(name5=college1[5])
                return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Yeah! We got it😎",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentText1+"\n"+fulfillment2+"\n"+fulfillment3+"\n"+fulfillment4+"\n"+fulfillment5+"\n"+fulfillment6,
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
# Course Suggest:
    elif intent == "Suggest a Course":
        return {
                        "payload": {
                        "google": {
                        "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                "textToSpeech": "Tell me what you're looking for 🧐"   
                            }
                        },
                        {
                                "simpleResponse": {
                                "textToSpeech": "Let's be more specific 🕵🏻‍♀️"
                            }
                        }
                        ],
                        "suggestions": [
                            
                            {   
                                "title": "UG courses"     
                            },
                            {   
                                "title": "PG courses"
                            }
                        ]  
                        }
                        }
                        }
                        }   
#UG courses:
    #Engineering courses UG:
    elif intent == "Engineering courses":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Engineering 👨🏽‍🎓 Trending courses"
        fulfillment="Do you have any courses in your mind for Engineering?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "You're at the right place."   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "I'm always happy to help you."   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "Tell me more.🤓🤓"   
                            }
                        }
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillment 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    elif intent == "Yes_Engineering_UG":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form_submitted_Eng_Courses_UG": 
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
    elif intent == "Information_Technology_with Specialization_in Cloud Technology and Information Security_UG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "CSE with specialization in Network Security_UG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "CSE with specialization in Web Technology_UG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "CSE with specialization in IoT& Cyber Security_UG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "CSE with specialization in AI & Machine Learning_UG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "Manufacturing Process and Automation Engineering_UG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "Computer Science and Engineering (Artificial Intelligence)_UG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "Chemical Technology with Specialization in Paint Technology_UG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "Chemical Technology with Specialization in Plastic Technology_UG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "Chemical Technology with Specialization in Leather Technology_UG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#COURSES FOR ENGINEERING:
#Do you have a any courses in your mind for Engineering?
    elif intent == "Do you have any courses in your mind for Engineering?":
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        college1=[]
        sql =('SELECT distinct \
  cs_courselists.cs_coursename \
  FROM cs_courselists  ')
        cur.execute(sql)
        myresult = cur.fetchall()
        #print(myresult) 
        for webhook in myresult:
            college.extend(webhook) 
            
        for details in college:
            if city == details:
                college1 = []
                mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
                cur = mydb.cursor()
                sql1=('SELECT distinct \
  cs_college_info.cs_collegename \
  FROM cs_courses_nw \
  left join cs_college_info on cs_college_info.cs_sno = cs_courses_nw.college_id \
  left join cs_courselists on cs_courselists.cs_sno = cs_courses_nw.course_id \
  where cs_courselists.cs_coursename = "%s" and cs_college_info.cs_col_nirf_rank >=1 GROUP by cs_college_info.cs_col_nirf_rank' %city)    
                cur.execute(sql1)
                myresult1 = cur.fetchall()
                #print(myresult1)
                for webhook1 in myresult1:
                    college1.extend(webhook1)
            #print(college1[0])        
                if len(college1) >= 5:  
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
            elif len(college1) >= 4: 
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

            elif len(college1) >= 3:   
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
                        
            elif len(college1) >= 2:   
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
                            
            elif len(college1) >= 1:  
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
    elif intent == "Medical courses":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Medical 👨🏾‍⚕️ Trending courses"
        fulfillment = "Do you have any courses in your mind for Medical?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Hey future doctor, this is the right thing to do for the world now."   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "How can I help you?"   
                            }
                        }
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillment 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    elif intent == "Yes_Medical_UG":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form_submitted_Medical_courses_UG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT  \
  cs_courselists.cs_coursename \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        #fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's the most trendy courses you asked for 👇👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":"Let's go deeper 👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[0],
            "message": college[0]
            
        }
       ]
       
    }
         }
      }
   ]
}

# Medical UG trending courses:
    elif intent == "MBBS_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1  limit 10 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        if len(college) >= 10:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trending_medical_ug.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9]),
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
        
#COURSES FOR MEDICAL:
#Do you have a any courses in your mind for Medical?
    elif intent == "Do you have any courses in your mind for Medical?":
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        college1 = []
        sql =('SELECT distinct \
  cs_courselists.cs_coursename \
  FROM cs_courselists  ')
        cur.execute(sql)
        myresult = cur.fetchall()
        #print(myresult) 
        for webhook in myresult:
            college.extend(webhook) 
            
        for details in college:
            if city == details:
                college1 = []
                mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
                cur = mydb.cursor()
                sql1=('SELECT distinct \
  cs_college_info.cs_collegename \
  FROM cs_courses_nw \
  left join cs_college_info on cs_college_info.cs_sno = cs_courses_nw.college_id \
  left join cs_courselists on cs_courselists.cs_sno = cs_courses_nw.course_id \
  where cs_courselists.cs_coursename = "%s" and cs_college_info.cs_col_nirf_rank >=1 GROUP by cs_college_info.cs_col_nirf_rank' %city)    
                cur.execute(sql1)
                myresult1 = cur.fetchall()
                #print(myresult1)
                for webhook1 in myresult1:
                    college1.extend(webhook1)
            #print(college1[0])        
                if len(college1) >= 5:  
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
            elif len(college1) >= 4: 
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

            elif len(college1) >= 3:   
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
                        
            elif len(college1) >= 2:   
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
                            
            elif len(college1) >= 1:  
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
#Architecture courses UG:
    elif intent == "Architecture courses":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Architecture 👨🏾‍🎓 Trending courses"
        fulfillment = "Do you have any courses in your mind for Architecture?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Confused about updates in architecture studies."   
                            }
                        },
                 {
                       "simpleResponse": {
                       "textToSpeech":"I am here to help you 😉"   
                            }
                        }    
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillment 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    elif intent == "Yes_architecture_UG":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form_submitted_Architecture_courses_UG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT  distinct \
  cs_courselists.cs_coursename \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        #fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Trendiest courses in the coolest stream 👇👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":"Choose one👇",
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
            
        }
       ]
       
    }
         }
      }
   ]
}

# UG_Bachelor of Architecture:
    elif intent == "Bachelor of Architecture_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
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
        name = college[0]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1 and cs_courselists.cs_sno = {city} limit 5'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

# UG_Architecture & Planning:
    elif intent == "Architecture & Planning_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
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
        name = college[1]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1 and cs_courselists.cs_sno = {city} limit 5'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Dental courses UG:
    elif intent == "Dental courses":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Dental 👨🏾‍⚕️ Trending courses"
        fulfillment = "Do you have any courses in your mind for Dental?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "**heartfelt smile for you**😃"    
                            }
                        },
               {
                      "simpleResponse":{
                      "textToSpeech":"Your future profession can make this world smile. Thankyou!"   
                           }
                       },
               {
                      "simpleResponse":{
                      "textToSpeech":"How can I help you to reach there?!"   
                           }
                       }    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillment
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    elif intent == "Yes_dental_UG":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form_submitted_Dental_courses_UG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT  distinct \
  cs_courselists.cs_coursename \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id = 1')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        #fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Nothing is more trendy than a smile! Anyway, here are some trendy way to make us smile😁😁",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":"Choose one👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[0],
            "message": college[0]
            
        }
       ]
       
    }
         }
      }
   ]
}

# Dental UG trending courses:
    elif intent == "Bachelor of Dental Surgery_UG":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 1  limit 10 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        if len(college) >= 10:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message": render_template("Trending_medical_ug.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9]),
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

#COURSES FOR DENTAL:
#Do you have a any courses in your mind for Dental?
    elif intent == "Do you have any courses in your mind for Dental?":
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        college1 = []
        sql =('SELECT distinct \
  cs_courselists.cs_coursename \
  FROM cs_courselists  ')
        cur.execute(sql)
        myresult = cur.fetchall()
        #print(myresult) 
        for webhook in myresult:
            college.extend(webhook) 
            
        for details in college:
            if city == details:
                college1 = []
                mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
                cur = mydb.cursor()
                sql1=('SELECT distinct \
  cs_college_info.cs_collegename \
  FROM cs_courses_nw \
  left join cs_college_info on cs_college_info.cs_sno = cs_courses_nw.college_id \
  left join cs_courselists on cs_courselists.cs_sno = cs_courses_nw.course_id \
  where cs_courselists.cs_coursename = "%s" and cs_college_info.cs_col_nirf_rank >=1 GROUP by cs_college_info.cs_col_nirf_rank' %city)    
                cur.execute(sql1)
                myresult1 = cur.fetchall()
                #print(myresult1)
                for webhook1 in myresult1:
                    college1.extend(webhook1)
            #print(college1[0])        
                if len(college1) >= 5:  
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
            elif len(college1) >= 4: 
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

            elif len(college1) >= 3:   
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
                        
            elif len(college1) >= 2:   
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
                            
            elif len(college1) >= 1:  
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

#Pharmacy courses UG:
    elif intent == "Pharmacy courses":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Pharmacy 👨🏾‍⚕️ Trending courses"
        fulfillment = "Do you have any courses in your mind for Pharmacy?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                 {
                       "simpleResponse": {
                       "textToSpeech":"You decided to heal this world, right? Thats Great."   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech":"How can I help you for now?"   
                            }
                        }  
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillment
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    elif intent == "Yes_pharmacy_UG":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form_submitted_Pharmacy_courses_UG": 
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
        #fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"These are the trending courses in your prefered stream. Hope this help.",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":"Choose one👇",
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

#COURSES FOR PHARMACY:
#Do you have a any courses in your mind for Pharmacy?
    elif intent == "Do you have any courses in your mind for Pharmacy?":
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
        cur = mydb.cursor()
        college = []
        college1 = []
        sql =('SELECT distinct \
  cs_courselists.cs_coursename \
  FROM cs_courselists  ')
        cur.execute(sql)
        myresult = cur.fetchall()
        #print(myresult) 
        for webhook in myresult:
            college.extend(webhook) 
            
        for details in college:
            if city == details:
                college1 = []
                mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
                cur = mydb.cursor()
                sql1=('SELECT distinct \
  cs_college_info.cs_collegename \
  FROM cs_courses_nw \
  left join cs_college_info on cs_college_info.cs_sno = cs_courses_nw.college_id \
  left join cs_courselists on cs_courselists.cs_sno = cs_courses_nw.course_id \
  where cs_courselists.cs_coursename = "%s" and cs_college_info.cs_col_nirf_rank >=1 GROUP by cs_college_info.cs_col_nirf_rank' %city)    
                cur.execute(sql1)
                myresult1 = cur.fetchall()
                #print(myresult1)
                for webhook1 in myresult1:
                    college1.extend(webhook1)
            #print(college1[0])        
                if len(college1) >= 5:  
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
            elif len(college1) >= 4: 
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

            elif len(college1) >= 3:   
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
                        
            elif len(college1) >= 2:   
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
                            
            elif len(college1) >= 1:  
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

#PG courses:
    #Engineering courses PG:
    elif intent == "Engineering courses_PG":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Engineering 👨🏽‍🎓 Trending courses"
        fulfillment = "Do you have any courses in your mind for Engineering?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Nice choice friend!!"   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "you're one among us.💪"   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "Let's move forward."   
                            }
                        }
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillment
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    elif intent == "Yes_Engineering_PG":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form_submitted_Engineering_courses_PG": 
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
            "message":"So happy that you want to try something new!",
            "platform": "kommunicate"
        }
    },
    {
        "payload": {
            "message":"Here the most trending courses!!",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":"which one you're most likely to go for?  👇",
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
    elif intent == "Electronics and Telecommunication specilization with Communication Network_PG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "Civil Engg. with specialization in Infrastructure Engineering & Management_PG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "Electrical Engg. with pecialization in Power System_PG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "CSE with M.Tech specialization in Information Technology_PG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "ECE with Specialization in  Communication & Signal Processing_PG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "ECE with M.Tech Specialization in Power and Control_PG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "ECE with M.Tech Specialization in Microwave and Communication Engineering_PG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "Wireless Networks & Applications (Specialising in IoT, AI, 5G, Blockchain)_PG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "CSE – Full Stack with Virtusa_PG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "Chemical Technology with Specialization in Biochemical Engineering_PG":
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
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
    elif intent == "Medical courses_PG":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Medical 👨🏾‍⚕️ Trending courses"
        fulfillment = "Do you have any courses in your mind for Medical?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Glad that you're taking another step forward.  🙏 "   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "We're more than happy that you came to us!"   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech": "tell me doc, what you're looking forward to.."   
                            }
                        }
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillment
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    elif intent == "Yes_medical_PG":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form_submitted_Medical_courses_PG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT cs_courselists.cs_coursename \
        FROM cs_courses_nw \
        left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
        where cs_courses_nw.degree_type_id = 2')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        #fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"The most accurate data is here, personalised for you. Exactly how you like it.👇👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":"Let's go deeper 👇",
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
            "title": college[10],
            "message": college[10]
            
        }
       ]
       
    }
         }
      }
   ]
}

#Medical_PG Trending courses:
#Nuclear Medicine Technology_PG:
    elif intent == 'Nuclear_Medicine_Technology_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[0]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Anatomy_PG:
    elif intent == 'Anatomy_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Biochemistry_PG:
    elif intent == 'Biochemistry_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[2]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Biophysics_PG:
    elif intent == 'Biophysics_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[3]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Pharmacology_PG:
    elif intent == 'Pharmacology_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[4]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Physiology_PG:
    elif intent == 'Physiology_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[5]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Reproductive Biology and Clinical Embryology_PG:
    elif intent == 'Reproductive Biology and Clinical Embryology_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[6]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Cardiovascular_Imaging_and_Endovascular_Technologies_PG:
    elif intent == 'Cardiovascular_Imaging_and_Endovascular_Technologies_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[7]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Clinical Pathology_PG:
    elif intent == 'Clinical Pathology_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[8]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Diploma in Anaesthesia_PG:
    elif intent == 'Diploma in Anaesthesia_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[10]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Architecture courses PG:
    elif intent == "Architecture courses_PG":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Architecture 👨🏾‍🎓 Trending courses"
        fulfillment = "Do you have any courses in your mind for Architecture?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Hey!! Someone of the coolest stream going cooler😆😅"   
                            }
                        },
                 {
                       "simpleResponse": {
                       "textToSpeech":"That's great"   
                            }
                        },
                 {
                       "simpleResponse": {
                       "textToSpeech":"What can I find for you?"   
                            }
                        }     
                    
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillment 
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    elif intent == "Yes_architecture_PG":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form_submitted_Architecture_courses_PG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT distinct cs_courselists.cs_coursename \
        FROM cs_courses_nw \
        left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
        where cs_courses_nw.degree_type_id = 2')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        #fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"The trending courses for the architect in you 👇",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":"Choose one👇",
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

#City planning:
    elif intent == 'City planning_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[0]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#sustainable built environment_PG:
    elif intent == 'sustainable built environment_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Architecture & Planning_PG:
    elif intent == 'Architecture & Planning_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[2]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Architectural Design_PG:
    elif intent == 'Architectural Design_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[3]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Urban Design_PG:
    elif intent == 'Urban Design_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[4]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Industrial Design_PG:
    elif intent == 'Industrial Design_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[5]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Conservation_PG:
    elif intent == 'Conservation_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[6]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Landscape_PG:
    elif intent == 'Landscape_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[7]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Design_PG:
    elif intent == 'Design_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[8]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Energy Efficient and Sustainable Architecture_PG:
    elif intent == 'Energy Efficient and Sustainable Architecture_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[9]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Dental courses PG:
    elif intent == "Dental courses_PG":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Dental 👨🏾‍⚕️ Trending courses"
        fulfillment = "Do you have any courses in your mind for Dental?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech": "Taking another big step huh?"    
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
                        "title": fulfillment
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    elif intent == "Yes_dental_PG":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form_submitted_Dental_courses_PG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT distinct cs_courselists.cs_coursename \
        FROM cs_courses_nw \
        left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
        where cs_courses_nw.degree_type_id = 2')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        #fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Go! Go further! ",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":"Choose one👇",
            "platform":"kommunicate",
            
            "metadata": {
        "contentType": "300",
        "templateId": "6",
        "payload": [
        {
            "title": college[1],
            "message": college[1]
            
        },
        {
            "title": college[4],
            "message": college[4]
            
        },
        {
            "title": college[7],
            "message": college[7]
            
        },
        {
            "title": college[5],
            "message": college[5]
            
        },
        {
            "title": college[2],
            "message": college[2]
            
        },
        {
            "title": college[9],
            "message": college[9]
            
        },
        {
            "title": college[3],
            "message": college[3]
            
        },
        {
            "title": college[0],
            "message": college[0]
            
        },
        {
            "title": college[8],
            "message": college[8]
            
        },
        {
            "title": college[7],
            "message": college[7]
            
        }
       ]
       
    }
         }
      }
   ]
}

#Conservative Dentistry and Endodontics_PG:
    elif intent == 'Conservative Dentistry and Endodontics_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[1]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Oral and Maxillofacial Surgery_PG:
    elif intent == 'Oral and Maxillofacial Surgery_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[4]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Oral Medicine and Radiology_PG:
    elif intent == 'Oral Medicine and Radiology_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[7]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Oral Pathology and Microbiology_PG:
    elif intent == 'Oral Pathology and Microbiology_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[5]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Orthodonitics and Dentofacial Orthopaedics_PG:
    elif intent == 'Orthodonitics and Dentofacial Orthopaedics_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[2]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Paedodontics and Preventive Dentistry_PG:
    elif intent == 'Paedodontics and Preventive Dentistry_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[9]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Periodontology_PG:
    elif intent == 'Periodontology_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[3]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Prosthodontics and Crown and Bridge_PG:
    elif intent == 'Prosthodontics and Crown and Bridge_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[0]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Public Health Dentistry_PG:
    elif intent == 'Public Health Dentistry_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[8]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Oral Medicine and Radiology_PG:
    elif intent == 'Oral Medicine and Radiology_PG':
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        college1 = []
        fulfillmentText = ''
        sql =('SELECT distinct \
  cs_courselists.cs_sno \
  FROM cs_courses_nw \
  left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno\
  where cs_courses_nw.degree_type_id =2 ')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        name = college[7]
        sql1 =('SELECT cs_college_info.cs_collegename \
from cs_courses_nw \
left JOIN cs_courselists ON cs_courses_nw.course_id = cs_courselists.cs_sno \
left join cs_college_info on cs_courses_nw.college_id = cs_college_info.cs_sno \
where cs_courses_nw.degree_type_id = 2 and cs_courselists.cs_sno = {city}'.format(city = name))
        cur.execute(sql1)
        myresult1 = cur.fetchall() 
        for webhook1 in myresult1:
            college1.extend(webhook1)
        if len(college1) >= 5:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
        elif len(college1) >= 4: 
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

        elif len(college1) >= 3:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                        
        elif len(college1) >= 2:   
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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
                            
        elif len(college1) >= 1:  
            return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Here's what I found👇",
            "platform": "kommunicate"
        }
    },
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

#Pharmacy courses PG:
    elif intent == "Pharmacy courses_PG":
        #fulfillmentText = "Top colleges of Government and Private. Please, choose the options."
        fulfillmentText1 = "Top 10 Pharmacy 👨🏾‍⚕️ Trending courses"
        fulfillment = "Do you have any courses in your mind for Pharmacy?"
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                {
                       "simpleResponse": {
                       "textToSpeech":"You know whats the best thing to do?"   
                            }
                        },
                {
                       "simpleResponse": {
                       "textToSpeech":"Learn more. You’re doing the right thing!"   
                            }
                        } ,
                {
                       "simpleResponse": {
                       "textToSpeech":"We’re here for you."   
                            }
                        }  ,
                {
                       "simpleResponse": {
                       "textToSpeech":"How can we help?"   
                            }
                        }     
                ],
                "suggestions": [
                    {   
                        "title": fulfillmentText1 
                    },
                    {   
                        "title": fulfillment
                    }
                ]    
                }
                }
                }
                }  
                
# html form showed in the chatbot:
    elif intent == "Yes_pharmacy_PG":
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
            "formAction": "https://cc80d242f398.ngrok.io/result"
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
    elif intent == "Form_submitted_Pharmacy_courses_PG": 
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
        #fulfillmentMessages = render_template("coursesuggest.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4],value5=college[5],value6=college[6],value7=college[7],value8=college[8],value9=college[9])
        
        return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Thank you! This is the list of courses you asked for! Reach out to us .",
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":"We are always happy to help you.👇",
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

#ADMISSION INFORMATION:
# Admission Intent:
    elif intent == "I want to know more about Admission Information":
        return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    {
                     "simpleResponse": {
                     "textToSpeech": "Which colleges do you want for Admission Information?"   
                    }
                }
                ],
                "suggestions": [         
                 {   
                     "title": "Engineering Admission details"     
                     },
                 {   
                     "title": "Medical Admission details"
                  },
                 {   
                     "title": "Architecture Admission details"
                  },
                 {   
                     "title": "Dental Admission details"
                  },
                 {   
                     "title": "Pharmacy Admission details"
                  }
                  ]  
                  }
                  }
                  }
                  }
                     

#Engineering Admission details
    elif intent == "Engineering Admission details":
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
        cur = mydb.cursor()
        college=[]
        college1 = []
        sql =('SELECT distinct \
  cs_collegename \
  FROM cs_college_info ')
        cur.execute(sql)    
        myresult = cur.fetchall()
        for webhook in myresult:
            college.extend(webhook)
        for details in college:
            if city == details:
                sql =('select cs_college_info.cs_collegename,cs_college_info.cs_col_address,cs_college_info.cs_col_phone, cs_college_info.cs_col_email,cs_college_info.cs_col_web\
                from cs_college_info \
                WHERE  cs_college_info.cs_collegename ="%s"' %city)
                cur.execute(sql)
                myresult = cur.fetchall()
                for webhook in myresult:
                    college1.extend(webhook) 
                fulfillmentText1 ="College name: {name}".format(name=college1[0])
                fulfillment2 = "College Address: {name1}".format(name1=college1[1])
                fulfillment3 = "College Phone Number: {name2}".format(name2=college1[2])
                fulfillment4 = "College Email: {name3}".format(name3=college1[3])
                fulfillment5 = "College Web: {name4}".format(name4=college1[4])
                return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Admission Information",
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillmentText1,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment2,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment3,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment4,
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillment5,
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
    
#Medical Admission details
    elif intent == "Medical Admission details":
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college=[]
        college1 = []
        sql =('SELECT distinct \
  cs_collegename \
  FROM cs_college_info ')
        cur.execute(sql)    
        myresult = cur.fetchall()
        for webhook in myresult:
            college.extend(webhook)
        for details in college:
            if city == details:
                sql =('select cs_college_info.cs_collegename,cs_college_info.cs_col_address,cs_college_info.cs_col_phone, cs_college_info.cs_col_email,cs_college_info.cs_col_web\
                from cs_college_info \
                WHERE  cs_college_info.cs_collegename ="%s"' %city)
                cur.execute(sql)
                myresult = cur.fetchall()
                for webhook in myresult:
                    college1.extend(webhook) 
                fulfillmentText1 ="College name: {name}".format(name=college1[0])
                fulfillment2 = "College Address: {name1}".format(name1=college1[1])
                fulfillment3 = "College Phone Number: {name2}".format(name2=college1[2])
                fulfillment4 = "College Email: {name3}".format(name3=college1[3])
                fulfillment5 = "College Web: {name4}".format(name4=college1[4])
                return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Admission Information",
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillmentText1,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment2,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment3,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment4,
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillment5,
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
 
#Architecture Admission details
    elif intent == "Architecture Admission details":
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college=[]
        college1 = []
        sql =('SELECT distinct \
  cs_collegename \
  FROM cs_college_info ')
        cur.execute(sql)    
        myresult = cur.fetchall()
        for webhook in myresult:
            college.extend(webhook)
        for details in college:
            if city == details:
                sql =('select cs_college_info.cs_collegename,cs_college_info.cs_col_address,cs_college_info.cs_col_phone, cs_college_info.cs_col_email,cs_college_info.cs_col_web\
                from cs_college_info \
                WHERE  cs_college_info.cs_collegename ="%s"' %city)
                cur.execute(sql)
                myresult = cur.fetchall()
                for webhook in myresult:
                    college1.extend(webhook) 
                fulfillmentText1 ="College name: {name}".format(name=college1[0])
                fulfillment2 = "College Address: {name1}".format(name1=college1[1])
                fulfillment3 = "College Phone Number: {name2}".format(name2=college1[2])
                fulfillment4 = "College Email: {name3}".format(name3=college1[3])
                fulfillment5 = "College Web: {name4}".format(name4=college1[4])
                return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Admission Information",
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillmentText1,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment2,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment3,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment4,
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillment5,
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

#Dental Admission details
    elif intent == "Dental Admission details":
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college=[]
        college1 = []
        sql =('SELECT distinct \
  cs_collegename \
  FROM cs_college_info ')
        cur.execute(sql)    
        myresult = cur.fetchall()
        for webhook in myresult:
            college.extend(webhook)
        for details in college:
            if city == details:
                sql =('select cs_college_info.cs_collegename,cs_college_info.cs_col_address,cs_college_info.cs_col_phone, cs_college_info.cs_col_email,cs_college_info.cs_col_web\
                from cs_college_info \
                WHERE  cs_college_info.cs_collegename ="%s"' %city)
                cur.execute(sql)
                myresult = cur.fetchall()
                for webhook in myresult:
                    college1.extend(webhook) 
                fulfillmentText1 ="College name: {name}".format(name=college1[0])
                fulfillment2 = "College Address: {name1}".format(name1=college1[1])
                fulfillment3 = "College Phone Number: {name2}".format(name2=college1[2])
                fulfillment4 = "College Email: {name3}".format(name3=college1[3])
                fulfillment5 = "College Web: {name4}".format(name4=college1[4])
                return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Admission Information",
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillmentText1,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment2,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment3,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment4,
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillment5,
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

#Pharmacy Admission details
    elif intent == "Pharmacy Admission details":
        city = parameters.get("college")
        city = str(city)[1:-1] 
        print(city)
        city=city.replace("'", "")
        print(city)
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
        cur = mydb.cursor()
        college=[]
        college1 = []
        sql =('SELECT distinct \
  cs_collegename \
  FROM cs_college_info ')
        cur.execute(sql)    
        myresult = cur.fetchall()
        for webhook in myresult:
            college.extend(webhook)
        for details in college:
            if city == details:
                sql =('select cs_college_info.cs_collegename,cs_college_info.cs_col_address,cs_college_info.cs_col_phone, cs_college_info.cs_col_email,cs_college_info.cs_col_web\
                from cs_college_info\
                WHERE  cs_college_info.cs_collegename ="%s"' %city)
                cur.execute(sql)
                myresult = cur.fetchall()
                for webhook in myresult:
                    college1.extend(webhook) 
                fulfillmentText1 ="College name: {name}".format(name=college1[0])
                fulfillment2 = "College Address: {name1}".format(name1=college1[1])
                fulfillment3 = "College Phone Number: {name2}".format(name2=college1[2])
                fulfillment4 = "College Email: {name3}".format(name3=college1[3])
                fulfillment5 = "College Web: {name4}".format(name4=college1[4])
                return {
   "fulfillmentMessages":[
   {
        "payload": {
            "message":"Admission Information",
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillmentText1,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment2,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment3,
            "platform": "kommunicate"
        }
    },{
        "payload": {
            "message":fulfillment4,
            "platform": "kommunicate"
        }
    },
      {
         "payload":{
            "messageType":"html",
            "message":fulfillment5,
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
    return 0
    
if __name__ == '__main__':
    app.run(debug=False,port = 80)