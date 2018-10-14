from application import db

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
