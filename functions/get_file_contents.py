import os
from config import MAX_CHARS


def get_file_contents(working_directory, file_path):
    real_working = os.path.realpath(working_directory)
    real_file_path = os.path.realpath(os.path.join(real_working, file_path))

    common_path = os.path.commonpath([real_working, real_file_path])

    if common_path != real_working:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(real_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(real_file_path, "r") as file:
            file_contents = file.read(MAX_CHARS + 1)

            if len(file_contents) > MAX_CHARS:
                file_contents = (
                    file_contents[:MAX_CHARS]
                    + f'[...File "{real_file_path}" truncated at 10000 characters]'
                )
        return file_contents
    except Exception as e:
        return f"Error: {e}"
