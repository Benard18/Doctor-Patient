from flask import render_template,request,redirect,flash,url_for,jsonify
from . import main
from ..requests import sendemail
from flask_login import current_user,login_required,login_user,logout_user
from ..models import PatientUser,Message,Notification
from .forms import LoginForm,RegistrationForm,MessageForm
from .. import db
from datetime import datetime

post_per_page = None

def configure_request(app):
	global post_per_page
	post_per_page = app.config['POSTS_PER_PAGE']


@main.route('/')
def index():
	title="Doctors"
	return render_template("index.html",title=title)
@main.route('/appointment')
def appointment():
	title='Booking appointment'
	return render_template('form.html',title=title)
@main.route('/newappointment/',methods=["GET","POST"])
@login_required
def addappointment():

	start=request.form['start']
	end=request.form['end']
	email=request.form['email']
	# patient=current_user.email
	currentuser=current_user.username

	sendemail(email,start,end,currentuser)
	redirect(url_for('main.messages'))
	flash('Appointment sent')
	title='Doctors'
	return render_template("messages.html",title=title)

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

@main.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = PatientUser.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title=('Send Message'),form=form, recipient=recipient)


@main.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(page,post_per_page, False)
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,next_url=next_url, prev_url=prev_url)

@main.route('/user/<username>')
@login_required
def user(username):
    user = PatientUser.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
@main.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(Notification.timestamp > since).order_by(Notification.timestamp.asc())

    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
