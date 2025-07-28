from flask import Blueprint
from app.controllers.login import login_view
from app.controllers.dashboard import dashboard_view, logout_view
from app.controllers.users import users_view
from app.controllers.photo import form_photo,load_photo
from app.controllers.create_user import create_user

main = Blueprint("main", __name__)

main.route("/", methods=["GET", "POST"])(login_view)
main.route("/dashboard")(dashboard_view)
main.route("/logout")(logout_view)
main.route("/users")(users_view)
main.route("/create_user")(create_user)
main.route("/form_photo")(form_photo)

main.route("/load_photo",methods=["POST"])(load_photo)

