from flask import Blueprint, redirect, render_template, url_for, flash, request
from application import db
from application.library.models import Library
from application.book.models import Book
from application.user.models import User
from application.book.routes import get_book, get_books
from application.user.routes import user_route
from application.library.forms import AssignBookForm


# create blue print

libraries = Blueprint("libraries", __name__, template_folder="templates")


@libraries.route("/library", methods=["POST", "GET"])
def library_home():
    librarians = Library.query.all()
    form = AssignBookForm()
    if form.validate_on_submit():
        exist_book = Book.query.get(request.form.get("book_id", type=int))
        if exist_book:
            new_library_user = Library(
                username=form.username.data,
                book_id=request.form.get("book_id", type=int),
            )
            db.session.add(new_library_user)
            db.session.commit()
            db.session.close()
            flash("Assign book successfully", "success")
            return redirect(url_for("libraries.library_home"))
        else:
            flash("Book Not Exists", "danger")

    return render_template("library.html", librarians=librarians, form=form)


# Get all books in the library
@libraries.route("/library/book", methods=["POST", "GET"])
def library_books():
    return get_books()


# Get all users in the library
@libraries.route("/library/user", methods=["POST", "GET"])
def library_users():
    return user_route()


# Get a library book by id
@libraries.route("/library/book/<int:id>", methods=["POST", "GET"])
def library_book_id(id):
    return get_book(id)


# register a book to specific user
@libraries.route(
    "/library/user/<string:user_name>/book/<int:bookId>", methods=["POST", "GET"]
)
def assign_book(user_name, bookId):
    exist_user = User.query.filter_by(username=user_name).first()
    exist_book = Book.query.filter_by(book_id=bookId)

    if exist_user and exist_book:
        library_user = Library(username=user_name, book_id=bookId)
        db.session.add(library_user)
        db.session.commit()
        flash("Assign book successfully", "success")
        return redirect(url_for("libraries.library_home"))
    else:
        flash("Invalid user or Invalid Book Id", "danger")
        return redirect(url_for("libraries.library_home"))


# delete the registered id
@libraries.route("/library/delete/<int:id>", methods=["GET", "POST"])
def library_delete_user(id):
    librarian_to_delete = Library.query.get(id)
    if librarian_to_delete:
        db.session.delete(librarian_to_delete)
        db.session.commit()
        flash("User Deleted", "success")
        return redirect(url_for("libraries.library_home"))
    else:
        flash("Invalid Id", "danger")
        return redirect(url_for("libraries.library_home"))


# check user assign  books
@libraries.route("/library/user/<string:user_name>", methods=["POST", "GET"])
def user_assigned_books(user_name):
    users = Library.query.filter_by(username=user_name)
    library_user = User.query.filter_by(username=user_name).first()
    book_ids = []
    for user in users:
        book_ids.append(user.book_id)

    books = []
    for i in book_ids:
        book = Book.query.get(i)
        books.append(book)
    return render_template(
        "user_assign_books.html",
        books=books,
        title="User Books",
        library_user=library_user,
    )
