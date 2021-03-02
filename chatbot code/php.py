from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for,session
import mysql.connector
import MySQLdb
from flask_cors import CORS
import json

app = Flask(__name__)
cors = CORS(app)

@app.route('/hello', methods=['GET', 'POST'])
def hello(): 
    c=[]
    d=[]
    e=[]
    f=[]
    college=[]
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
        
    #Jossa Academic program
    cur.execute("SELECT distinct josaa_course.j_course  FROM josaa_ranking \
left join josaa_course on josaa_ranking.j_acedemic = josaa_course.j_sno")
    rounds14 = cur.fetchall()
    for i in rounds14:
        f.extend(i)   
        
    
        
    return render_template("josaa.html",c=c,d=d)
    
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
        

    
        
if __name__ == '__main__':
    app.run(debug=False)	