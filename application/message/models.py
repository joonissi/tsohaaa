from application import db
from application import participant

from sqlalchemy import Text


class Message(db.Model):

    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    #account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
    #                       nullable=False)
