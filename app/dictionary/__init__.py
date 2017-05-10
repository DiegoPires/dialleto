# app/dictionary/__init__.py

from flask import Blueprint

dictionary = Blueprint('dictionary', __name__)

from . import views