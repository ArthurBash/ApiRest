from flask import render_template, request, redirect, url_for, flash, session
import requests
from app.forms import get_login_form_data
import logging
LOGIN_URL = "http://ms-usuarios/api/users/token/login"

def login_view():
    if request.method == "POST":
        credentials = get_login_form_data()
        try:
            response = requests.post(
                LOGIN_URL,
                data=credentials,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            logging.error(response)
            if response.status_code == 200:
                data = response.json()
                session["access_token"] = data.get("access_token")
                flash("Login exitoso", "success")
                return redirect(url_for("main.dashboard_view"))
            else:
                flash("Usuario o contraseña incorrectos", "danger")
        except requests.exceptions.RequestException:
            flash("Error de conexión al microservicio", "danger")
    return render_template("login.html")