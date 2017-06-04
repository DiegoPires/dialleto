# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, HiddenField, SelectField, StringField, SubmitField, ValidationError, FieldList, FormField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models.Lexicographer import Lexicographer

class LanguagemRegistrationForm(FlaskForm):
    language = HiddenField(validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    #first_name = StringField('First Name', validators=[DataRequired()])
    #last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')

    # TODO: Implement dynamic list for this: https://gist.github.com/kageurufu/6813878
    #properties = FieldList(FormField(PropertyForm), validators=[Optional()])

    language = SelectField(u'Language', choices=[], coerce=int)

    submit = SubmitField('Register')

    def validate_email(self, field):
        if Lexicographer.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Lexicographer.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')