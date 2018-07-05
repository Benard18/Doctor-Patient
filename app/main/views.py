from flask import render_template,request
from . import main
from ..requests import sendemail
from flask_login import current_user,login_required
from ..models import DoctorUser



@main.route('/')
def index():
	title="Doctors"
	return render_template("index.html",title=title)

@main.route('/newappointment/',methods=["GET","POST"])
@login_required
def addappointment():
	start=request.form['start']
	end=request.form['end']
	email='ben.karanja@live.com'
	# patient=current_user.email
	currentuser=current_user.username

	sendemail(email,start,end,currentuser)

	title='Doctors'
	return render_template("index.html",title=title)
