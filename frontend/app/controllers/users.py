from flask import session, redirect, url_for, flash, render_template
from app.services.user_service import get_data_users

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
