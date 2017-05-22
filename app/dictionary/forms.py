# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchWordForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])

class WordForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    word = StringField('Word', validators=[DataRequired()])
    definition = StringField('Definition', validators=[DataRequired()])
    submit = SubmitField('Submit')