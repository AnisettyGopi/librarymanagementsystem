from application import user_api
from application.user.views import UserView, UserDetailView, HomeView

# Get Home view
user_api.add_resource(HomeView, "/")


# Get all users and post new user
user_api.add_resource(UserView, "/users")

# Get user, update and delete using username
user_api.add_resource(UserDetailView, "/users/<string:user_name>")
