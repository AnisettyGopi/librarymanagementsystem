from application import library_api
from application.library.views import (
    LibraryHomeView,
    LibraryUsersView,
    LibraryBookAssign,
    LibraryBooks,
    LibraryUsersAssignBook,
    LibraryBooksById,
)


library_api.add_resource(LibraryHomeView, "/libraryhome")
library_api.add_resource(LibraryUsersView, "/library/users")
library_api.add_resource(LibraryUsersAssignBook, "/library/users/<string:user_name>")
library_api.add_resource(LibraryBooks, "/library/books")
library_api.add_resource(LibraryBooksById, "/library/books/<int:id>")
library_api.add_resource(
    LibraryBookAssign, "/library/users/<string:user_name>/books/<int:bookId>"
)
