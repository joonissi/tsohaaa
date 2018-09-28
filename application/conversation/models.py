from application import db


participant = db.Table('participant', db.Model.metadata,
                             db.Column('conversation', db.Integer,
                                       db.ForeignKey('conversation.id')),
                             db.Column('message', db.Integer,
                                       db.ForeignKey('message.id'))
                             )

class Conversation(db.Model):

    __tablename__ = 'conversation'

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    message = db.relationship("Message", secondary=participant)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)

