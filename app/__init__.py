# app/__init__.py

# third-party imports
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

# local imports
from config import app_config


# db variable initialization
db = SQLAlchemy()
bootstrap = Bootstrap()

login_manager = LoginManager()


def before_request_function():
    from .dictionary.forms import SearchWordForm
    g.search_form = SearchWordForm()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # authentication config
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    from app.models.Rating import RatingType
    from app.models.Text import TextType

    from app.models import Language, Word, Lexicographer, BaseMixin, Rating, Text, Word

    bootstrap.init_app(app)

    # import blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .dictionary import dictionary as dic_blueprint
    app.register_blueprint(dic_blueprint)
    app.before_request(before_request_function)
    return app