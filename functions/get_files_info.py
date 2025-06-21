import os

from google.genai import types


def get_files_info(working_directory, directory=None):
    real_working = os.path.realpath(working_directory)
    if directory:
        real_directory = os.path.realpath(os.path.join(real_working, directory))
    common_path = os.path.commonpath([real_working, real_directory])

    if common_path != real_working:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(real_directory):
        return f'Error: "{real_directory}" is not a directory'

    items = os.listdir(real_directory)
    try:
        lines = []
        for item in items:
            item_path = os.path.join(real_directory, item)
            lines.append(
                f"{item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            )
        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
