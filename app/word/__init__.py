# app/word/__init__.py

from flask import Blueprint

word_blueprint = Blueprint('word', __name__)

from . import views