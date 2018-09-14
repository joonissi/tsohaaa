from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class AccountForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3)])
    password = PasswordField("Password", [validators.Length(min=6)])
    email = StringField("Email", [validators.Length(min=6)])
 
    class Meta:
        csrf = False