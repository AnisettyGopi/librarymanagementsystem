from application.book.views import BookAPIView, BookDetailView
from application import book_api


book_api.add_resource(BookAPIView, "/books")
book_api.add_resource(BookDetailView, "/books/<int:id>")
