from flask import Flask
from werkzeug.utils import import_string
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_babel import Babel, lazy_gettext as _l
from flask_moment import Moment
from config import Config

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message = _l('Please log in to access this page.')
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


blueprints = [
    'V2EX.main:main',
    'V2EX.admin:admin',
    'V2EX.user:user',
    #'V2EX.fun:fun',
    #'V2EX.job:job',
]

def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Load extensions
    db.init_app(app)
    #migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    # Load blueprints
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    return app