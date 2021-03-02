from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for,session 
import requests
import json
import MySQLdb

app = Flask(__name__)

@app.route('/form', methods=['POST','GET'])  
def form():
    c=[]
    mydb = MySQLdb.connect(host='localhost',user='root',password= 'Chatbot',database='student2')
    cur = mydb.cursor()
    myresult = cur.execute("SELECT distinct  josaa_col_category.j_col_category FROM josaa_ranking \
		left join josaa_col_category on josaa_ranking.j_category = josaa_col_category.j_sno limit 1  ")
#myresult = cur.fetchall()
#for i in myresult:
#    c.extend(i)
  
    return(myresult)

if __name__ == '__main__':
    app.run(debug=False)      
 
