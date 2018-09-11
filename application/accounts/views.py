from application import app, db
from flask import render_template, request, redirect, url_for
from application.accounts.models import Account

@app.route("/accounts", methods=["GET"])
def accounts_index():
  return render_template("accounts/index.html", accounts = Account.query.all())

@app.route("/accounts/new/")
def accounts_form():
    return render_template("accounts/new.html")

@app.route("/accounts/edit/<account_id>")
def accounts_update(account_id):

  #if method is GET
  a = Account.query.get(account_id)

  return render_template("accounts/edit.html", account = a)

  #else if method is POST
  # TODO

@app.route("/accounts/", methods=["POST"])
def accounts_create():
    print(request.form.get("username"))

    a = Account(request.form.get("username"), request.form.get("password"), request.form.get("email"))
    #p = Account(request.form.get("password"))
    #e = Account(request.form.get("email"))
    
    db.session().add(a)
    db.session().commit()
  
    return redirect(url_for("accounts_index"))