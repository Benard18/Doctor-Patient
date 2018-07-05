from flask import render_template,request
from . import main
from ..requests import sendemail
from flask_login import current_user,login_required
from ..models import DoctorUser


@main.route('/')
def index():
	title="Doctors"
	return render_template("index.html",title=title)