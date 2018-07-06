from flask import Flask
from flask_bootstrap import Bootstrap
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_mail import Mail





login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
bootstrap = Bootstrap()
db = SQLAlchemy()
photos = UploadSet('photos',IMAGES)
mail = Mail()

def create_app(config_name):

    app = Flask(__name__)
    # Creating the app configurations

    app.config.from_object(config_options[config_name])
    config_options[config_name].init_app(app)
    # Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .main import views
    views.configure_request(app)

    # from .auth2 import auth2 as auth2_blueprint
    # app.register_blueprint(auth2_blueprint,url_prefix = '/auth2')
    #

    # configure UploadSet
    configure_uploads(app,photos)



    return app
