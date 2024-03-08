from application import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    books = db.relationship("Book", backref="user_name")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
