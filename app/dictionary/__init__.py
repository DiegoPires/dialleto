# app/dictionary/__init__.py

from flask import Blueprint

dic_blueprint = Blueprint('dictionary', __name__)

from . import views