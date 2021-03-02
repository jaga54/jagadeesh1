from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for,session
import mysql.connector
import MySQLdb
app = Flask(__name__)
@app.route('/hello')

def hello():

	return render_template("index.php")
    
if __name__ == '__main__':
    app.run(debug=False)    