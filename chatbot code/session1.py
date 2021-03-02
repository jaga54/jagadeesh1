from flask_session import Session
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session,app,current_app

# session configuraiton -- filesystem interface
app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route('/index')
def index():
  # different keywords to store data in session
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'>" + "click here to log in</a>"


@app.route('/headlines', methods=["POST","GET"])
def headlines():
  # retrieving data from and modifying data in sessions
    if request.method == 'POST':
        session['username'] = request.form['nm']
        return redirect(url_for('index'))
    return render_template("test.html")
  
if __name__ == '__main__':
    app.run(debug=False)      