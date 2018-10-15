from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
import os
import hashlib
import uuid

from application.auth.models import User
from application.photos.models import Photo
from application.message.models import Message

from application.auth.forms import AccountForm, RegisterForm, LoginForm, MessageForm


# List conversations
@app.route("/messages", methods=["GET", "POST"])
def messages_index():
  #messages = current_user.conversations
  #if current_user != None:
  if current_user.get_id() != None:
    account = User.query.get(current_user.get_id())
    
    messages = account.conversations

    return render_template("messages/index.html", messages=messages)

  else:
    return redirect(url_for("users_index"))