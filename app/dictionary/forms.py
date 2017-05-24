# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchWordForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])

class WordForm(FlaskForm):

    word = StringField('Word', validators=[DataRequired()])
    definition = StringField('Definition', validators=[DataRequired()])
    example = StringField('Example', validators=[DataRequired()])
    #language = StringField("Language", validators=[DataRequired()])
    submit = SubmitField('Submit')