from flask import Flask, render_template, session, redirect, url_for
app = Flask(__name__)

@app.route('/index', methods=['GET', 'POST'])

def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('test.html', form=form, name=session.get('name'))
 


if __name__ == '__main__':
    app.run(debug=False)    
	
	
	