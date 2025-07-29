import requests

def upload_photo_to_backend(name, user_id, folder_id, token,file):
    headers = {"Authorization": f"Bearer {token}"}

    files = {'file': (file.filename, file.stream, file.mimetype)}
    data = {
        'name': name,
        'user_id': user_id,
        'folder_id': folder_id
    }

    response = requests.post('http://ms-fotos/api/photo/', data=data, files=files, headers=headers)
    response.raise_for_status()
    return response