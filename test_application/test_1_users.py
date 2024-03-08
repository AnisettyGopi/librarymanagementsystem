from codecs import ascii_encode
import json
import pytest
from application import app    


@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    with flask_app.test_client() as testing_client:
        yield testing_client


def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


url = "http://localhost:5000/users"
# 
# Invalid URl

invalid_url = "http:127.0.0.1:5000/user/"

def test_invalid_url(test_client):
    response = test_client.get(invalid_url)
    assert response.status_code == 404



# # Get all users
def test_get_users(test_client):
    response = test_client.get(url)
    assert response.status_code == 200


# Parameterized fixture for inserting 3 users
@pytest.mark.parametrize(
    "username, email, password, response_code",
    [("test1","test1@gmail.com", "123", 201),
    ("test2","test2@gmail.com", "123", 201),
    ("test3","test3@gmail.com", "123", 201)
    ],
    ids = ["TestCase-1","TestCase-2","TestCase-3"]
)
def test_user_post( username, email, password, response_code, test_client):
    data = {
        "username":username,
        "email":email,
        "password":password
    }
    test_user = {
        "username":"test4",
        "email":"test4@gmail.com",
        "password":"1234"
    }
    response = test_client.post(url, json = data)
    assert response.status_code ==  response_code
    test_client.post(url, json=test_user )


# # Parametatrized funtion for deleting user
@pytest.fixture( params= ["test1", "test2", "test3"])
def user_base_fixture(request):
    return request.param

# Get specific user by name
def test_get_user(user_base_fixture,  test_client):
    username = user_base_fixture 
    response = test_client.get(url+"/"+username)
    assert response.status_code == 200

# Delete user by username
def test_delete_user(user_base_fixture, test_client):
    username = user_base_fixture
    response = test_client.delete(url+"/"+username)
    assert response.status_code == 200


#update User
update_Gopi = {
    "username":"test4updated",
    "email":"test4updated@gmail.com",
    "password":"1234"
}
def test_update_user(test_client):
    response = test_client.put(url+"/test4", json=update_Gopi)
    assert response.status_code == 200
    # test_client.delete(url+"/test4updated")


# Fixture for invalid data requests
@pytest.mark.parametrize("username, email, password", [
    ("", "exam@gmail.com", "password"),
    ("user", "", "password"),
    ("user", "exam@gmail.com", ""),
    ("test4updated", "exam@gmail.com", "password"),
    ("user1", "test4updated@gmail.com", "password"),
],
ids=["Test1", "Test2", "Test3", "Test4", "Test5"]
)
# Test all invalid data requests
def test_user_invalid_data_request(username, email, password, test_client):
    data = {
        "username":username,
        "email":email,
        "password":password
    }
    response_post = test_client.post(url, json = data)
    response_get  = test_client.get(url+"/notexistuser")

    assert response_post.status_code ==  400
    assert response_get.status_code == 400
   


# Delete updated user and delete non existing user
def test_delete_updated_user(test_client):
    data = {
    }
    response_put = test_client.put(url+"/tes4updated", json = data)
    response_valid_delete =  test_client.delete(url+"/test4updated")
    response_invalid_delete = test_client.delete(url+"/test4")

    assert response_valid_delete.status_code == 200
    assert response_invalid_delete.status_code == 400
    assert response_put.status_code == 400