from flask import request

def get_login_form_data():
    return {
        "username": request.form.get("username"),
        "password": request.form.get("password")
    }