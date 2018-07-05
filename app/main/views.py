from flask import render_template,request,redirect,flash,url_for
from . import main
from ..requests import sendemail
from flask_login import current_user,login_required,login_user,logout_user
from ..models import DoctorUser,PatientUser
from .forms import LoginForm,RegistrationForm
from .. import db


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

@main.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = PatientUser.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or Password')
    title = "One-Minute login"
    return render_template('auth/login.html',login_form = login_form,title=title)

#logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out')
    return redirect(url_for("main.index"))

@main.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = PatientUser(email = form.email.data, username = form.username.data,password = form.password.data,first_name=form.first_name.data,second_name=form.second_name.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
        title = "New Account"
    return render_template('auth/register.html',registration_form = form)
