from application import db


class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    bookname = db.Column(db.String(30), nullable=False, unique=True)
    publisher = db.Column(db.String(20), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), default=0)

    def __init__(self, bookname, publisher, author):
        self.bookname = bookname
        self.publisher = publisher
        self.author = author
