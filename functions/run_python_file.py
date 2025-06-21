import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path):
    real_working = os.path.realpath(working_directory)
    real_file_path = os.path.realpath(os.path.join(real_working, file_path))

    common_path = os.path.commonpath([real_working, real_file_path])

    if common_path != real_working:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(real_file_path):
        return f'Error: File "{file_path}" not found.'

    if not os.path.basename(real_file_path).endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(
            ["python", real_file_path],
            cwd=real_working,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = []

        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")

        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "/n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the python file in the designated file path, in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path that the designated file exists, relative to the working directory. If no file exists in the file path, or the file is not a .py file, it will fail",
            )
        },
        required=["file_path"],
    ),
)
