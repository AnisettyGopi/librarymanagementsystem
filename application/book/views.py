from flask_restful import Resource
from application import ma, db
from application.book.models import Book
from flask import request
from application.error_handling import *


class BookSchema(ma.Schema):
    class Meta:
        fields = ("bookname", "publisher", "author", "user_id")


book_schema = BookSchema()
books_schema = BookSchema(many=True)


class BookAPIView(Resource):
    def get(self):
        books = Book.query.all()
        response = books_schema.dump(books)
        return response, 200

    def post(self):
        try:

            book_name = request.json["bookname"]
            if len(book_name) == 0:
                return {"message": "Book name should not be null"}, 400
            publisher = request.json["publisher"]
            if len(publisher) == 0:
                return {"message": "Publisher name should not be null"}, 400
            author = request.json["author"]
            if len(author) == 0:
                return {"message": "Author name should not be null"}, 400
            check_book = Book.query.filter_by(bookname=book_name).first()
            if check_book:
                return {"message ": "Book already Exists"}, 400

            else:
                new_book = Book(book_name, publisher, author)
                db.session.add(new_book)
                db.session.commit()
                return {
                    "message ": "Book by " + author + " registered successfully "
                }, 201
        except Exception as e:
            return {"message": "Invalid data request "}, 400


class BookDetailView(Resource):
    def get(self, id):
        required_book = Book.query.filter_by(id=id).first()
        if required_book:
            response = book_schema.jsonify({required_book}, 200)
            return response
        else:
            return {"message ": "Book not Exists "}, 400

    def put(self, id):
        try:
            update_book = Book.query.get(id)
            if update_book:
                update_book.bookname = request.json["bookname"]
                update_book.publisher = request.json["publisher"]
                update_book.author = request.json["author"]
                db.session.commit()
                return {"message": "Book updated successfully"}, 200
            else:
                return {"message": " Book not found"}, 400
        except Exception as e:
            return {"message": "Invalid request"}, 400

    def delete(self, id):
        delete_book = Book.query.get(id)
        if delete_book:
            db.session.delete(delete_book)
            db.session.commit()
            return {"message": "Book deleted successfully"}, 202
        else:
            return {"message ": "Invalid book id  "}, 400
