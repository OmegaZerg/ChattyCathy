import os
from google.genai import types

def get_file_content(working_directory, file_path):
    allowed_full_working_directory = os.path.abspath(working_directory)
    requested_file = os.path.abspath(os.path.join(working_directory, file_path if file_path else "."))
    if not requested_file.startswith(allowed_full_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(requested_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000
    try:
        with open(requested_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                file_content_string += f'...File "{requested_file}" truncated at 10000 characters'
    except Exception as e:
        return f"Error: {e}"
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get content of specified file (Maximum 10000 characters), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)