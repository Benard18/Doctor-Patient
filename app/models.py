from . import db 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
	return PatientUser.query.get(int(user_id))

class Admin(UserMixin, db.Model):
	__tablename__='admin'

	id=db.Column(db.Integer, primary_key=True)
	adminname=db.Column(db.String(255))
	adminemail=db.Column(db.String(255))
	passwr=db.Column(db.String(255))
	passwr_secure=db.Column(db.String(255))

	@property
	def password(self):
		raise AttributeError('You cannot read the password attribute')

	@password.setter
	def password(self, password):
		self.passwr_secure = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.passwr_secure, password)

	def __repr__(self):
		return f'Admin {self.username}'


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


class DoctorUser(UserMixin, db.Model):
	__tablename__='doctoruser'

	id=db.Column(db.Integer, primary_key=True)
	medical_id=db.Column(db.String(255))
	doctorname=db.Column(db.String(255))
	passw_secure=db.Column(db.String(255))
	pass_hash=db.Column(db.String(255))
	docemail=db.Column(db.String(255))
	feedback_doctor=db.Column(db.String(255))




	@property
	def password(self):
		raise AttributeError('You cannot read the password attribute')

	@password.setter
	def password(self, password):
		self.passw_secure = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.passw_secure, password)

	def __repr__(self):
		return f'DoctorUser {self.doctorname}'


