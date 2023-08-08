from wtforms import StringField, PasswordField,SubmitField,validators, ValidationError 
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from .model import Customer


class CustomerRegisterForm(FlaskForm):
    name = StringField(_l('Name: '))
    password = PasswordField(_l('Password: '), [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField(_l('Repeat Password: '), [validators.DataRequired()])
    contact = StringField(_l('Contact: '), [validators.DataRequired()])
    address = StringField(_l('Address: '), [validators.DataRequired()])
    submit = SubmitField(_l('Register'))

    def validate_username(self, name):
        if Customer.query.filter_by(name=name.data).first():
            raise ValidationError(_l("This name is already in use!"))

    def validate_email(self, contact):
        if Customer.query.filter_by(contact=contact.data).first():
            raise ValidationError(_l("This phone number is already in use!"))




class CustomerLoginFrom(FlaskForm):
    contact = StringField(_l('Contact: '), [validators.DataRequired()])
    password = PasswordField(_l('Password: '), [validators.DataRequired()])
