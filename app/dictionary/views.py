# app/home/views.py

from flask import render_template
from flask_login import login_required

from . import dictionary

@dictionary.route('/')
def index():
    """
    Render the homepage template on the / route
    """
    return render_template('dictionary/index.html', title="Welcome")
