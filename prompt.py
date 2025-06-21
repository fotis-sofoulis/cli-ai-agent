from google.genai import types

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

- Read file contents

- Execute Python files with optional arguments

- Write or overwrite files


All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="List the file contents of the file path, less than 10.000 characters in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path that the designated file exists, relative to the working directory. If no file exists in the file path, it will fail"
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the python file in the designated file path, in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path that the designated file exists, relative to the working directory. If no file exists in the file path, or the file is not a .py file, it will fail"
            )
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the given contents in a new or existing file in the file path, in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path that the designated file exists, relative to the working directory. If no file exists in the file path, it should create it"
            ),
            "contents": types.Schema(
                type=types.Type.STRING,
                description="The file contents to be written. If none given it will fail"
            )
        }
    )
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
