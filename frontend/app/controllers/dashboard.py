from flask import session, redirect, url_for, flash, render_template
from app.services.user_service import get_data_user

def dashboard_view():
    token = session.get("access_token")

    if not token:
        flash("Primero debes iniciar sesión", "warning")
        return redirect(url_for("main.login_view"))

    user, error = get_data_user(token)

    if error:
        flash(error, "danger")
        return redirect(url_for("main.login_view"))

    return render_template("dashboard.html", user=user)

def logout_view():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for("main.login_view"))