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
    
    conversations = account.conversations

    print(current_user.id)
    print(account.id)

    message_count = Message.count_user_messages(current_user.get_id())
    print(message_count)

    return render_template("messages/index.html", conversations=conversations, message_count=message_count)

  else:
    return redirect(url_for("users_index"))
