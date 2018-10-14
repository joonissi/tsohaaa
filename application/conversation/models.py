from application import db


class Conversation(db.Model):

    __tablename__ = 'conversation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
