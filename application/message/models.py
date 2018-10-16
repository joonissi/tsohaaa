from application import db

from sqlalchemy.sql import text

from sqlalchemy import Text


class Message(db.Model):

    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text)
    
    #conversation_id = db.Column(db.Integer, nullable=False)

    #sender = db.relationship("Account", backref='message', lazy=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())


    def __init__(self, message):
      self.message = message


    @staticmethod
    def count_user_messages(account_id):
      stmt = text(
          "SELECT Account.username, COUNT(Conversations.account_id), COUNT(DISTINCT Conversations.account_id) AS notMe FROM Account"
          " LEFT JOIN Conversations ON Account.id=Conversations.account_id"
          " WHERE (Account.id = :account_id)"
          " GROUP BY username"
      ).params(account_id=account_id)

      res = db.engine.execute(stmt)

      result = []
      for row in res:
        result.append(row)
      #row = res.fetchone()
      #return row
      return result
