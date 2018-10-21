from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms import StringField, PasswordField, TextField, validators


class SearchForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3, max=144)])

    class Meta:
        csrf = False

class MessageForm(FlaskForm):
    message = TextField("Message", [validators.Length(min=3, max=500)])

    class Meta:
        csrf = False


class AccountForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3, max=144)])
    password = PasswordField("Password", [validators.Length(min=6, max=144)])
    email = StringField("Email", [validators.Length(min=6, max=144)])

    photo = FileField()

    class Meta:
        csrf = False


class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3, max=144)])
    email = StringField("Email", [validators.Length(min=6, max=144)])
    password = PasswordField("Password", [validators.Length(min=3, max=144)])
    password_confirmation = PasswordField(
        "Confirm Password", [validators.Length(min=3, max=144)])

    class Meta:
        csrf = False


class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3, max=144)])
    password = PasswordField("Password", [validators.Length(min=3, max=144)])

    class Meta:
        csrf = False

