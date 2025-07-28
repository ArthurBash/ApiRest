import requests

API_URL = "http://ms-usuarios/api/users"

def get_data_users(token):
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as e:
        return None, f"Error HTTP: {e.response.status_code} - {e.response.reason}"
    except requests.exceptions.RequestException as e:
        return None, "No se pudo conectar con el microservicio de usuarios"



def get_data_user(token):
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(f"{API_URL}/me", headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as e:
        return None, f"Error HTTP: {e.response.status_code} - {e.response.reason}"
    except requests.exceptions.RequestException as e:
        return None, "No se pudo conectar con el microservicio de usuarios"