# login_view.py - Función corregida
from flask import render_template, request, redirect, url_for, flash, session
import requests
from app.forms import get_login_form_data
import logging

LOGIN_URL = "http://ms-usuarios/api/users/token/login"

def login_view():
    # Si el usuario ya está logueado, redirigir al dashboard
    if session.get("access_token"):
        return redirect(url_for("main.dashboard_view"))
    
    if request.method == "POST":
        try:
            credentials = get_login_form_data()
            
            response = requests.post(
                LOGIN_URL,
                data=credentials,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10  # Agregar timeout
            )
            
            logging.info(f"Login response status: {response.status_code}")
            logging.info(f"Login response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Guardar datos en session
                session["access_token"] = data.get("access_token")
                session["user_id"] = data.get("user_id", True)  # Marcar como logueado
                session["username"] = credentials.get("username")
                session["email"] = data.get("email", credentials.get("username"))  # Email del usuario
                
                flash("Login exitoso", "success")
                return redirect(url_for("main.dashboard_view"))
            
            elif response.status_code == 401:
                flash("Usuario o contraseña incorrectos", "danger")
            elif response.status_code == 422:
                flash("Datos de login inválidos", "danger") 
            else:
                flash(f"Error del servidor: {response.status_code}", "danger")
                
        except requests.exceptions.Timeout:
            flash("Timeout de conexión. Intenta nuevamente.", "danger")
        except requests.exceptions.ConnectionError:
            flash("Error de conexión al microservicio", "danger")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            flash("Error de conexión", "danger")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            flash("Error interno del servidor", "danger")
    
    return render_template("login.html")