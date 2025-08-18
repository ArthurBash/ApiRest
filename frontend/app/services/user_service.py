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


def get_photos(user_id, token, skip=0, limit=10):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"skip": skip, "limit": limit}
    try:
        response = requests.get(f"{API_URL}/{user_id}", headers=headers, params=params)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)
