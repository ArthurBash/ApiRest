from flask import session, redirect, url_for, flash, render_template
from app.services.user_service import get_data_users,get_data_user

def users_view():
    token = session.get("access_token")

    if not token:
        flash("Primero debes iniciar sesión", "warning")
        return redirect(url_for("main.login_view"))

    usuarios, error = get_data_users(token)

    if error:
        flash(error, "danger")
        return redirect(url_for("main.login_view"))

    return render_template("users.html", usuarios=usuarios)



def get_current_user_endpoint():
    """Obtiene información del usuario actual desde el token"""
    try:
        token = session.get("access_token")

        if not token:
            flash("Primero debes iniciar sesión", "warning")
            return redirect(url_for("main.login_view"))

        usuario, error = get_data_user(token)

        if error:
            flash(error, "danger")
            return redirect(url_for("main.login_view"))
            
            return jsonify({
                "id": usuario.get("user_id"),
                "username": usuario.get("username"), 
                "email": usuario.get("email")
            })
            
    except Exception as e:
        logging.error(f"Error getting current user: {e}")
        return jsonify({"error": "Error decoding token"}), 400



