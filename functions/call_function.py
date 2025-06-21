from google.genai import types

from functions.get_file_contents import get_file_contents, schema_get_file_contents
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(
            f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    functions = {
        "get_files_info": get_files_info,
        "get_file_contents": get_file_contents,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    function_name = function_call_part.name

    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = function_call_part.args.copy()
    args["working_directory"] = WORKING_DIR 

    actual_function = functions[function_name]
    result = actual_function(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
