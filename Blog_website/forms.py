from Blog_website.models import User, Comment, Blog

from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Length, EqualTo, Email, DataRequired

class LoginForm(FlaskForm):
    email = StringField(label='Email: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class RegisterForm(FlaskForm):
    username = StringField(label='User name: ',validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email: ', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password: ', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label='Confirm password: ', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')


    def validate_username(self, field):
        user = User.query.filter_by(name=field.data).first()
        if user:
            raise ValidationError('Username already in use')


    def validate_email_adress(self, field):
        email = User.query.filter_by(email=field.data).first()
        if email:
            raise ValidationError('Email already in use')