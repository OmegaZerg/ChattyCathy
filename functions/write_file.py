import os
from google.genai import types

def write_file(working_directory, file_path, content):
    allowed_full_working_directory = os.path.abspath(working_directory)
    requested_file = os.path.abspath(os.path.join(working_directory, file_path if file_path else "."))
    if not requested_file.startswith(allowed_full_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        parent_dir = os.path.dirname(requested_file)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        with open(requested_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except FileExistsError as FEE:
        return f"Error: {FEE}"
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Write to the specified file, constrained to the working directory. File is created if it does not already exist.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)