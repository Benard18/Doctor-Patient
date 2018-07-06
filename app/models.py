from . import db
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from time import time

@login_manager.user_loader
def load_user(user_id):
	return PatientUser.query.get(int(user_id))


class PatientUser(UserMixin, db.Model):
	__tablename__='patientuser'

	id= db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(255))
	first_name=db.Column(db.String(255))
	second_name=db.Column(db.String(255))
	pass_secure=db.Column(db.String(255))
	password_hash=db.Column(db.String(255))
	email=db.Column(db.String(255))
	feedback_patient=db.Column(db.String(255))
	patient_medical_prof=db.Column(db.String(255))
	messages_received = db.relationship('Message',foreign_keys='Message.recipient_id',backref='recipient', lazy='dynamic')
	last_message_read_time = db.Column(db.DateTime)
	messages_sent = db.relationship('Message',foreign_keys='Message.sender_id',backref='author', lazy='dynamic')
	notifications = db.relationship('Notification', backref='patientuser',lazy='dynamic')


	@property
	def password(self):
		raise AttributeError('You cannot read the password attribute')

	@password.setter
	def password(self, password):
		self.pass_secure = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.pass_secure, password)

	def __repr__(self):
		return f'PatientUser {self.username}'

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},
			app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			 id = jwt.decode(token, app.config['SECRET_KEY'],
					 algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

	def new_messages(self):
		last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
		return Message.query.filter_by(recipient=self).filter(Message.timestamp > last_read_time).count()

	def add_notification(self, name, data):
		self.notifications.filter_by(name=name).delete()
		n = Notification(name=name, payload_json=json.dumps(data), patientuser=self)
		db.session.add(n)
		return n


class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('patientuser.id'))
	recipient_id = db.Column(db.Integer, db.ForeignKey('patientuser.id'))
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	def __repr__(self):
		return '<Message {}>'.format(self.body)

class Notification(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('patientuser.id'))
	timestamp = db.Column(db.Float, index=True, default=time)
	payload_json = db.Column(db.Text)


	def get_data(self):
		return json.loads(str(self.payload_json))
