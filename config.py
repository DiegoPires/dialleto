# config.py
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    Common configurations
    """
    # Put any configurations here that are common across all environments

    # pagination
    POSTS_PER_PAGE = 3

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    # http://flask.pocoo.org/docs/0.11/config/
    # http://flask-sqlalchemy.pocoo.org/2.1/config/

    DEBUG = True
    SQLALCHEMY_ECHO = True



class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}