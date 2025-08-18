from flask import Blueprint
from app.controllers.login import login_view
from app.controllers.dashboard import dashboard_view, logout_view,get_single_photo_endpoint,get_photos_endpoint
from app.controllers.users import users_view
from app.controllers.photo import form_photo,load_photo,photo_proxy
from app.controllers.create_user import create_user

main = Blueprint("main", __name__)

main.route("/", methods=["GET", "POST"])(login_view)
main.route("/dashboard")(dashboard_view)
main.route("/logout")(logout_view)
main.route("/users")(users_view)
main.route("/create_user")(create_user)
main.route("/form_photo")(form_photo)

main.route("/load_photo",methods=["POST"])(load_photo)

main.route("/api/photos", methods=["GET"])(get_photos_endpoint)
main.route("/api/photos/<int:photo_id>", methods=["GET"])(get_single_photo_endpoint)


main.route("/photo_proxy")(photo_proxy)
