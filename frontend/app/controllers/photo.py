from flask import session, redirect, url_for, flash, render_template,request
from app.services.photo import upload_photo_to_backend,get_folders_from_api

import requests

from flask import Response
import logging
import os

def photo_proxy():
    presigned_url = request.args.get("file")
    file_response = requests.get(presigned_url)
    return Response(file_response.content, content_type=file_response.headers["Content-Type"])




MS_FOTOS_BASE_URL = os.getenv('MS_FOTOS_URL', 'http://ms-fotos/api/photo')

def load_photo():
    """Controlador para cargar foto"""
    
    folders = get_folders_from_api()
    
    if request.method == "POST":
        try:
            # Validar que se haya enviado un archivo
            if 'file' not in request.files:
                flash("No se seleccionó ningún archivo", "danger")
                return render_template("form_photo.html", folders=folders)
            
            file = request.files['file']
            if file.filename == '':
                flash("No se seleccionó ningún archivo", "danger")
                return render_template("form_photo.html", folders=folders)
            
            # Obtener datos del formulario
            form_data = {
                "name": request.form.get("name"),
                "folder_id": request.form.get("folder_id"),
                "file": file
            }
            
            # Validar datos requeridos
            if not all([form_data["name"], form_data["folder_id"]]):
                flash("Todos los campos son requeridos", "danger")
                return render_template("form_photo.html", folders=folders)
            
            # Validar que el folder_id sea válido
            valid_folder_ids = [str(folder["id"]) for folder in folders]
            if form_data["folder_id"] not in valid_folder_ids:
                flash("Carpeta seleccionada no válida", "danger")
                return render_template("form_photo.html", folders=folders)
            
            # Validar tipo de archivo (opcional)
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
            if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
                flash("Tipo de archivo no permitido. Use: " + ", ".join(allowed_extensions), "danger")
                return render_template("form_photo.html", folders=folders)
            
            # Encontrar el nombre de la carpeta para logging
            selected_folder = next((f for f in folders if str(f["id"]) == form_data["folder_id"]), None)
            if selected_folder:
                logging.info(f"Foto será cargada en la carpeta: {selected_folder['name']}")
            
            # Llamar a tu servicio para cargar la foto
            access_token = session.get("access_token")
            #user_id = session.get("user_id") 
            user_id = 'oZR2kxP2'
            result = upload_photo_to_backend(form_data['name'], user_id, form_data['folder_id'],access_token, form_data['file'])
            
            if result:
                flash("Foto cargada exitosamente", "success")
                return redirect(url_for("main.dashboard_view")) 
            else:
                flash(result.get("error", "Error al cargar la foto"), "danger")
                return render_template("form_photo.html", folders=folders)
                
                
        except Exception as e:
            logging.error(f"Error uploading photo: {e}")
            flash("Error interno del servidor", "danger")
            return render_template("form_photo.html", folders=folders)
    
    # GET request - mostrar formulario
    return render_template("form_photo.html", folders=folders)


def proxy_get_folders():
    """
    Proxy para obtener las carpetas desde el microservicio FastAPI.
    """
    try:
        # Pasa la cabecera de autorización del usuario al microservicio
        auth_header = request.headers.get('Authorization')
        headers = {'Authorization': auth_header} if auth_header else {}
        # Llama al endpoint de carpetas de FastAPI
        response = requests.get(f"{MS_FOTOS_BASE_URL}/folders", headers=headers)
        
        # Devuelve la respuesta exacta (JSON y código de estado) de FastAPI al frontend
        return Response(response.content, status=response.status_code, mimetype='application/json')

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error de conexión con el servicio de fotos: {e}"}), 503 # Service Unavailable

def proxy_get_photos():
    """
    Proxy para obtener las fotos desde FastAPI, manejando paginación y filtros.
    """
    try:
        auth_header = request.headers.get('Authorization')
        headers = {'Authorization': auth_header} if auth_header else {}

        # Reenvía todos los parámetros (page, page_size, folder_id) a FastAPI
        params = request.args.to_dict()

        response = requests.get(f"{MS_FOTOS_BASE_URL}/photos", headers=headers, params=params)
        
        return Response(response.content, status=response.status_code, mimetype='application/json')

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error de conexión con el servicio de fotos: {e}"}), 503


def gallery_view():
    # Simula una sesión de usuario para que la plantilla funcione
    session['access_token'] = 'un_token_real_o_simulado'
    session['username'] = 'usuario@ejemplo.com'
    
    # Pasa los datos necesarios a la plantilla
    access_token = session['access_token']
    user = {'email': session['username']}

    return render_template('gallery.html', access_token=access_token, user=user)
    