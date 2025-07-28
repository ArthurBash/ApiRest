from flask import session, redirect, url_for, flash, render_template
# from app.services.user_service import get_data_user
def create_user():
    token = session.get("access_token")

    if not token:
        flash("Primero debes iniciar sesión", "warning")
        return redirect(url_for("main.login_view"))

    return render_template("create_user.html")