from flask import Flask, render_template, request, redirect, url_for, flash
import MySQLdb
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('details.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      name = request.form["name"]
      email = request.form["email"]
      mydb = MySQLdb.connect(host='localhost',user='root',password='Chatbot',database='details')
      cur = mydb.cursor()
      query = "INSERT INTO studentdetails(name,email) VALUES (%s,%s)"
      val = (name,email)
      cur.execute(query, val)
      result = cur.fetchall()
      for row in result:
        print(row[0], row[1])
        print("/n")       
            
      mydb.commit()
      cur.close()
      return ()

if __name__ == '__main__':
    app.run(debug = False)