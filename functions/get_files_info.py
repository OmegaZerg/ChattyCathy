import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    allowed_full_working_directory = os.path.abspath(working_directory)
    requested_directory = os.path.abspath(os.path.join(working_directory, directory if directory else "."))
    if not requested_directory.startswith(allowed_full_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(requested_directory):
        return f'Error: "{directory}" is not a directory'
    
    file_information = []
    try:
        for object in os.listdir(path=requested_directory):
            full_path = os.path.join(requested_directory, object)
            file_information.append(f"- {object}: file_size={os.path.getsize(full_path)}, is_dir={os.path.isdir(full_path)}\n")
    except OSError as OSE:
        return f"Error: file {full_path} does not exist or is inaccessible. {OSE}"
    except Exception as e:
        return f"Error: {e}"
    return "".join(file_information)

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