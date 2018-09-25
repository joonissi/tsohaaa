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
from application.auth.forms import AccountForm, RegisterForm,LoginForm

# Register
@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
  if request.method == "GET":
    return render_template("auth/registerform.html", form = RegisterForm())

  else:
    form = RegisterForm()

    if (form.password.data != form.password_confirmation.data):
      return render_template("auth/registerform.html", form = form, message= "Passwords does not match!")

    # check if account already exists
    account = User.query.filter_by(username=form.username.data).first()
    
    if account:
      return render_template("auth/registerform.html", form = form, message="Username already in use")

    # validate form
    if not form.validate():
      return render_template("auth/registerform.html", form=form)

    # Proceed with registration
    account = User(form.username.data, form.password.data, form.email.data)

    db.session().add(account)
    db.session().commit()

    return redirect(url_for("users_index"))



# Login
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
  if request.method == "GET":
    return render_template("auth/loginform.html", form = LoginForm())

  form = LoginForm(request.form)
  # TODO validation

  user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
  if not user:
    return render_template("auth/loginform.html", form = form,
                            message = "No such username or password")
  
  login_user(user)
  return redirect(url_for("index"))

# Logout
@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

# List users
@app.route("/users", methods=["GET"])
def users_index():

  accounts = User.find_all_users_with_user_photos()

  return render_template("users/index.html", accounts=accounts)

# Edit user
@app.route("/users/edit/<account_id>", methods=["GET", "POST"])
@login_required
def users_update(account_id):

  # if method is GET
  if request.method == 'GET':
    account = User.query.get(account_id)
    #account = User.find_user_with_pictures(account_id)
    photos = User.find_user_pictures(account_id)
    
    form = AccountForm()

    form.username.data = account.username
    form.email.data = account.email

    return render_template("users/edit.html", account=account, form=form, photos=photos)

  else:
    form = AccountForm(CombinedMultiDict((request.files, request.form)))

    account = User.query.filter_by(username=form.username.data).first()
    photos = User.find_user_pictures(account_id)

    if not form.validate():
      return render_template("users/edit.html", account=account, form=form, photos=photos)

    #account = User(form.username.data, form.password.data, form.email.data)
    account.password = form.password.data
    account.email = form.email.data

    f = form.photo.data
    filename = secure_filename(f.filename)
    extension = filename.split(".")
    extension = extension[1]

    hashed_filename = str(uuid.uuid4()) + "." + extension

    f.save(os.getcwd() + "/application/static/images/" + hashed_filename)
    photo = Photo(hashed_filename, 'deetailit', True)
    photo.account_id = current_user.id

    db.session().add(photo)
    db.session().add(account)
    db.session().commit()


    return redirect(url_for("users_index"))


# Delete user


