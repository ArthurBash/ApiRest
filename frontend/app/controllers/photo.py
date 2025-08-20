from flask import session, redirect, url_for, flash, render_template,request
from app.services.photo import upload_photo_to_backend

# from app.services.user_service import get_data_user
import requests

from flask import Response
import logging

# def form_photo():
#     token = session.get("access_token")

#     if not token:
#         flash("Primero debes iniciar sesión", "warning")
#         return redirect(url_for("main.login_view"))


#     return render_template("form_photo.html")



# def load_photo():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         user_id = request.form.get('user_id')
#         folder_id = request.form.get('folder_id')
#         file = request.files.get('file')
#         token = session.get("access_token")

#         if not file:
#             flash('No se seleccionó ningún archivo.', 'danger')
#             return redirect(url_for('main.load_photo'))

#         try:
#             upload_photo_to_backend(name, user_id, folder_id,token, file)
#             flash('Foto cargada exitosamente.', 'success')
#         except requests.exceptions.RequestException as e:
#             flash(f'Error al subir la foto: {e}', 'danger')

#     return redirect(url_for('main.form_photo'))


def photo_proxy():
    presigned_url = request.args.get("file")
    # pedir a fastapi la presigned url
    #r = requests.get(f"http://fastapi:8000/get_presigned?file={file_path}")
    #presigned_url = r.json()["presigned_url"]

    # ahora descargar el archivo desde minio
    file_response = requests.get(presigned_url)
    return Response(file_response.content, content_type=file_response.headers["Content-Type"])



def load_photo():
    """Controlador para cargar foto"""
    
    # Carpetas hardcodeadas para prueba
    hardcoded_folders = [
        {"id": "oZR2kxP2", "name": "Fotos Personales"},
        {"id": "oZR2kxP2", "name": "Documentos"},
        {"id": "oZR2kxP2", "name": "Proyectos"},
        {"id": "oZR2kxP2", "name": "Vacaciones"},
        {"id": "oZR2kxP2", "name": "Trabajo"},
        {"id": "oZR2kxP2", "name": "Familia"},
        {"id": "oZR2kxP2", "name": "Eventos"},
        {"id": "oZR2kxP2", "name": "Otros"}
    ]
    
    if request.method == "POST":
        try:
            # Validar que se haya enviado un archivo
            if 'file' not in request.files:
                flash("No se seleccionó ningún archivo", "danger")
                return render_template("form_photo.html", folders=hardcoded_folders)
            
            file = request.files['file']
            if file.filename == '':
                flash("No se seleccionó ningún archivo", "danger")
                return render_template("form_photo.html", folders=hardcoded_folders)
            
            # Obtener datos del formulario
            form_data = {
                "name": request.form.get("name"),
                "folder_id": request.form.get("folder_id"),
                "file": file
            }
            
            # Validar datos requeridos
            if not all([form_data["name"], form_data["folder_id"]]):
                flash("Todos los campos son requeridos", "danger")
                return render_template("form_photo.html", folders=hardcoded_folders)
            
            # Validar que el folder_id sea válido
            valid_folder_ids = [str(folder["id"]) for folder in hardcoded_folders]
            if form_data["folder_id"] not in valid_folder_ids:
                flash("Carpeta seleccionada no válida", "danger")
                return render_template("form_photo.html", folders=hardcoded_folders)
            
            # Validar tipo de archivo (opcional)
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
            if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
                flash("Tipo de archivo no permitido. Use: " + ", ".join(allowed_extensions), "danger")
                return render_template("form_photo.html", folders=hardcoded_folders)
            
            # Encontrar el nombre de la carpeta para logging
            selected_folder = next((f for f in hardcoded_folders if str(f["id"]) == form_data["folder_id"]), None)
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
                return render_template("form_photo.html", folders=hardcoded_folders)
                
                
        except Exception as e:
            logging.error(f"Error uploading photo: {e}")
            flash("Error interno del servidor", "danger")
            return render_template("form_photo.html", folders=hardcoded_folders)
    
    # GET request - mostrar formulario
    return render_template("form_photo.html", folders=hardcoded_folders)