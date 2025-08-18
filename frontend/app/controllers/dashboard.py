from flask import session, redirect, url_for, flash, render_template
from app.services.user_service import get_data_user,get_photos
from app.services.photo import PhotoAPIService
from flask import session, request, jsonify

photo_api_service = PhotoAPIService()

def dashboard_view():
    token = session.get("access_token")

    if not token:
        flash("Primero debes iniciar sesión", "warning")
        return redirect(url_for("main.login_view"))

    user, error = get_data_user(token)

    if error:
        flash(error, "danger")
        return redirect(url_for("main.login_view"))

    user_id = user.get("id") 
    return render_template("dashboard.html",
                            user=user,
                           user_id=user_id,
                           access_token=token)

def logout_view():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for("main.login_view"))




def get_photos_endpoint():
    """
    Endpoint para que el frontend JavaScript obtenga fotos
    Este endpoint actúa como proxy hacia FastAPI
    """
    token = session.get("access_token")
    
    if not token:
        return jsonify({"error": "No autenticado"}), 401
    
    # Obtener parámetros de query
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    folder_id = request.args.get('folder_id', type=int)  # None si no se envía
    
    # Llamar al microservicio FastAPI
    result = photo_api_service.get_photos(
        token=token,
        page=page,
        page_size=page_size,
        folder_id=folder_id
    )
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

def get_single_photo_endpoint(photo_id):
    """Endpoint para obtener una foto específica"""
    token = session.get("access_token")
    
    if not token:
        return jsonify({"error": "No autenticado"}), 401
    
    result = photo_api_service.get_single_photo(token, photo_id)
    
    if "error" in result:
        status = 404 if "no encontrada" in result["error"] else 400
        return jsonify(result), status

    
    return jsonify(result)