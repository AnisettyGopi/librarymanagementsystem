from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
app.app_context().push()

app.config["SECRET_KEY"] = "ddbc03578e0c7c561427d814a059ea02"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"


db = SQLAlchemy(app)
ma = Marshmallow(app)

user_api = Api(app)
book_api = Api(app)
library_api = Api(app)

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app-name": "Library Management System"}
)


from application.user.routes import users
from application.book.routes import books
from application.library.routes import libraries


from application.user import views, urls
from application.book import views, urls
from application.library import views, urls
from middleware import *

app.register_blueprint(users)
app.register_blueprint(books)
app.register_blueprint(libraries)
app.register_blueprint(swagger_blueprint)

db.create_all()
