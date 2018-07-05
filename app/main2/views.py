from flask import render_template,redirect,url_for,flash,request
from . import main2
from flask_login import login_user,logout_user,login_required
from ..models import DoctorUser
from .forms import LoginForms,RegistrationForms
from .. import db



#login
@main2.route('/logins',methods=['GET','POST'])
def login():
    login_forms = LoginForms()
    if login_forms.validate_on_submit():
        user = DoctorUser.query.filter_by(docemail = login_forms.email.data).first()
        if user is not None and user.verify_password(login_forms.password.data):
            login_user(user,login_forms.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or Password')
    title = "One-Minute login"
    return render_template('auth2/login.html',login_forms = login_forms,title=title)

#logout
@main2.route('/logouts')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out')
    return redirect(url_for("main.index"))



#register
@main2.route('/registers',methods = ["GET","POST"])
def register():
    form = RegistrationForms()
    if form.validate_on_submit():
        user = DoctorUser(docemail = form.email.data,password = form.password.data,medical_id=form.medical_id.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main2.login'))
        title = "New Account"
    return render_template('auth2/register.html',registration_forms = form)
