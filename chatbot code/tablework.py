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
        
@app.route('/result', methods=[ 'POST',"GET"])
def result():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
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
    return jsonify("form submitted")   
    

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
                
# html form showed in the chatbot:
    if intent == "Yes_Intent_Govt_Engineering":
        return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "platform":"kommunicate",
            "message":render_template('details.html')
         }
      }
   ]
}
             
   # Top 10 Engineering Government colleges in India                 
    if intent == "Form submitted_GVT_ENG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='engineering')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT distinct cs_college_info.cs_collegename, cs_col_nirf_placements.no_of_intake\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        where cs_college_info.cs_col_category = "G" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com",
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
          
# Top 10 Engineering Private colleges in India
    if intent == "Form submitted_PVT_ENG": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='engineering')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT distinct cs_college_info.cs_collegename, cs_col_nirf_placements.no_of_intake\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        where cs_college_info.cs_col_category = "P" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com",
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
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='engineering')
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
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4])
                    }
                }
                ]
                }
                elif len(college) == 4:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index2.html",value=college[0],value1=college[1],value2=college[2],value3=college[3])
                    }
                }
                ]
                }

                elif len(college) == 3:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index3.html",value=college[0],value1=college[1],value2=college[2])
                    }
                }
                ]
                }
                        
                elif len(college) == 2:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index4.html",value=college[0],value1=college[1])
                    }
                }
                ]
                }
                            
                elif len(college) == 1:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index5.html",value=college[0])
                    }
                }
                ]
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
        sql = ('SELECT distinct cs_college_info.cs_collegename, cs_col_nirf_placements.no_of_intake\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        where cs_college_info.cs_col_category = "G" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com",
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

# Top 10 Medical Private colleges in India                 
    if intent == "Form submitted_PVT_Medical":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='medical')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT distinct cs_college_info.cs_collegename, cs_col_nirf_placements.no_of_intake\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        where cs_college_info.cs_col_category = "P" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com",
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
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4])
                    }
                }
                ]
                }
                elif len(college) == 4:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index2.html",value=college[0],value1=college[1],value2=college[2],value3=college[3])
                    }
                }
                ]
                }

                elif len(college) == 3:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index3.html",value=college[0],value1=college[1],value2=college[2])
                    }
                }
                ]
                }
                        
                elif len(college) == 2:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index4.html",value=college[0],value1=college[1])
                    }
                }
                ]
                }
                            
                elif len(college) == 1:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index5.html",value=college[0])
                    }
                }
                ]
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
        sql = ('SELECT distinct cs_college_info.cs_collegename, cs_col_nirf_placements.no_of_intake\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        where cs_college_info.cs_col_category = "G" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com",
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
# Top 10 Architecture Private colleges in India                 
    if intent == "Form submitted_PVT_Architecture":
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='architecture')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT distinct cs_college_info.cs_collegename, cs_col_nirf_placements.no_of_intake\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        where cs_college_info.cs_col_category = "P" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com",
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
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4])
                    }
                }
                ]
                }
                elif len(college) == 4:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index2.html",value=college[0],value1=college[1],value2=college[2],value3=college[3])
                    }
                }
                ]
                }

                elif len(college) == 3:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index3.html",value=college[0],value1=college[1],value2=college[2])
                    }
                }
                ]
                }
                        
                elif len(college) == 2:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index4.html",value=college[0],value1=college[1])
                    }
                }
                ]
                }
                            
                elif len(college) == 1:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index5.html",value=college[0])
                    }
                }
                ]
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
        sql = ('SELECT distinct cs_college_info.cs_collegename, cs_col_nirf_placements.no_of_intake\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        where cs_college_info.cs_col_category = "G" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com",
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
               
# Top 10 dental Private colleges in India
    if intent == "Form submitted_PVT_Dental": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='dental')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT distinct cs_college_info.cs_collegename, cs_col_nirf_placements.no_of_intake\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        where cs_college_info.cs_col_category = "P" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com",
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
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4])
                    }
                }
                ]
                }
                elif len(college) == 4:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index2.html",value=college[0],value1=college[1],value2=college[2],value3=college[3])
                    }
                }
                ]
                }

                elif len(college) == 3:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index3.html",value=college[0],value1=college[1],value2=college[2])
                    }
                }
                ]
                }
                        
                elif len(college) == 2:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index4.html",value=college[0],value1=college[1])
                    }
                }
                ]
                }
                            
                elif len(college) == 1:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index5.html",value=college[0])
                    }
                }
                ]
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
        sql = ('SELECT distinct cs_college_info.cs_collegename, cs_col_nirf_placements.no_of_intake\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        where cs_college_info.cs_col_category = "G" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com",
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
               
# Top 10 Pharmacy Private colleges in India
    if intent == "Form submitted_PVT_Pharmacy": 
        mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='pharmacy')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT distinct cs_college_info.cs_collegename, cs_col_nirf_placements.no_of_intake\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        where cs_college_info.cs_col_category = "P" limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
        fulfillmentMessages = render_template("index1.html",value=college[0],Intake=college[1],value1=college[2],Intake1=college[3],value2=college[4],Intake2=college[5],value3=college[6],Intake3=college[7],value4=college[8],Intake4=college[9],value5=college[10],Intake5=college[11],value6=college[12],Intake6=college[13],value7=college[14],Intake7=college[15],value8=college[16],Intake8=college[17],value9=college[18],Intake9=college[19])    
        
        return {
   "fulfillmentMessages":[
      {
         "payload":{
            "messageType":"html",
            "message":fulfillmentMessages + "\n"+"https://www.google.com",
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
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index.html",value=college[0],value1=college[1],value2=college[2],value3=college[3],value4=college[4])
                    }
                }
                ]
                }
                elif len(college) == 4:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index2.html",value=college[0],value1=college[1],value2=college[2],value3=college[3])
                    }
                }
                ]
                }

                elif len(college) == 3:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index3.html",value=college[0],value1=college[1],value2=college[2])
                    }
                }
                ]
                }
                        
                elif len(college) == 2:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index4.html",value=college[0],value1=college[1])
                    }
                }
                ]
                }
                            
                elif len(college) == 1:  
                    return {
                    "fulfillmentMessages":[
                    {
                        "payload":{
                        "messageType":"html",
                        "platform":"kommunicate",
                        "message":render_template("index5.html",value=college[0])
                    }
                }
                ]
                }
                
                
    return 0
    
if __name__ == '__main__':
    app.run(debug=False,port = 80)