import requests

def upload_photo_to_backend(name, path, user_id, folder_id, file):
    files = {'file': (file.filename, file.stream, file.mimetype)}
    data = {
        'name': name,
        'path': path,
        'user_id': user_id,
        'folder_id': folder_id
    }

    response = requests.post('http://ms-fotos/api/photos/upload', data=data, files=files)
    response.raise_for_status()
    return response