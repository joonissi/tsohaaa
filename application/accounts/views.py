from application import app, db
from flask import render_template, request, redirect, url_for
from application.accounts.models import Account
from application.accounts.forms import AccountForm

@app.route("/accounts", methods=["GET"])
def accounts_index():
  return render_template("accounts/index.html", accounts = Account.query.all())


@app.route("/accounts/new/")
def accounts_form():
    return render_template("accounts/new.html", form = AccountForm())


@app.route("/accounts/edit/<account_id>", methods=["GET", "POST"])
def accounts_update(account_id):

  # if method is GET
  if request.method == 'GET':
    my_account = Account.query.get(account_id)
    form = AccountForm()
    
    form.username.data = my_account.username
    
    # Not going to be displayed
    #form.password.data = account.password
    form.email.data = my_account.email

    return render_template("accounts/edit.html", account = my_account, form = form)

  else:
    form = AccountForm(request.form)

    my_account = Account.query.get(account_id)

    if not form.validate():
      return render_template("accounts/edit.html", account = my_account, form = form)

    # update fields
    #my_account.username = form.username.data
    my_account.password = form.password.data
    my_account.email = form.email.data

    db.session().commit()

    return redirect(url_for("accounts_index"))


@app.route("/accounts/", methods=["POST"])
def accounts_create():

    form = AccountForm(request.form)

    # check if account already exists
    account = Account.query.filter_by(username=form.username.data).first()
    if account:
      # TODO show warning text
      return render_template("accounts/new.html", form=form)

    if not form.validate():
      return render_template("accounts/new.html", form = form)

    account = Account(form.username.data, form.password.data, form.email.data)
    
    if (account == None):
      db.session().add(account)
      db.session().commit()
  
    return redirect(url_for("accounts_index"))
  
