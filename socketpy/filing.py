import os
from socketpy.excpetions import FileError


class Filer:

    def create_model_folder(self, name):
        path = os.path.dirname(os.path.abspath(__file__)) + name
        if not os.path.exists(path):
            os.mkdir(path)

        return path

    def create_model_file(self, name, flags):
        try:
            file_handle = os.open(name, flags)

        except OSError as e:
            raise FileError("???")
        else:  # No exception, so the file must have been created successfully.
            with os.fdopen(file_handle, 'w') as file_obj:
                file_obj.write("Look, ma, I'm writing to a new file!")
        return