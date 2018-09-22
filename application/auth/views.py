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
from application.auth.forms import AccountForm, LoginForm


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

  print("käyttäjä " + user.username + " tunnistettiin")
  
  login_user(user)
  return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/users", methods=["GET"])
def users_index():

  #user_photos = User.find_user_photos()
  accounts = User.find_all_users_with_user_photos()
  
  #file_path = os.path.join(app.config['UPLOAD_FOLDER'])

  return render_template("users/index.html", accounts=accounts)


@app.route("/users/new/")
@login_required
def users_form():
    return render_template("users/new.html", form=AccountForm())


@app.route("/users/edit/<account_id>", methods=["GET", "POST"])
@login_required
def users_update(account_id):

  # if method is GET
  if request.method == 'GET':
    my_account = User.query.get(account_id)
    form = AccountForm()

    form.username.data = my_account.username

    # Not going to be displayed
    #form.password.data = account.password
    form.email.data = my_account.email

    return render_template("users/edit.html", account=my_account, form=form)

  else:
    form = AccountForm(request.form)

    my_account = User.query.get(account_id)

    if not form.validate():
      return render_template("users/edit.html", account=my_account, form=form)

    # update fields
    #my_account.username = form.username.data
    my_account.password = form.password.data
    my_account.email = form.email.data

    db.session().commit()

    return redirect(url_for("users_index"))


@app.route("/users/", methods=["POST"])
@login_required
def users_create():

    #form = AccountForm(request.form)
    form = AccountForm(CombinedMultiDict((request.files, request.form)))

    # check if account already exists
    account = User.query.filter_by(username=form.username.data).first()
    if account:
      # TODO show warning text
      return render_template("users/new.html", form=form, message="Username already in use")

    # validate form
    if not form.validate():
      return render_template("users/new.html", form=form)

    account = User(form.username.data, form.password.data, form.email.data)




    f = form.photo.data
  
    filename = secure_filename(f.filename)
    
    extension = filename.split(".")
    extension = extension[1]

    hashed_filename = str(uuid.uuid4()) + "." + extension
    
    print(hashed_filename)

    f.save(os.getcwd() + "/application/static/images/" + hashed_filename)

    photo = Photo(hashed_filename, 'deetailit', True)
    photo.account_id = current_user.id

    db.session().add(photo)

    #if (account == None):
    db.session().add(account)
    db.session().commit()

    return redirect(url_for("users_index"))


