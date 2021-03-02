from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session,app,current_app
from datetime import timedelta
from flask import current_app as app

app = Flask(__name__)

app.secret_key = "super secret key"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)

@app.route('/visits-counter/')
def visits():
    if 'visits' in session:
        print("helllo")
        session['visits'] = session.get('visits') + 1  # reading and updating session data
    else:
        print("visits_all")
        session['visits'] = 1 # setting session data
    return "Total visits: {}".format(session.get('visits'))

@app.route('/delete-visits/')
def delete_visits():
    session.pop('visits', None) # delete visits
    return 'Visits deleted'
    


if __name__ == '__main__':
    app.run(debug=False)    