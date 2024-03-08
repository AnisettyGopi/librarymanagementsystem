from flask import Blueprint, redirect, url_for, render_template, request, flash
from application.book.models import Book
from application import db
from application.book.forms import UpdateBookForm, BookRegistrationForm


# creating bluprint instance

books = Blueprint("books", __name__, template_folder="templates")


@books.route("/book", methods=["GET", "POST"])
def get_books():
    books = Book.query.all()
    form = BookRegistrationForm()
    if form.validate_on_submit():
        new_book = Book(
            bookname=form.bookname.data,
            publisher=form.publisher.data,
            author=form.author.data,
        )
        db.session.add(new_book)
        db.session.commit()
        flash("Book addded Successfully", "success")
        return redirect(url_for("books.get_books"))
    return render_template("book.html", books=books, form=form)


@books.route("/book/<int:id>", methods=["GET"])
def get_book(id):
    required_book = Book.query.get(id)
    if required_book:
        return render_template(
            "book_by_id.html", required_book=required_book, title="Book Details"
        )
    else:
        flash("Book Not Exists", "danger")
    return redirect(url_for("books.get_books"))


@books.route("/book/update/<int:id>", methods=["POST", "GET"])
def update_book(id):
    book_to_update = Book.query.get(id)
    if book_to_update:
        form = UpdateBookForm()
        if form.validate_on_submit():
            book_to_update.bookname = form.bookname.data
            book_to_update.publisher = form.publisher.data
            book_to_update.author = form.author.data
            db.session.commit()
            flash("Book update successfully", "success")
            return redirect(url_for("books.get_books"))
        elif request.method == "GET":
            form.bookname.data = book_to_update.bookname
            form.publisher.data = book_to_update.publisher
            form.author.data = book_to_update.author
        return render_template("update_book.html", form=form)
    else:
        flash("Book Not Exist!!", "danger")


@books.route("/book/delete/<int:id>", methods=["POST", "GET"])
def delete_book(id):
    book_to_delete = Book.query.get(id)
    if book_to_delete:
        db.session.delete(book_to_delete)
        db.session.commit()
        flash("Book deletd successfully", "success")
        return redirect(url_for("books.get_books"))
    else:
        flash("Book Not Exists or Already deleted", "danger")
