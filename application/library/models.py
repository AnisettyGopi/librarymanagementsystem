from application import db


class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    book_id = db.Column(db.Integer, nullable=False)

    def __init__(self, username, book_id):
        self.username = username
        self.book_id = book_id
