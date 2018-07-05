from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Email,Length,EqualTo
from ..models import PatientUser
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    password = PasswordField('Password',validators =[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	email = StringField('Your Email Address',validators=[Required(),Email()])
	username = StringField('Enter your username',validators = [Required()])
	first_name = StringField('Enter your First Name',validators = [Required()])
	second_name = StringField('Enter your Second Name',validators = [Required()])
	password = PasswordField('Password',validators = [Required(),
	EqualTo('password2',message = 'Passwords must match')])
	password2 = PasswordField('Confirm Password',validators = [Required()])
	submit = SubmitField('Sign Up')


	def validate_email(self,data_field):
		if PatientUser.query.filter_by(email =data_field.data).first():
			raise ValidationError('There is an account with that email')

	def validate_username(self,data_field):
		if PatientUser.query.filter_by(username = data_field.data).first():
			raise ValidationError('That username is taken')
