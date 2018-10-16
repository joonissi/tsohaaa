from application import app, db, bcrypt
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
#from flask_bcrypt import Bcrypt

from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
import os
import hashlib
import uuid

from application.auth.models import User, conversations
from application.photos.models import Photo
from application.message.models import Message

from application.auth.forms import AccountForm, RegisterForm, LoginForm, MessageForm

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
    account = User.query.filter_by(email=form.email.data).first()
    
    if account and account.username == form.username.data:
      return render_template("auth/registerform.html", form = form, message="Username already in use")
    
    if account and account.email == form.email.data:
      return render_template("auth/registerform.html", form=form, message="Email already in use")

    # validate form
    if not form.validate():
      return render_template("auth/registerform.html", form=form)

    # Proceed with registration
    pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    account = User(form.username.data, pw_hash, form.email.data)

    db.session().add(account)
    db.session().commit()

    account = User.query.filter_by(username=form.username.data).first()

    photo = Photo('88f532fb-b66d-4e4f-824f-1fff9e825a20.jpg',
                  'deetailit', True)
    photo.account_id = account.id

    db.session().add(photo)
    db.session().commit()

    return redirect(url_for("users_index"))



# Login
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
  if request.method == "GET":
    return render_template("auth/loginform.html", form = LoginForm())

  form = LoginForm(request.form)
  # TODO validation

  user = User.query.filter_by(username=form.username.data).first()
  if not user:
    return render_template("auth/loginform.html", form=form,
                            message="No such username or password")
  
  if bcrypt.check_password_hash(user.password, form.password.data) == False:
    return render_template("auth/loginform.html", form = form,
                            message = "Incorrect username or password")
  
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

  if current_user.get_id() == None:
    accounts = User.find_all_users_with_user_photos()
    #account_id = current_user.get_id()
    #print(account_id)
    #accounts = User.find_all_users_with_user_photos_not_itself(account_id)
    

    return render_template("users/index.html", accounts=accounts)
  
  else:
    print(current_user)
    print(current_user.get_id())
    print("tanne")
    account_id = current_user.get_id()
    accounts = User.find_all_users_with_user_photos_not_itself(account_id)
    #accounts = User.find_all_users_with_user_photos()

    return render_template("users/index.html", accounts=accounts)


# Show user
@app.route("/users/<account_id>", methods=["GET", "POST"])
def users_show(account_id):

  if request.method == 'GET':
    account = User.query.get(account_id)
    photos = User.find_user_pictures(account_id)

    form = MessageForm()

    return render_template("users/show.html", account=account, form=form, photos=photos)

  else:
    form = MessageForm(request.form)

    # from_account = current_user
    # to_account = account = User.query.get(account_id)
    # print(form.message.data)
    # print("viestin lahettaa kayttaja: " + str(from_account.get_id()))
    # print("viesti lahetetaan kayttajalle: " + str(to_account.id))
    
    account_from = User.query.get(current_user.get_id())
    account_to = account = User.query.get(account_id)


    m = Message(form.message.data)
    
    account_from.conversations.append(m)
    account_to.conversations.append(m)




    #db.session().add(msg)
    db.session().commit()

    return redirect(url_for("users_index"))





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
    account.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
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
@app.route("/users/delete/<account_id>", methods=["GET"])
@login_required
def users_delete(account_id):
  
  user = User.query.get(account_id)

  db.session().delete(user)
  db.session().commit()

  return redirect(url_for('auth_login'))
