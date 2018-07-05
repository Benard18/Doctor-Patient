import os

class Config:
	SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://ben:ben@localhost/doctorpatient'
	SECRET_KEY='bleh'
	UPLOADED_PHOTOS_DEST = 'app/static/photos'
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
	MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
	SUBJECT_PREFIX = 'PITCH'
	SENDER_EMAIL = 'benkaranja43@gmail.com'



class ProdConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevConfig(Config):
	DEBUG = True



config_options = {
	'development': DevConfig,
	'production':ProdConfig
}
