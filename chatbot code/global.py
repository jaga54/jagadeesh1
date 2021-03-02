#from app import index_add_counter
from flask_session import Session
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session,app,current_app

# session configuraiton -- filesystem interface
app = Flask(__name__)

global index_add_counter

index_add_counter = 0
def test():
  global index_add_counter # means: in this scope, use the global name
  print(index_add_counter)
  
if __name__ == '__main__':
    app.run(debug=False)        