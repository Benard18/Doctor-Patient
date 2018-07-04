from flask import render_template
from . import main




@main.route('/')
def index():
	title="Doctors"
	return render_template("index.html",title=title)


@main.route('/authdoc/login')
def logindoc():
	return render_template('login.html')



	
