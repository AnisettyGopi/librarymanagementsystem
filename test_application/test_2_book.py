from cgi import test
import pytest
from test_application.test_1_users import test_client 
from application.book.models import Book  
url = "http://localhost:5000/books"

# # Get all users
def test_get_books(test_client):
    response = test_client.get(url)
    assert response.status_code == 200


# Parameterized fixture for inserting 3 books
@pytest.mark.parametrize(
    "bookname, publisher, author, response_code",
    [("book1","book1-publisher1", "author1", 201),
    ("book2","book1-publisher2", "author2", 201),
    ("book3","book1-publisher3", "author3", 201)
    ],
    ids = ["TestCase-1","TestCase-2","TestCase-3"]
)
def test_book_post( bookname, publisher, author, response_code, test_client):
    data = {
        "bookname":bookname,
        "publisher":publisher,
        "author":author
    }
    test_book = {
        "bookname":"testbook",
        "publisher":"testpublisher",
        "author":"testauthor"
    }
    response = test_client.post(url, json = data)
    assert response.status_code ==  response_code
    test_client.post(url, json=test_book )


# # Parametatrized funtion for deleting book
@pytest.fixture( params= ["book1", "book2", "book3"])
def book_base_fixture(request):
    book_name = request.param
    required_book = Book.query.filter_by(bookname=book_name).first()
    return required_book.id

# Get specific book by id
def test_get_book(book_base_fixture, test_client):
    book_id = book_base_fixture
    response = test_client.get(url+"/{}".format(book_id))
    assert response.status_code == 200

# Delete book by id
def test_delete_book(book_base_fixture, test_client):
    book_id = book_base_fixture
    response = test_client.delete(url+"/{}".format(book_id))
    assert response.status_code == 202


# Posting invalid data requests
# Fixture for invalid data requests
@pytest.mark.parametrize("bookname, publisher, author", [
    ("", "com", "author"),
    ("name", "", "author"),
    ("name", "com", "")
    
],
ids=["Test1", "Test2", "Test3"]
)

# Test all invalid data requests
def test_user_invalid_data_request(bookname, publisher, author, test_client):
    data = {
        "bookname":bookname,
        "publisher":publisher,
        "author":author
    }
    response_post = test_client.post(url, json = data)
    # response_put = test_client.put(url, json = data)
    response_get  = test_client.get(url+"/{}".format(0))
    response_delete = test_client.delete(url+"/{}".format(0))

    assert response_post.status_code ==  400
    # assert response_put.status_code == 400
    assert response_get.status_code == 400
    assert response_delete.status_code == 400

#update book
update_book = {
    "bookname":"testbookUpdated",
    "publisher":"testpublisherUpdated",
    "author":"testauthorUpdated"
}
def test_update_book(test_client):
    required_book = Book.query.filter_by(bookname="testbook").first()
    book_id = required_book.id
    response = test_client.put(url+"/{}".format(book_id), json=update_book)
    assert response.status_code == 200
    test_client.delete(url+"/{}".format(book_id))

# 