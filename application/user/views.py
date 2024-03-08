from application import ma, db
from flask_restful import Resource
from flask import request
from application.user.models import User
from application.error_handling import *


# creating user schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ("username", "email", "password")


user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Home View
class HomeView(Resource):
    def get(self):
        return {"message:": "Home Page"}, 200


# create User View Api
class UserView(Resource):
    def get(self):
        users = User.query.all()
        response = UserSchema(users, many=True)
        return response, 200

    def post(self):
        try:
            username = request.json["username"]
            if len(username) == 0:
                return {"message": "User name can't be empty"}, 400
            email = request.json["email"]
            # check valid email
            if not check_user_email(email):
                return {"message": "Invalid mail"}, 400
            password = request.json["password"]
            # check password
            if len(password) == 0:
                return {"message": "Password cannot be empty"}, 400
            # checking wheather the user_name and email exists or not
            exist_user_name = User.query.filter_by(username=username).first()
            exist_user_email = User.query.filter_by(email=email).first()
            if exist_user_name:
                return {"message": "User name already exists"}, 400
            if exist_user_email:
                return {"message": "Email already exists"}, 400
            else:
                # create an instance for new_user
                new_user = User(username, email, password)
                db.session.add(new_user)
                db.session.commit()
                return {"message": "User added succesfully"}, 201
        except Exception as e:
            return {"message": " Invalid data request by user "}, 400


# creating user detail view api
class UserDetailView(Resource):
    def get(self, user_name):
        exist_user = User.query.filter_by(username=user_name).first()
        if exist_user:
            return user_schema.jsonify({exist_user}, 200)
        else:
            return {"message": "User not exists"}, 400

    def put(self, user_name):
        try:
            username = request.json["username"]
            if len(username) == 0:
                return {"message": "User name can't be empty"}, 400
            email = request.json["email"]
            if not check_user_email(email):
                return {"message": " Invalid mail"}, 400
            password = request.json["password"]
            # check password
            if len(password) == 0:
                return {"message": "Password cannot be empty"}, 400
            updated_user = User.query.filter_by(username=user_name).first()
            if updated_user:
                updated_user.username = username
                updated_user.email = email
                updated_user.password = password
                db.session.commit()
                return {
                    "message": "User ---> " + username + " <--- is updated sucessfully"
                }, 200
            else:
                return {"message": " Invalid username"}, 400
        except Exception as e:
            return {"message": "Invalid data request by user"}, 400

    def delete(self, user_name):
        delete_user = User.query.filter_by(username=user_name).first()
        if delete_user:
            db.session.delete(delete_user)
            db.session.commit()
            return {
                "message": "User --> " + user_name + " <-- deleted successfully"
            }, 200

        else:
            return {"message": "Invalid User"}, 400
