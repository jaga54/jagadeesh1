from flask import Flask,request,render_template,jsonify
app = Flask(__name__)

@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    return {
                "payload": {
                "google": {
                "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                        "textToSpeech": '''<form action = "/webhook" method = "POST">
	<div class = "form-group">
		<label for="Name"><b>Name:</b></label>
		<input type = "text" name ="Name" placeholder="Name"><br> 
		<label for="Email"><b>Email:</b></label>
		<input type ="text" name = "Email" placeholder="Email"><br>
		<label for="Mobile"><b>Mobile:</b></label>
		<input type ="number" name ="Mobile" placeholder="Mobile"><br> 
		<label for="city"><b>city:</b></label>
		<input type = "text" name ="city" placeholder="city"><br>
	</div>	
	<input class = "btn btn-primary" type = "submit" value = "submit">
   
</form>'''
                    }
                }
                ]
                
            }
            }
            }
            }

if __name__ == '__main__':
    app.run(debug=False)