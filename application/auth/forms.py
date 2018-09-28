from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms import StringField, PasswordField, TextField, validators

class MessageForm(FlaskForm):
    message = TextField("Message")

    class Meta:
        csrf = False


class AccountForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3)])
    password = PasswordField("Password", [validators.Length(min=6)])
    email = StringField("Email", [validators.Length(min=6)])

    photo = FileField()

    class Meta:
        csrf = False


class RegisterForm(FlaskForm):
    username = StringField("Username")
    email = StringField("Email", [validators.Length(min=6)])
    password = PasswordField("Password")
    password_confirmation = PasswordField("Confirm Password")

    class Meta:
        csrf = False


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False

