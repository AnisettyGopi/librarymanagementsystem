from requests import delete
from application import db, ma
from flask_restful import Resource
from application.library.models import Library
from application.book.models import Book
from application.user.models import User
from application.book.views import (
    book_schema,
    books_schema,
    BookAPIView,
    BookDetailView,
)
from application.user.views import UserView, UserDetailView

# creating library schema
class LibrarySchema(ma.Schema):
    class Meta:
        fields = ("username", "book_id")


lib_user = LibrarySchema()
lib_users = LibrarySchema(many=True)

# Get all users with thier assigned book Ids
class LibraryHomeView(Resource):
    def get(self):
        librarians = Library.query.all()
        response = lib_users.dump(librarians)
        return response, 200
        
# Get all the users
class LibraryUsersView(Resource):
    def get(self):
        obj = UserView()
        return obj.get()

    def post(self):
        obj = UserView()
        return obj.post()
    

# Get user with all Assigned books
class LibraryUsersAssignBook(Resource):
    def get(self, user_name):
        books = Library.query.filter_by(username=user_name)
        book_ids = []
        for book in books:
            book_ids.append(book.book_id)
        if len(book_ids) == 0:
            return {"message": "No book assigned"}, 400
        books = []
        for i in book_ids:
            book = Book.query.get(i)
            books.append(book)

        if len(books) == 1:
            return book_schema.jsonify({books[0]}, 200)
        else:
            response = books_schema.dump(books)
        return response, 200

    def delete(self, user_name):
        obj = UserDetailView()
        return obj.delete(user_name)

# Get all books  and add a book in library
class LibraryBooks(Resource):
    def get(self):
        obj = BookAPIView()
        return obj.get()

    def post(self):
        obj = BookAPIView()
        return obj.post()


# Get and delete a book by id
class LibraryBooksById(Resource):
    def get(self, id):
        obj = BookDetailView()
        return obj.get(id)

    def delete(self, id):
        obj = BookDetailView()
        return obj.delete(id)


# assign a book to user
class LibraryBookAssign(Resource):
    def post(self, user_name, bookId):
        try:
            exist_user = User.query.filter_by(username=user_name).first()
            exist_book = Book.query.get(bookId)
            if exist_user and exist_book:
                library_user = Library(username=user_name, book_id=bookId)
                db.session.add(library_user)
                db.session.commit()
                return {"message": "Book Asigned Successfully"}, 201
            elif not exist_user:
                return {"message": "Invalid Username"}, 400
            else:
                return {"message": "Invalid book Id"}, 400

        except Exception as e:
            return {"message": "Invalid Request"}, 400

    def delete(self, user_name, bookId):
        try:
            exist_user = User.query.filter_by(username=user_name).first()
            exist_book = Book.query.get(bookId)
            if exist_user and exist_book:
                library_user = Library.query.filter_by(username=user_name, book_id=bookId).first()
                db.session.delete(library_user)
                db.session.commit()
                return {"message": "Deleted assigned book Sucessfully"}, 201
            elif not exist_user:
                return {"message": "Invalid Username"}, 420
            else:
                return {"message": "Invalid book Id"}, 420

        except Exception as e:
            return {"message": "Invalid Request"}, 400