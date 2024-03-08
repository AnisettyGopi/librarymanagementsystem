import re
from flask import make_response, jsonify
from application import app


def check_user_email(user_email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, user_email):
        return True
    return False


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({"Error": "Page or url not exists "}), 404)


@app.errorhandler(405)
def internal_server_error(error):
    return make_response(jsonify({"Error": "Invalid method request from user"}), 405)


@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({"Error": "Internal Server error "}), 500)


# @app.errorhandler(565)
# def connection_error(error):
#     return make_response(jsonify({"Error": "Connection missied"}), 565)
