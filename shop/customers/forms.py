from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from .model import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField(_l('Name: '))
    email = StringField(_l('Email: '), [validators.Email(), validators.DataRequired()])
    password = PasswordField(_l('Password: '), [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField(_l('Repeat Password: '), [validators.DataRequired()])
    city = StringField(_l('City: '), [validators.DataRequired()])
    contact = StringField(_l('Contact: '), [validators.DataRequired()])
    address = StringField(_l('Address: '), [validators.DataRequired()])
    submit = SubmitField(_l('Register'))

    def validate_username(self, name):
        if Register.query.filter_by(name=name.data).first():
            raise ValidationError(_l("This name is already in use!"))

    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError(_l("This email address is already in use!"))




class CustomerLoginFrom(FlaskForm):
    email = StringField(_l('Email: '), [validators.Email(), validators.DataRequired()])
    password = PasswordField(_l('Password: '), [validators.DataRequired()])
