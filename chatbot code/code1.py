from flask import Flask, render_template, request, jsonify, make_response,redirect
app = Flask(__name__)


	

@app.route('/webhook',methods= ['POST','GET'])
def webhook():
    if request.method == 'POST':
        Name = request.form['Name']
        Email = request.form['Email']
        Mobile = request.form['Mobile']
        city = request.form['city']
        resp = make_response(render_template('flask.html'))
    return  resp
    
if __name__ == '__main__':
    app.run(debug=False)