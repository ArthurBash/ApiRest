class BaseCustomException(Exception):
    def __init__(self, message: str, **kwargs):
        self.message = message
        self.extra_data = kwargs
        super().__init__(self.message)

class DecodingError(BaseCustomException):
    pass

class PhotoNotFoundError(BaseCustomException):
    pass

class FolderNotFoundError(BaseCustomException):
    def __init__(self, folder_id: str = None):
        self.folder_id = folder_id
        super().__init__(f"Folder con ID {folder_id} no fue encontrado", folder_id=folder_id)

class FileNotValidate(BaseCustomException):
    pass
