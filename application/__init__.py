from flask import Flask

import os
from werkzeug.utils import secure_filename

#UPLOAD_FOLDER = '/uploads'
UPLOAD_FOLDER = os.getcwd() + "/uploads/"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_url_path='/static')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
  app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views

from application.auth import models
from application.auth import views

from application.photos import models

from application.auth.models import User

from application.conversation.models import Conversation
from application.conversation.models import participant

from application.message.models import Message

from os import urandom

app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)



try:
    db.create_all()
except:
    pass

