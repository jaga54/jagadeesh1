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
    
    
    if intent == "studentdetails": 
        stud_name = parameters.get("stud_name")
        email = parameters.get("email")
        mobile = parameters.get("mobile")
        city = parameters.get("city")
        country = parameters.get("country")
        
    
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
		

    if intent == "All_colleges_details":
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        sql = ('SELECT cs_collegename FROM cs_college_info limit 10')
        cur.execute(sql)
        myresult = cur.fetchall()
         
        for webhook in myresult:
            college.extend(webhook)    
                        
        fulfillmentText = 'Top colleges in India: '
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
                    },
                    {   
                        "title": college[5] 
                    },
                    {   
                        "title": college[6] 
                    },
                    {   
                        "title": college[7] 
                    },
                    {   
                        "title": college[8] 
                    },
                    {   
                        "title": college[9] 
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
                
                
    
                
    if intent == "Overallcolleges_city":
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
                        
                fulfillmentText = 'Top colleges in {} :'.format(city)
                
                
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

    if intent == 'Median_Salary_city':
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
    
                sql = ('SELECT  cs_college_info.cs_collegename, cs_col_nirf_placements.median_salary_for_placed\
                 FROM cs_college_info\
                left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                left join cs_city on cs_college_info.cs_col_city = cs_city.cs_sno\
                left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates\
                left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type\
                WHERE cs_city.cs_city = "%s" and cs_col_nirf_academic_year.years = "2018-19" and cs_degreetype.cs_degree = "UG" limit 5 ' %city )    
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.extend(webhook)    
                        
                fulfillmentText = 'Top Median Salary colleges in {}, College_name & Median_Salary:'.format(city) 
                fulfillmentText1 = "{0}, {1}".format(college[0],college[1])
                fulfillmentText2 = "{0}, {1}".format(college[2],college[3])
                fulfillmentText3 = "{0}, {1}".format(college[4],college[5])
                fulfillmentText4 = "{0}, {1}".format(college[6],college[7])
                fulfillmentText5 = "{0}, {1}".format(college[8],college[9])
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
                        "textToSpeech": fulfillmentText1
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText2
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText3
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText4
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText5
                        }
                    }
                ]       
                }
                }
                }
                
                }
                      

    if intent == 'Placement_city':
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
    
                sql = ('SELECT   cs_collegename, cs_col_nirf_placements.no_of_placed \
                        FROM cs_college_info\
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        left join cs_city on cs_college_info.cs_col_city = cs_city.cs_sno\
                        left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates\
                        left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type\
                        WHERE cs_city.cs_city = "%s" and cs_col_nirf_academic_year.years = "2018-19" and cs_degreetype.cs_degree = "UG" limit 5 ' %city )    
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.extend(webhook)    
                        
                fulfillmentText = 'Top Placement colleges in {} College_name & student_Placed:'.format(city) 
                fulfillmentText1 = "{0}, {1}".format(college[0],college[1])
                fulfillmentText2 = "{0}, {1}".format(college[2],college[3])
                fulfillmentText3 = "{0}, {1}".format(college[4],college[5])
                fulfillmentText4 = "{0}, {1}".format(college[6],college[7])
                fulfillmentText5 = "{0}, {1}".format(college[8],college[9])
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
                        "textToSpeech": fulfillmentText1
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText2
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText3
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText4
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText5
                        }
                    }
                ]       
                }
                }
                }
                
                }

    if intent == 'Intake_city':
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
    
                sql = ('SELECT  cs_college_info.cs_collegename, cs_col_nirf_placements.no_of_intake\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        left join cs_city on cs_college_info.cs_col_city = cs_city.cs_sno\
                        left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates\
                        left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type\
                        WHERE cs_city.cs_city = "%s" and cs_col_nirf_academic_year.years = "2018-19" and cs_degreetype.cs_degree = "UG" limit 5 ' %city )    
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.extend(webhook)    
                        
                fulfillmentText = ' colleges in {}, College_name & No_of_Intake:'.format(city) 
                fulfillmentText1 = "{0}, {1}".format(college[0],college[1])
                fulfillmentText2 = "{0}, {1}".format(college[2],college[3])
                fulfillmentText3 = "{0}, {1}".format(college[4],college[5])
                fulfillmentText4 = "{0}, {1}".format(college[6],college[7])
                fulfillmentText5 = "{0}, {1}".format(college[8],college[9])
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
                        "textToSpeech": fulfillmentText1
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText2
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText3
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText4
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText5
                        }
                    }
                ]       
                }
                }
                }
                }
                 

    if intent == "Overallcolleges_state":
        state = parameters.get("state") 
        state = str(state)
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        state = state
        sql = "select  DISTINCT  cs_statename from cs_state"
        cur.execute(sql)
        myresult = cur.fetchall()
        var=[]

        for x in myresult:
            var.extend(x)

        for cities in var:
            if state == cities:
    
                sql = ('SELECT  cs_college_info.cs_collegename\
                        FROM cs_state left join cs_college_info on cs_state.cs_sno = cs_college_info.cs_col_state\
                        WHERE cs_state.cs_statename = "%s" limit 5 ' %state )    
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.extend(webhook)    
                        
                fulfillmentText = 'Top colleges in {} :'.format(state)
                
                
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

    
    if intent == 'Mediansalary_state':
        state = parameters.get("state") 
        state = str(state)
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        state = state
        sql = "select  DISTINCT  cs_statename from cs_state"
        cur.execute(sql)
        myresult = cur.fetchall()
        var=[]

        for x in myresult:
            var.extend(x)

        for cities in var:
            if state == cities:
    
                sql = ('SELECT  cs_college_info.cs_collegename, cs_col_nirf_placements.median_salary_for_placed\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        left join cs_state on cs_college_info.cs_col_state = cs_state.cs_sno\
                        left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates\
                        left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type\
                        WHERE cs_state.cs_statename = "%s" and cs_col_nirf_academic_year.years = "2018-19" and cs_degreetype.cs_degree = "UG" limit 5 ' %state )    
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.extend(webhook)    
                        
                fulfillmentText = 'Top Median Salary colleges in {} , College_name & Median_Salary:'.format(state) 
                fulfillmentText1 = "{0}, {1}".format(college[0],college[1])
                fulfillmentText2 = "{0}, {1}".format(college[2],college[3])
                fulfillmentText3 = "{0}, {1}".format(college[4],college[5])
                fulfillmentText4 = "{0}, {1}".format(college[6],college[7])
                fulfillmentText5 = "{0}, {1}".format(college[8],college[9])
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
                        "textToSpeech": fulfillmentText1
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText2
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText3
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText4
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText5
                        }
                    }
                ]       
                }
                }
                }
                
                }
        
        
    if intent == 'Placement_state':
        state = parameters.get("state") 
        state = str(state)
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        state = state
        sql = "select  DISTINCT  cs_statename from cs_state"
        cur.execute(sql)
        myresult = cur.fetchall()
        var=[]

        for x in myresult:
            var.extend(x)

        for cities in var:
            if state == cities:
    
                sql = ('SELECT   cs_collegename, cs_col_nirf_placements.no_of_placed\
                        FROM cs_college_info\
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        left join cs_state on cs_college_info.cs_col_state = cs_state.cs_sno\
                        left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates\
                        left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type\
                        WHERE cs_state.cs_statename = "%s" and cs_col_nirf_academic_year.years = "2018-19"and cs_degreetype.cs_degree = "UG" limit 5 ' %state )    
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.extend(webhook)    
                        
                fulfillmentText = 'Top Placement colleges in {} , College_name & student_Placed:'.format(state) 
                fulfillmentText1 = "{0}, {1}".format(college[0],college[1])
                fulfillmentText2 = "{0}, {1}".format(college[2],college[3])
                fulfillmentText3 = "{0}, {1}".format(college[4],college[5])
                fulfillmentText4 = "{0}, {1}".format(college[6],college[7])
                fulfillmentText5 = "{0}, {1}".format(college[8],college[9])
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
                        "textToSpeech": fulfillmentText1
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText2
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText3
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText4
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText5
                        }
                    }
                ]       
                }
                }
                }
                
                }
        

    if intent == 'Intake_state':
        state = parameters.get("state") 
        state = str(state)
        mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='student2')
        cur = mydb.cursor()
        college = []
        fulfillmentText = ''
        state = state
        sql = "select  DISTINCT  cs_statename from cs_state"
        cur.execute(sql)
        myresult = cur.fetchall()
        var=[]

        for x in myresult:
            var.extend(x)
   
        for cities in var:
            if state == cities:
    
                sql = ('SELECT  cs_college_info.cs_collegename, cs_col_nirf_placements.no_of_intake\
                        FROM cs_college_info \
                        left join cs_col_nirf_placements on cs_college_info.cs_sno = cs_col_nirf_placements.college_id\
                        left join cs_state on cs_college_info.cs_col_state = cs_state.cs_sno\
                        left join cs_col_nirf_academic_year on cs_col_nirf_academic_year.id = cs_col_nirf_placements.year_id_graduates\
                        left join cs_degreetype on cs_degreetype.cs_sno = cs_col_nirf_placements.degree_type\
                        WHERE cs_state.cs_statename = "%s" and cs_col_nirf_academic_year.years = "2018-19" and cs_degreetype.cs_degree = "UG" limit 5 ' %state )    
                cur.execute(sql)
                myresult = cur.fetchall()
         
                for webhook in myresult:
                    college.extend(webhook)    
                        
                fulfillmentText = ' colleges in {} , College_name & No_of_Intake:'.format(state) 
                fulfillmentText1 = "{0}, {1}".format(college[0],college[1])
                fulfillmentText2 = "{0}, {1}".format(college[2],college[3])
                fulfillmentText3 = "{0}, {1}".format(college[4],college[5])
                fulfillmentText4 = "{0}, {1}".format(college[6],college[7])
                fulfillmentText5 = "{0}, {1}".format(college[8],college[9])
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
                        "textToSpeech": fulfillmentText1
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText2
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText3
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText4
                        }
                    },
                    {
                        "simpleResponse": {
                        "textToSpeech": fulfillmentText5
                        }
                    }
                ]       
                }
                }
                }
                
                }
           
        
    return 0     
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port = 80)  		
		