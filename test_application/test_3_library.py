import pytest
from application.book.models import Book
from application.library.models import Library

from test_application.test_1_users import test_client
    
url_library = "http://localhost:5000/library/"
url_users = "http://localhost:5000/users/"
url_books = "http://localhost:5000/books/"


# Get Library data
def test_library_home(test_client):
    response = test_client.get("http://localhost:5000/libraryhome")
    assert response.status_code == 200



# Get all users
def test_get_all_users(test_client):
    response = test_client.get(url_library+"/users", follow_redirects=True)
    assert response.status_code == 200


###### Parameterized fixture for inserting 3 users through library api
@pytest.mark.parametrize(
    "username, email, password, response_code",
    [("test1","test1@gmail.com", "123", 201),
    ("test2","test2@gmail.com", "123", 201),
    ("test3","test3@gmail.com", "123", 201)
    ],
    ids = ["TestCase-1","TestCase-2","TestCase-3"]
)
def test_post_user( username, email, password, response_code, test_client ):
    data = {
        "username":username,
        "email":email,
        "password":password
    }

    response = test_client.post(url_library+"/users", json = data, follow_redirects=True)
    assert response.status_code ==  response_code
  


# # Get all books
def test_get_books(test_client):
    response = test_client.get(url_library+"/books", follow_redirects = True)
    assert response.status_code == 200


# Parameterized fixture for inserting 3 books
@pytest.mark.parametrize(
    "bookname, publisher, author, response_code",
    [("book1","book1-publisher1", "author1", 201),
    ("book2","book2-publisher2", "author2", 201),
    ("book3","book3-publisher3", "author3", 201)
    ],
    ids = ["TestCase-1","TestCase-2","TestCase-3"]
)
def test_book_post( bookname, publisher, author, response_code, test_client ):
    data = {
        "bookname":bookname,
        "publisher":publisher,
        "author":author
    }

    response = test_client.post(url_library+"/books", json = data, follow_redirects=True)
    assert response.status_code ==  response_code
    

# Assigning book to specific user and delete assigned book
@pytest.mark.parametrize(
    "username, book_id,  response_code",
    [("test1", 1,  201),
     ("test1", 2, 201),
    ("test3", 3, 201)
    ],
    ids = ["TestCase-1","TestCase-2","TestCase-3"]
)
def test_book_assign( username, book_id, response_code, test_client ):
    data = {
        "username": username,
        "book_id": book_id
    }
    response_post = test_client.post(url_library+"users/"+username+"/books/{}".format(book_id), json = data, follow_redirects=True)
    response_get = test_client.get(url_library+"users/"+username)
    response_delete = test_client.delete(url_library+"users/"+username+"/books/{}".format(book_id), follow_redirects=True)

    #test unasingned book user
    response_invalid_get = test_client.get(url_library+"users/test2")
    #Asigning book to invalid user
    response_invalid_post = test_client.post(url_library+"users/"+"invalid_user"+"/books/{}".format(book_id), json = data, follow_redirects=True)

    assert response_post.status_code ==  response_code
    assert response_get.status_code == 200
    assert response_delete.status_code == response_code
    
    assert response_invalid_get.status_code == 400
    assert response_invalid_post.status_code ==  400


# Base fixture for book
@pytest.fixture( params= ["book1","book2","book3"])
def book_base_fixture(request):
    book_name= request.param
    required_book = Book.query.filter_by(bookname=book_name).first()
    return required_book.id
# Get specific book by id
def test_get_book(book_base_fixture, test_client):
    book_id = book_base_fixture
    response = test_client.get(url_library+"/books/{}".format(book_id), follow_redirects=True)
    assert response.status_code == 200

    
# Parametatrized funtion for deleting user
@pytest.fixture( params= ["test1", "test2", "test3"])
def user_base_fixture(request):
    return request.param

def test_delete_user(user_base_fixture, test_client):
    username = user_base_fixture
    test_client.delete(url_users+username)

    
# # Parametatrized funtion for deleting book
@pytest.fixture( params= ["book1", "book2", "book3"])
def book_base_fixture(request):
    book_name = request.param
    required_book = Book.query.filter_by(bookname=book_name).first()
    return required_book.id

def test_delete_book(book_base_fixture, test_client):
    book_id = book_base_fixture
    test_client.delete(url_books+"{}".format(book_id))
    
