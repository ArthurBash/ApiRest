from flask import Blueprint
from app.controllers.login import login_view
from app.controllers.dashboard import dashboard_view, logout_view, get_single_photo_endpoint, get_photos_endpoint
from app.controllers.users import users_view, get_current_user_endpoint
from app.controllers.photo import load_photo, photo_proxy, proxy_get_folders, proxy_get_photos
from app.controllers.create_user import create_user

main = Blueprint("main", __name__)

# --- Rutas de Vistas (Páginas) ---
# Usando add_url_rule para mantener la consistencia
main.add_url_rule("/", view_func=login_view, methods=["GET", "POST"])
main.add_url_rule("/dashboard", view_func=dashboard_view, methods=["GET"])
main.add_url_rule("/logout", view_func=logout_view, methods=["GET"])
main.add_url_rule("/users", view_func=users_view, methods=["GET"])
main.add_url_rule("/create_user", view_func=create_user, methods=["GET", "POST"]) # Asumiendo GET y POST
main.add_url_rule("/load_photo", view_func=load_photo, methods=["GET", "POST"])

# --- Rutas de API y Proxies ---
main.add_url_rule("/api/photos", view_func=get_photos_endpoint, methods=["GET"])
main.add_url_rule("/api/photos/<int:photo_id>", view_func=get_single_photo_endpoint, methods=["GET"])
main.add_url_rule("/api/current-user", view_func=get_current_user_endpoint, methods=["GET"])

# Rutas del proxy
main.add_url_rule("/photo_proxy", view_func=photo_proxy, methods=["GET"])

main.add_url_rule("/api/folders", view_func=proxy_get_folders, methods=["GET"])

# ❗️ OJO: Corregí el error tipográfico de "photoo" a "photos" para que coincida con tu JS
main.add_url_rule("/api/photoss", view_func=proxy_get_photos, methods=["GET"]) 
