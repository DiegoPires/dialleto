# app/word/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField, SelectField, \
    HiddenField, validators, SelectMultipleField, IntegerField

from wtforms.widgets import ListWidget,CheckboxInput

from wtforms.validators import DataRequired
from ..models.Language import Language

class SearchWordForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])

class WordForm(FlaskForm):

    word_id = HiddenField("WordId")

    word = StringField('Word', [validators.required(), validators.length(max=60)])
    definition = TextAreaField('Definition', [validators.required(), validators.length(max=200)])
    example = TextAreaField('Example', [validators.required(), validators.length(max=200)])
    language = SelectField(u'Language', choices=[], coerce=int)

    submit = SubmitField('Submit')

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class RelatedWordForm(FlaskForm):

    word = HiddenField("Word")
    words = MultiCheckboxField(coerce=int)

    submit = SubmitField('Submit')


