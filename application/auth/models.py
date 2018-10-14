from application import db

from sqlalchemy.sql import text

conversations = db.Table('conversations',
                db.Column('account_id', db.Integer, db.ForeignKey(
                    'account.id'), primary_key=True),
                db.Column('message_id', db.Integer, db.ForeignKey(
                    'message.id'), primary_key=True)
                )


class User(db.Model):

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(144), unique=True, nullable=False)
    password = db.Column(db.String(144), nullable=False)
    email = db.Column(db.String(144), nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    photos = db.relationship("Photo", backref='account', lazy=True)

    conversations = db.relationship("Message", secondary="conversations", backref="account")


    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def get_id(self):
      return self.id

    def is_active(self):
      return True

    def is_anonymous(self):
      return False

    def is_authenticated(self):
      return True

    

    @staticmethod
    def find_all_users_with_user_photos():
      stmt = text(
          "SELECT Account.id, Account.username, Account.password, Account.email, Photo.link FROM Account"
          " LEFT JOIN Photo ON Account.id = Photo.account_id")

      res = db.engine.execute(stmt)

      response = []
      for row in res:
          response.append(
              {"id": row[0], "username": row[1], "password": row[2], "email": row[3], "photo": row[4]})

      return response

    @staticmethod
    def find_all_users_with_user_photos_not_itself(account_id):
      stmt = text(
          "SELECT Account.id, Account.username, Account.password, Account.email, Photo.link FROM Account"
          " LEFT JOIN Photo ON Account.id = Photo.account_id"
          " WHERE (Account.id != :account_id)"
        ).params(account_id=account_id)

      res = db.engine.execute(stmt)

      response = []
      for row in res:
          response.append(
              {"id": row[0], "username": row[1], "password": row[2], "email": row[3], "photo": row[4]})

      return response

    @staticmethod
    def find_user_with_pictures(account_id):
      stmt = text(
        "SELECT Account.id, Account.username, Account.email, Photo.link FROM Account"
        " LEFT JOIN Photo ON Account.id = Photo.account_id"
        " WHERE (Account.id IS :account_id)"
      ).params(account_id=account_id)

      res = db.engine.execute(stmt)

      response = []
      for row in res:
        response.append(
          {"id": row[0], "username": row[1], "email": row[2], "photo_link": row[3]})

      print(response)

      return response

    
    @staticmethod
    def find_user_pictures(account_id):
      stmt = text(
        "SELECT Photo.link FROM Account"
        " LEFT JOIN Photo ON Account.id = Photo.account_id"
        " WHERE (Account.id = :account_id)"
      ).params(account_id=account_id)

      res = db.engine.execute(stmt)

      response = []
      for row in res:
        response.append(
          {"photo_link": row[0]})

      print(response)

      return response
