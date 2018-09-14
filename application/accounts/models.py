from application import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    email = db.Column(db.String(144), nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

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