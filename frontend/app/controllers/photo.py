from flask import session, redirect, url_for, flash, render_template,request
from app.services.photo import upload_photo_to_backend

# from app.services.user_service import get_data_user
import requests

def form_photo():
    token = session.get("access_token")

    if not token:
        flash("Primero debes iniciar sesión", "warning")
        return redirect(url_for("main.login_view"))


    return render_template("form_photo.html")



def load_photo():
    if request.method == 'POST':
        name = request.form.get('name')
        user_id = request.form.get('user_id')
        folder_id = request.form.get('folder_id')
        file = request.files.get('file')
        token = session.get("access_token")

        if not file:
            flash('No se seleccionó ningún archivo.', 'danger')
            return redirect(url_for('main.load_photo'))

        try:
            upload_photo_to_backend(name, user_id, folder_id,token, file)
            flash('Foto cargada exitosamente.', 'success')
        except requests.exceptions.RequestException as e:
            flash(f'Error al subir la foto: {e}', 'danger')

    return redirect(url_for('main.form_photo'))
