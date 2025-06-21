import os

from google.genai import types


def write_file(working_directory, file_path, content):
    real_working = os.path.realpath(working_directory)
    real_file_path = os.path.realpath(os.path.join(real_working, file_path))

    common_path = os.path.commonpath([real_working, real_file_path])

    if common_path != real_working:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        parent = os.path.dirname(real_file_path)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)

        with open(real_file_path, "w") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
