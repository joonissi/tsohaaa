from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from application.auth.models import User
from application.message.models import Message


# List conversations
@app.route("/messages", methods=["GET", "POST"])
@login_required
def messages_index():

  if current_user.get_id() != None:
    account = User.query.get_or_404(current_user.get_id())
    conversations = account.conversations
    message_count = Message.count_user_messages(current_user.get_id())

    return render_template("messages/index.html", conversations=conversations, message_count=message_count)

  else:
    return redirect(url_for("users_index"))
