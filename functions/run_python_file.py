import os
import subprocess


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
            timeout=30
        )

        output = ""

        if result.stdout:
            output += f"STDOUT:\n{result.stdout.strip()}\n"

        if result.stderr:
            output += f"STDERR:\n{result.stderr.strip()}\n"

        if result.returncode:
            output += f"Process exited with code {result.returncode}\n"

        if not output:
            return "No output produced."

        return output.strip()
    except Exception as e:
        return f"Error: executing Python file: {e}"
