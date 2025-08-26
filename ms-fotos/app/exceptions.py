

class DecodingError(Exception):
    pass

class PhotoNotFoundError(Exception):
    pass

class FolderNotFoundError(Exception):
    def __init__(self, folder_id: str = None):
        self.folder_id = folder_id
        super().__init__(f"Folder con ID {folder_id} no fue encontrado")

class FileNotValidate(Exception):
    pass