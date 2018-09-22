from application import db

class Photo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(150), nullable=False)
    details = db.Column(db.String(250))
    active = db.Column(db.Boolean, nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                            nullable=False)

    def __init__(self, link, details, active):
        self.link = link
        self.details = details
        self.active = active