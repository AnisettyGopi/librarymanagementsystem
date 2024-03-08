from flask_wtf import FlaskForm
from application.book.models import Book
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class BookRegistrationForm(FlaskForm):
    bookname = StringField("Book Name", validators=[DataRequired()])
    publisher = StringField("Publisher", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    submit = SubmitField("Register Book")

    def validate_bookname(self, bookname):
        book = Book.query.filter_by(bookname=bookname.data).first()
        if book:
            raise ValidationError("That Book is already registered")


class UpdateBookForm(FlaskForm):
    bookname = StringField("Book Name", validators=[DataRequired()])
    publisher = StringField("Publisher", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    submit = SubmitField("Update Book")

    def validate_bookname(self, bookname):
        book = Book.query.filter_by(bookname=bookname.data).first()
        if book:
            raise ValidationError("That Book is already registered")
