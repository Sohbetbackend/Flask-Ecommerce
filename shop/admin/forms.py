from wtforms import StringField, PasswordField, validators , ValidationError
from flask_wtf import FlaskForm
from .models import User
from wtforms import Form, IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf.file import FileField,FileRequired,FileAllowed


class RegistrationForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Your Password', [validators.DataRequired()])


class Addcat(Form):
    name = StringField('Name', [validators.DataRequired()])
    image_category = FileField('Image Category', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif','jpeg'])])


class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg']), 'Images only please'])


class Addbanner(Form):
    name = StringField('Name', [validators.DataRequired()])
    image_banner = FileField('Image Banner', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif','jpeg'])])